from tests.conftest import csrf_token_from


REQUIRED_SECURITY_HEADERS = {
    "x-content-type-options": "nosniff",
    "referrer-policy": "strict-origin-when-cross-origin",
    "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
}


def assert_security_headers(response):
    assert response.headers["content-security-policy"]
    for header_name, expected_value in REQUIRED_SECURITY_HEADERS.items():
        assert response.headers[header_name] == expected_value


def test_healthz_is_liveness_only_json_with_security_headers(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "location" not in response.headers
    assert "set-cookie" not in response.headers
    assert_security_headers(response)


def test_login_page_exposes_local_css_auth_form_and_security_headers(client):
    response = client.get("/login")

    assert response.status_code == 200
    assert "Sign in to HYDRO" in response.text
    assert 'name="csrf_token"' in response.text
    assert 'href="/static/css/styles.css"' in response.text
    assert "https://cdn.tailwindcss.com" not in response.text
    assert "cdnjs.cloudflare.com" not in response.text
    assert_security_headers(response)


def test_authenticated_home_exposes_stable_dom_hooks_local_assets_and_security_headers(authenticated_client):
    response = authenticated_client.get("/")

    assert response.status_code == 200
    assert "Water Regulatory Intelligence" in response.text
    assert 'id="searchInput"' in response.text
    assert 'id="searchBtn"' in response.text
    assert 'id="regTable"' in response.text
    assert 'id="askBtn"' in response.text
    assert 'id="answerBox"' in response.text
    assert 'href="/static/css/styles.css"' in response.text
    assert 'src="/static/js/app.js"' in response.text
    assert "https://cdn.tailwindcss.com" not in response.text
    assert "cdnjs.cloudflare.com" not in response.text
    assert_security_headers(response)


def test_successful_login_redirects_to_home(client):
    login_page = client.get("/login")
    csrf_token = csrf_token_from(login_page.text)

    response = client.post(
        "/login",
        data={"username": "admin", "password": "test-admin-password", "csrf_token": csrf_token},
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_static_css_and_js_are_local_non_empty_app_owned_assets(client):
    css_response = client.get("/static/css/styles.css")
    js_response = client.get("/static/js/app.js")

    assert css_response.status_code == 200
    assert css_response.text.strip()
    assert css_response.headers["content-type"].startswith("text/css")
    assert ".page-login" in css_response.text
    assert "https://cdn.tailwindcss.com" not in css_response.text
    assert "cdnjs.cloudflare.com" not in css_response.text

    assert js_response.status_code == 200
    assert js_response.text.strip()
    assert "javascript" in js_response.headers["content-type"]
    assert "function searchRegs" in js_response.text
    assert "function askHydro" in js_response.text
    assert "https://cdn.tailwindcss.com" not in js_response.text
    assert "cdnjs.cloudflare.com" not in js_response.text
