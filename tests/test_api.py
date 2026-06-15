import re
from pathlib import Path

from app.routers import web
from tests.conftest import TEST_ADMIN_PASSWORD, csrf_token_from, login_client

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
    assert directives["script-src"] == ["'self'"]
    assert directives["style-src"] == ["'self'"]
    assert directives["img-src"] == ["'self'", "data:"]
    assert directives["font-src"] == ["'self'", "data:"]
    assert directives["connect-src"] == ["'self'"]
    assert directives["object-src"] == ["'none'"]
    assert directives["base-uri"] == ["'self'"]
    assert directives["frame-ancestors"] == ["'none'"]
    assert directives["form-action"] == ["'self'"]
    assert "https:" not in directives["script-src"]
    assert "*" not in directives["script-src"]
    assert "https://cdn.tailwindcss.com" not in directives["script-src"]
    assert "https://cdnjs.cloudflare.com" not in directives["script-src"]
    assert "'unsafe-inline'" not in directives["style-src"]


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


def test_login_response_includes_browser_security_headers(client):
    res = client.get("/login")

    assert res.status_code == 200
    assert "Sign in" in res.text
    assert_browser_security_headers(res)


def test_authenticated_home_includes_browser_security_headers(client):
    login_client(client)
    res = client.get("/")

    assert res.status_code == 200
    assert "Regulations" in res.text
    assert_browser_security_headers(res)


def test_csp_allows_current_frontend_dependencies_and_blocks_dangerous_capabilities(client):
    res = client.get("/login")

    assert res.status_code == 200
    assert_current_frontend_csp_allowances(res.headers["content-security-policy"])


def test_authenticated_home_csp_allows_same_origin_assets_only(client):
    login_client(client)
    res = client.get("/")

    assert res.status_code == 200
    assert_current_frontend_csp_allowances(res.headers["content-security-policy"])


def test_frontend_assets_use_local_css_without_external_cdn_dependencies():
    login_template = (PROJECT_ROOT / "app" / "templates" / "login.html").read_text(encoding="utf-8")
    index_template = (PROJECT_ROOT / "app" / "templates" / "index.html").read_text(encoding="utf-8")
    app_js = (STATIC_JS_ROOT / "app.js").read_text(encoding="utf-8")
    frontend_sources = "\n".join([login_template, index_template, app_js])

    assert "/static/css/styles.css" in login_template
    assert "/static/css/styles.css" in index_template
    assert "/static/js/app.js" in index_template
    assert "https://cdn.tailwindcss.com" not in frontend_sources
    assert "cdnjs.cloudflare.com" not in frontend_sources
    assert "gsap.min.js" not in frontend_sources
    assert "window.gsap" not in app_js
    assert "gsap." not in strip_js_comments(app_js)


def test_frontend_javascript_uses_semantic_css_classes_for_dynamic_ui():
    app_js = (STATIC_JS_ROOT / "app.js").read_text(encoding="utf-8")
    js_without_comments = strip_js_comments(app_js)
    forbidden_tailwind_utilities = [
        "px-5",
        "py-4",
        "hover:bg-",
        "rounded-full",
        "bg-slate-",
        "text-xs",
        "font-mono",
        "text-slate-",
        "text-sky-",
        "font-semibold",
        "font-medium",
        "mt-2",
        "mt-3",
        "text-amber-",
    ]

    assert 'className = "table-cell"' in js_without_comments
    assert 'className = "table-row"' in js_without_comments
    assert 'className = "badge"' in js_without_comments
    assert 'paragraph("answer-line answer-line--lead"' in js_without_comments
    assert '"answer-warning"' in js_without_comments
    assert not [utility for utility in forbidden_tailwind_utilities if utility in js_without_comments]


def test_readme_documents_local_css_hardening_and_manual_visual_checks():
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    assert "Tailwind CDN has been removed" in readme
    assert "app-owned static CSS" in readme
    assert "`/static/css/styles.css`" in readme
    assert "Manual visual smoke checks" in readme
    assert "`/login`" in readme
    assert "authenticated `/`" in readme
    assert "search refresh" in readme
    assert "Ask HYDRO answer and missing-information states" in readme
    assert "Tailwind CSS via CDN" not in readme
    assert "https://cdn.tailwindcss.com" not in readme
    assert "style-src 'unsafe-inline'" not in readme


