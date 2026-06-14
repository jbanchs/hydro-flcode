import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.routers import web
from app.main import app

TEST_ADMIN_PASSWORD = "test-admin-password"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
STATIC_JS_ROOT = PROJECT_ROOT / "app" / "static" / "js"
REQUIRED_SECURITY_HEADERS = {
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
    "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
}


def assert_browser_security_headers(response):
    assert response.headers["content-security-policy"]
    for header_name, expected_value in REQUIRED_SECURITY_HEADERS.items():
        assert response.headers[header_name] == expected_value


def parse_csp_directives(csp):
    directives = {}
    for directive in csp.split(";"):
        directive = directive.strip()
        if not directive:
            continue
        name, *sources = directive.split()
        directives[name] = sources
    return directives


def assert_current_frontend_csp_allowances(csp):
    directives = parse_csp_directives(csp)
    assert directives["default-src"] == ["'self'"]
    assert directives["script-src"] == [
        "'self'",
        "https://cdn.tailwindcss.com",
        "https://cdnjs.cloudflare.com",
    ]
    assert directives["style-src"] == ["'self'", "'unsafe-inline'"]
    assert directives["img-src"] == ["'self'", "data:"]
    assert directives["font-src"] == ["'self'", "data:"]
    assert directives["connect-src"] == ["'self'"]
    assert directives["object-src"] == ["'none'"]
    assert directives["base-uri"] == ["'self'"]
    assert directives["frame-ancestors"] == ["'none'"]
    assert directives["form-action"] == ["'self'"]
    assert "https:" not in directives["script-src"]
    assert "*" not in directives["script-src"]


FRONTEND_XSS_PATTERNS = {
    "raw HTML assignment": re.compile(r"\.\s*(?:innerHTML|outerHTML)\s*="),
    "raw HTML insertion": re.compile(r"\.\s*insertAdjacentHTML\s*\("),
    "document.write": re.compile(r"\bdocument\s*\.\s*write(?:ln)?\s*\("),
    "HTML fragment parsing": re.compile(r"\.\s*createContextualFragment\s*\("),
    "eval": re.compile(r"\beval\s*\("),
    "Function constructor": re.compile(r"\bnew\s+Function\s*\("),
    "string timer callback": re.compile(r"\bset(?:Timeout|Interval)\s*\(\s*['\"`]"),
    "inline event handler assignment": re.compile(r"\.\s*on[a-z]+\s*="),
    "inline event handler attribute": re.compile(r"\.\s*setAttribute\s*\(\s*['\"`]on[a-z]+", re.IGNORECASE),
    "javascript URL": re.compile(r"(?:=|setAttribute\s*\([^,]+,)\s*['\"`]javascript:", re.IGNORECASE),
}


def strip_js_comments(source):
    result = []
    index = 0
    quote = None

    while index < len(source):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""

        if quote:
            result.append(char)
            if char == "\\" and next_char:
                result.append(next_char)
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue

        if char in {"'", '"', "`"}:
            quote = char
            result.append(char)
            index += 1
            continue

        if char == "/" and next_char == "/":
            index += 2
            while index < len(source) and source[index] != "\n":
                index += 1
            continue

        if char == "/" and next_char == "*":
            index += 2
            while index < len(source) - 1 and not (source[index] == "*" and source[index + 1] == "/"):
                if source[index] == "\n":
                    result.append("\n")
                index += 1
            index += 2
            continue

        result.append(char)
        index += 1

    return "".join(result)


def test_frontend_does_not_use_raw_html_injection():
    js_files = sorted(STATIC_JS_ROOT.rglob("*.js"))
    assert js_files, f"No frontend JS files found under {STATIC_JS_ROOT}"

    findings = []
    for js_file in js_files:
        source = strip_js_comments(js_file.read_text(encoding="utf-8"))
        for line_number, line in enumerate(source.splitlines(), start=1):
            for pattern_name, pattern in FRONTEND_XSS_PATTERNS.items():
                if pattern.search(line):
                    relative_path = js_file.relative_to(PROJECT_ROOT)
                    findings.append(f"{relative_path}:{line_number}: {pattern_name}: {line.strip()}")

    assert not findings, "Unsafe frontend JavaScript patterns found:\n" + "\n".join(findings)


def test_login_response_includes_browser_security_headers():
    with TestClient(app, follow_redirects=False) as isolated_client:
        res = isolated_client.get("/login")

    assert res.status_code == 200
    assert "Sign in" in res.text
    assert_browser_security_headers(res)


def test_authenticated_home_includes_browser_security_headers():
    with TestClient(app, follow_redirects=False) as isolated_client:
        login_client(isolated_client)
        res = isolated_client.get("/")

    assert res.status_code == 200
    assert "Regulations" in res.text
    assert_browser_security_headers(res)


def test_csp_allows_current_frontend_dependencies_and_blocks_dangerous_capabilities():
    with TestClient(app, follow_redirects=False) as isolated_client:
        res = isolated_client.get("/login")

    assert res.status_code == 200
    assert_current_frontend_csp_allowances(res.headers["content-security-policy"])


def csrf_token_from(html):
    return re.search('name="csrf_token" value="([^"]+)"', html).group(1)


