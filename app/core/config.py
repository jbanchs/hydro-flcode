import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
APP_NAME = "HYDRO"

SESSION_SECRET_KEY = os.getenv("HYDRO_SESSION_SECRET")
SESSION_COOKIE_SECURE = os.getenv("HYDRO_SESSION_COOKIE_SECURE", "0") == "1"
SESSION_COOKIE_NAME = "hydro_session"


def get_database_path() -> Path:
    return Path(os.getenv("HYDRO_DATABASE_PATH", BASE_DIR / "hydro.db"))


def get_session_secret_key() -> str:
    if SESSION_SECRET_KEY:
        return SESSION_SECRET_KEY
    if os.getenv("HYDRO_ALLOW_DEV_SECRET") == "1":
        return "dev-only-hydro-session-secret-change-me"
    raise RuntimeError("HYDRO_SESSION_SECRET is required. Set HYDRO_ALLOW_DEV_SECRET=1 only for local development.")
