import os
import re
import subprocess
import sys
from pathlib import Path

import pytest


TEST_ADMIN_PASSWORD = "test-admin-password"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
REAL_DATABASE_PATH = PROJECT_ROOT / "hydro.db"
TEST_DATABASE_PATH = PROJECT_ROOT / "tests" / ".tmp_hydro_test.db"

os.environ["HYDRO_DATABASE_PATH"] = str(TEST_DATABASE_PATH)
os.environ.pop("HYDRO_ENV", None)
os.environ.setdefault("HYDRO_SESSION_SECRET", "test-session-secret-with-enough-entropy")
os.environ.setdefault("HYDRO_BOOTSTRAP_ADMIN_PASSWORD", TEST_ADMIN_PASSWORD)
os.environ.setdefault("HYDRO_SESSION_COOKIE_SECURE", "0")
os.environ.pop("HYDRO_ALLOW_DEV_SECRET", None)

from fastapi.testclient import TestClient

from app.main import app

assert Path(os.environ["HYDRO_DATABASE_PATH"]).resolve() == TEST_DATABASE_PATH.resolve()
assert Path(os.environ["HYDRO_DATABASE_PATH"]).resolve() != REAL_DATABASE_PATH.resolve()


def database_snapshot(path):
    if not path.exists():
        return None
    stat = path.stat()
    return (stat.st_size, stat.st_mtime_ns)


@pytest.fixture(scope="session", autouse=True)
def initialized_test_database():
    real_before = database_snapshot(REAL_DATABASE_PATH)
    subprocess.run([sys.executable, str(PROJECT_ROOT / "scripts" / "init_db.py")], check=True)
    real_after = database_snapshot(REAL_DATABASE_PATH)
    assert real_after == real_before
    return {"real_before": real_before, "real_after": real_after}


def csrf_token_from(html):
    return re.search('name="csrf_token" value="([^"]+)"', html).group(1)


def login_client(test_client):
    res = test_client.get("/login")
    csrf_token = csrf_token_from(res.text)
    return test_client.post(
        "/login",
        data={"username": "admin", "password": TEST_ADMIN_PASSWORD, "csrf_token": csrf_token},
    )


@pytest.fixture
def client():
    with TestClient(app, follow_redirects=False) as isolated_client:
        yield isolated_client


@pytest.fixture
def authenticated_client(client):
    login_client(client)
    return client