def login_client(test_client):
    res = test_client.get("/login")
    csrf_token = csrf_token_from(res.text)
    return test_client.post(
        "/login",
        data={"username": "admin", "password": TEST_ADMIN_PASSWORD, "csrf_token": csrf_token},
    )


def test_home_redirects_when_unauthenticated():
    with TestClient(app, follow_redirects=False) as isolated_client:
        res = isolated_client.get("/")
    assert res.status_code == 303
    assert res.headers["location"] == "/login"


def test_protected_api_requires_auth():
    with TestClient(app, follow_redirects=False) as isolated_client:
        res = isolated_client.get("/api/regulations?search=nitrate")
    assert res.status_code == 401


def test_successful_login_redirects_and_allows_home():
    with TestClient(app, follow_redirects=False) as isolated_client:
        res = login_client(isolated_client)
        assert res.status_code == 303
        assert res.headers["location"] == "/"

        home = isolated_client.get("/")
        assert home.status_code == 200
        assert "Regulations" in home.text


def test_failed_login_does_not_create_session():
    with TestClient(app, follow_redirects=False) as isolated_client:
        res = isolated_client.get("/login")
        csrf_token = csrf_token_from(res.text)
        failed = isolated_client.post(
            "/login",
            data={"username": "admin", "password": "wrong-password", "csrf_token": csrf_token},
        )
        assert failed.status_code == 401
        assert "Invalid username or password." in failed.text

        home = isolated_client.get("/")
        assert home.status_code == 303
        assert home.headers["location"] == "/login"


def test_login_csrf_uses_constant_time_compare(monkeypatch):
    calls = []
    original_compare_digest = web.secrets.compare_digest

    def tracking_compare_digest(submitted_token, session_token):
        calls.append((submitted_token, session_token))
        return original_compare_digest(submitted_token, session_token)

    monkeypatch.setattr(web.secrets, "compare_digest", tracking_compare_digest)

    with TestClient(app, follow_redirects=False) as isolated_client:
        login_form = isolated_client.get("/login")
        session_token = csrf_token_from(login_form.text)
        res = isolated_client.post(
            "/login",
            data={"username": "admin", "password": TEST_ADMIN_PASSWORD, "csrf_token": "invalid"},
        )

    assert res.status_code == 400
    assert calls == [("invalid", session_token)]


def test_logout_clears_session():
    with TestClient(app, follow_redirects=False) as isolated_client:
        login_client(isolated_client)
        home = isolated_client.get("/")
        csrf_token = csrf_token_from(home.text)

        res = isolated_client.post("/logout", data={"csrf_token": csrf_token})
        assert res.status_code == 303
        assert res.headers["location"] == "/login"

        home = isolated_client.get("/")
        assert home.status_code == 303
        assert home.headers["location"] == "/login"


def test_logout_rejects_missing_csrf_token():
    with TestClient(app, follow_redirects=False) as isolated_client:
        login_client(isolated_client)
        res = isolated_client.post("/logout", data={})
        assert res.status_code == 422

        home = isolated_client.get("/")
        assert home.status_code == 200


def test_logout_rejects_invalid_csrf_token():
    with TestClient(app, follow_redirects=False) as isolated_client:
        login_client(isolated_client)
        res = isolated_client.post("/logout", data={"csrf_token": "invalid"})
        assert res.status_code == 400

        home = isolated_client.get("/")
        assert home.status_code == 200


def test_logout_requires_authentication():
    with TestClient(app, follow_redirects=False) as isolated_client:
        res = isolated_client.post("/logout", data={"csrf_token": "invalid"})
        assert res.status_code == 401


def test_logout_csrf_uses_constant_time_compare(monkeypatch):
    calls = []
    original_compare_digest = web.secrets.compare_digest

    def tracking_compare_digest(submitted_token, session_token):
        calls.append((submitted_token, session_token))
        return original_compare_digest(submitted_token, session_token)

    with TestClient(app, follow_redirects=False) as isolated_client:
        login_client(isolated_client)
        home = isolated_client.get("/")
        session_token = csrf_token_from(home.text)

        monkeypatch.setattr(web.secrets, "compare_digest", tracking_compare_digest)
        res = isolated_client.post("/logout", data={"csrf_token": "invalid"})

    assert res.status_code == 400
    assert calls == [("invalid", session_token)]


def test_real_database_is_untouched_by_test_setup(initialized_test_database):
    assert initialized_test_database["real_after"] == initialized_test_database["real_before"]


def test_regulations_search_nitrate():
    with TestClient(app, follow_redirects=False) as isolated_client:
        login_client(isolated_client)
        res = isolated_client.get("/api/regulations?search=nitrate")
        assert res.status_code == 200
        data = res.json()
        assert len(data["items"]) >= 1
        assert any("nitrate" in item["topic"].lower() for item in data["items"])


def test_ask_hydro_ccr():
    with TestClient(app, follow_redirects=False) as isolated_client:
        login_client(isolated_client)
        res = isolated_client.post("/api/ask", json={"parameter": "consumer confidence report", "system_type": "CWS"})
        assert res.status_code == 200
        data = res.json()
        assert data["required_frequency"] == "annual"
        assert data["citation"]
