from fastapi.testclient import TestClient

from app.main import app
from tests.test_api import assert_browser_security_headers


def get_healthz_response():
    with TestClient(app, follow_redirects=False) as isolated_client:
        return isolated_client.get("/healthz")


def test_healthz_returns_static_ok_json_without_authentication():
    response = get_healthz_response()

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_healthz_does_not_redirect_to_login_or_require_session_state():
    response = get_healthz_response()

    assert response.status_code == 200
    assert "location" not in response.headers
    assert "set-cookie" not in response.headers


def test_healthz_includes_browser_security_headers():
    response = get_healthz_response()

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert_browser_security_headers(response)
