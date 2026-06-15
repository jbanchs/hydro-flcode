import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
APP_NAME = "HYDRO"

SESSION_SECRET_KEY = os.getenv("HYDRO_SESSION_SECRET")
SESSION_COOKIE_SECURE = os.getenv("HYDRO_SESSION_COOKIE_SECURE", "0") == "1"
SESSION_COOKIE_NAME = "hydro_session"


class ProductionConfigError(RuntimeError):
    pass


def is_production_mode() -> bool:
    return os.getenv("HYDRO_ENV", "").strip().lower() == "production"


def is_session_cookie_secure() -> bool:
    return os.getenv("HYDRO_SESSION_COOKIE_SECURE", "0") == "1"


def get_database_path() -> Path:
    return Path(os.getenv("HYDRO_DATABASE_PATH", BASE_DIR / "hydro.db"))


def validate_production_config() -> None:
    if not is_production_mode():
        return

    violations = []
    database_path_value = os.getenv("HYDRO_DATABASE_PATH")
    database_path = Path(database_path_value) if database_path_value else None

    if not os.getenv("HYDRO_SESSION_SECRET"):
        violations.append("HYDRO_SESSION_SECRET is required in production")
    if os.getenv("HYDRO_SESSION_COOKIE_SECURE") != "1":
        violations.append("HYDRO_SESSION_COOKIE_SECURE must be 1 in production")
    if os.getenv("HYDRO_ALLOW_DEV_SECRET") == "1":
        violations.append("HYDRO_ALLOW_DEV_SECRET must not be 1 in production")
    if database_path is None or not database_path.is_absolute() or database_path == BASE_DIR / "hydro.db":
        violations.append("HYDRO_DATABASE_PATH must be set to an absolute non-default path in production")

    if violations:
        raise ProductionConfigError(f"Invalid production configuration: {'; '.join(violations)}")


def get_session_secret_key() -> str:
    if SESSION_SECRET_KEY:
        return SESSION_SECRET_KEY
    if os.getenv("HYDRO_ALLOW_DEV_SECRET") == "1":
        return "dev-only-hydro-session-secret-change-me"
    raise RuntimeError("HYDRO_SESSION_SECRET is required. Set HYDRO_ALLOW_DEV_SECRET=1 only for local development.")
