from pathlib import Path
import importlib
import sys

import pytest

from app.core import config


def test_exact_production_signal_enables_production_mode(monkeypatch):
    monkeypatch.setenv("HYDRO_ENV", "production")

    assert config.is_production_mode() is True


@pytest.mark.parametrize("value", [" production ", "PRODUCTION", "\tProduction\n"])
def test_production_signal_is_normalized(monkeypatch, value):
    monkeypatch.setenv("HYDRO_ENV", value)

    assert config.is_production_mode() is True


@pytest.mark.parametrize("value", ["prod", "live", "1", "true", "", "staging"])
def test_production_signal_rejects_aliases(monkeypatch, value):
    monkeypatch.setenv("HYDRO_ENV", value)

    assert config.is_production_mode() is False


def test_missing_production_session_secret_fails_closed(monkeypatch):
    monkeypatch.setenv("HYDRO_ENV", "production")
    monkeypatch.delenv("HYDRO_SESSION_SECRET", raising=False)
    monkeypatch.setenv("HYDRO_SESSION_COOKIE_SECURE", "1")
    monkeypatch.delenv("HYDRO_ALLOW_DEV_SECRET", raising=False)
    monkeypatch.setenv("HYDRO_DATABASE_PATH", str(Path("C:/hydro/prod.db")))

    with pytest.raises(config.ProductionConfigError, match="HYDRO_SESSION_SECRET is required in production"):
        config.validate_production_config()


def test_insecure_production_cookie_fails_closed(monkeypatch):
    monkeypatch.setenv("HYDRO_ENV", "production")
    monkeypatch.setenv("HYDRO_SESSION_SECRET", "real-production-secret")
    monkeypatch.setenv("HYDRO_SESSION_COOKIE_SECURE", "0")
    monkeypatch.delenv("HYDRO_ALLOW_DEV_SECRET", raising=False)
    monkeypatch.setenv("HYDRO_DATABASE_PATH", str(Path("C:/hydro/prod.db")))

    with pytest.raises(config.ProductionConfigError, match="HYDRO_SESSION_COOKIE_SECURE must be 1 in production"):
        config.validate_production_config()


def test_development_secret_allowance_fails_closed_in_production(monkeypatch):
    monkeypatch.setenv("HYDRO_ENV", "production")
    monkeypatch.setenv("HYDRO_SESSION_SECRET", "real-production-secret")
    monkeypatch.setenv("HYDRO_SESSION_COOKIE_SECURE", "1")
    monkeypatch.setenv("HYDRO_ALLOW_DEV_SECRET", "1")
    monkeypatch.setenv("HYDRO_DATABASE_PATH", str(Path("C:/hydro/prod.db")))

    with pytest.raises(config.ProductionConfigError, match="HYDRO_ALLOW_DEV_SECRET must not be 1 in production"):
        config.validate_production_config()


@pytest.mark.parametrize("database_path", [None, "hydro.db", str(config.BASE_DIR / "hydro.db")])
def test_unsafe_production_database_path_fails_closed(monkeypatch, database_path):
    monkeypatch.setenv("HYDRO_ENV", "production")
    monkeypatch.setenv("HYDRO_SESSION_SECRET", "real-production-secret")
    monkeypatch.setenv("HYDRO_SESSION_COOKIE_SECURE", "1")
    monkeypatch.delenv("HYDRO_ALLOW_DEV_SECRET", raising=False)
    if database_path is None:
        monkeypatch.delenv("HYDRO_DATABASE_PATH", raising=False)
    else:
        monkeypatch.setenv("HYDRO_DATABASE_PATH", database_path)

    with pytest.raises(
        config.ProductionConfigError,
        match="HYDRO_DATABASE_PATH must be set to an absolute non-default path in production",
    ):
        config.validate_production_config()


def import_app_main_after_env_change():
    sys.modules.pop("app.main", None)
    return importlib.import_module("app.main")


def test_app_construction_fails_closed_for_invalid_production_config(monkeypatch):
    monkeypatch.setenv("HYDRO_ENV", "production")
    monkeypatch.delenv("HYDRO_SESSION_SECRET", raising=False)
    monkeypatch.setenv("HYDRO_SESSION_COOKIE_SECURE", "1")
    monkeypatch.delenv("HYDRO_ALLOW_DEV_SECRET", raising=False)
    monkeypatch.setenv("HYDRO_DATABASE_PATH", str(Path("C:/hydro/prod.db")))

    with pytest.raises(config.ProductionConfigError, match="Invalid production configuration:"):
        import_app_main_after_env_change()


def test_app_construction_allows_valid_production_config(monkeypatch):
    monkeypatch.setenv("HYDRO_ENV", "production")
    monkeypatch.setenv("HYDRO_SESSION_SECRET", "real-production-secret")
    monkeypatch.setenv("HYDRO_SESSION_COOKIE_SECURE", "1")
    monkeypatch.delenv("HYDRO_ALLOW_DEV_SECRET", raising=False)
    monkeypatch.setenv("HYDRO_DATABASE_PATH", str(Path("C:/hydro/prod.db")))

    app_main = import_app_main_after_env_change()

    assert app_main.app.title == "HYDRO"


def test_app_construction_uses_current_secure_cookie_env_after_config_import(monkeypatch):
    monkeypatch.setenv("HYDRO_SESSION_COOKIE_SECURE", "0")
    importlib.reload(config)
    monkeypatch.setenv("HYDRO_ENV", "production")
    monkeypatch.setenv("HYDRO_SESSION_SECRET", "real-production-secret")
    monkeypatch.setenv("HYDRO_SESSION_COOKIE_SECURE", "1")
    monkeypatch.delenv("HYDRO_ALLOW_DEV_SECRET", raising=False)
    monkeypatch.setenv("HYDRO_DATABASE_PATH", str(Path("C:/hydro/prod.db")))

    app_main = import_app_main_after_env_change()
    session_middleware = next(
        middleware for middleware in app_main.app.user_middleware if middleware.cls.__name__ == "SessionMiddleware"
    )

    assert session_middleware.kwargs["https_only"] is True


def test_app_construction_allows_non_production_alias_with_existing_dev_behavior(monkeypatch):
    monkeypatch.setenv("HYDRO_ENV", "prod")
    monkeypatch.delenv("HYDRO_SESSION_SECRET", raising=False)
    monkeypatch.setenv("HYDRO_ALLOW_DEV_SECRET", "1")
    monkeypatch.setenv("HYDRO_SESSION_COOKIE_SECURE", "0")
    monkeypatch.setenv("HYDRO_DATABASE_PATH", "hydro.db")

    app_main = import_app_main_after_env_change()

    assert app_main.app.title == "HYDRO"
