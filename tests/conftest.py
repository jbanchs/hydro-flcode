import os
import subprocess
import sys
from pathlib import Path

import pytest


TEST_ADMIN_PASSWORD = "test-admin-password"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
REAL_DATABASE_PATH = PROJECT_ROOT / "hydro.db"
TEST_DATABASE_PATH = PROJECT_ROOT / "tests" / ".tmp_hydro_test.db"

os.environ["HYDRO_DATABASE_PATH"] = str(TEST_DATABASE_PATH)
os.environ.setdefault("HYDRO_SESSION_SECRET", "test-session-secret-with-enough-entropy")
os.environ.setdefault("HYDRO_BOOTSTRAP_ADMIN_PASSWORD", TEST_ADMIN_PASSWORD)

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