def test_home_redirects_when_unauthenticated(client):
    res = client.get("/")
    assert res.status_code == 303
    assert res.headers["location"] == "/login"


def test_protected_api_requires_auth(client):
    res = client.get("/api/regulations?search=nitrate")
    assert res.status_code == 401


def test_successful_login_redirects_and_allows_home(client):
    res = login_client(client)
    assert res.status_code == 303
    assert res.headers["location"] == "/"

    home = client.get("/")
    assert home.status_code == 200
    assert "Regulations" in home.text


def test_failed_login_does_not_create_session(client):
    res = client.get("/login")
    csrf_token = csrf_token_from(res.text)
    failed = client.post(
        "/login",
        data={"username": "admin", "password": "wrong-password", "csrf_token": csrf_token},
    )
    assert failed.status_code == 401
    assert "Invalid username or password." in failed.text

    home = client.get("/")
    assert home.status_code == 303
    assert home.headers["location"] == "/login"


def test_login_csrf_uses_constant_time_compare(monkeypatch, client):
    calls = []
    original_compare_digest = web.secrets.compare_digest

    def tracking_compare_digest(submitted_token, session_token):
        calls.append((submitted_token, session_token))
        return original_compare_digest(submitted_token, session_token)

    monkeypatch.setattr(web.secrets, "compare_digest", tracking_compare_digest)

    login_form = client.get("/login")
    session_token = csrf_token_from(login_form.text)
    res = client.post(
        "/login",
        data={"username": "admin", "password": TEST_ADMIN_PASSWORD, "csrf_token": "invalid"},
    )

    assert res.status_code == 400
    assert calls == [("invalid", session_token)]


def test_logout_clears_session(client):
    login_client(client)
    home = client.get("/")
    csrf_token = csrf_token_from(home.text)

    res = client.post("/logout", data={"csrf_token": csrf_token})
    assert res.status_code == 303
    assert res.headers["location"] == "/login"

    home = client.get("/")
    assert home.status_code == 303
    assert home.headers["location"] == "/login"


def test_logout_rejects_missing_csrf_token(client):
    login_client(client)
    res = client.post("/logout", data={})
    assert res.status_code == 422

    home = client.get("/")
    assert home.status_code == 200


def test_logout_rejects_invalid_csrf_token(client):
    login_client(client)
    res = client.post("/logout", data={"csrf_token": "invalid"})
    assert res.status_code == 400

    home = client.get("/")
    assert home.status_code == 200


def test_logout_requires_authentication(client):
    res = client.post("/logout", data={"csrf_token": "invalid"})
    assert res.status_code == 401


def test_logout_csrf_uses_constant_time_compare(monkeypatch, client):
    calls = []
    original_compare_digest = web.secrets.compare_digest

    def tracking_compare_digest(submitted_token, session_token):
        calls.append((submitted_token, session_token))
        return original_compare_digest(submitted_token, session_token)

    login_client(client)
    home = client.get("/")
    session_token = csrf_token_from(home.text)

    monkeypatch.setattr(web.secrets, "compare_digest", tracking_compare_digest)
    res = client.post("/logout", data={"csrf_token": "invalid"})

    assert res.status_code == 400
    assert calls == [("invalid", session_token)]


def test_real_database_is_untouched_by_test_setup(initialized_test_database):
    assert initialized_test_database["real_after"] == initialized_test_database["real_before"]


def test_regulations_search_nitrate(client):
    login_client(client)
    res = client.get("/api/regulations?search=nitrate")
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) >= 1
    assert any("nitrate" in item["topic"].lower() for item in data["items"])


def test_ask_hydro_ccr(client):
    login_client(client)
    res = client.post("/api/ask", json={"parameter": "consumer confidence report", "system_type": "CWS"})
    assert res.status_code == 200
    data = res.json()
    assert data["required_frequency"] == "annual"
    assert data["citation"]
