import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"
DEPLOYMENT_DOC = PROJECT_ROOT / "docs" / "deployment.md"
README = PROJECT_ROOT / "README.md"

REQUIRED_ENV_KEYS = {
    "HYDRO_SESSION_SECRET",
    "HYDRO_DATABASE_PATH",
    "HYDRO_SESSION_COOKIE_SECURE",
    "HYDRO_BOOTSTRAP_ADMIN_USERNAME",
    "HYDRO_BOOTSTRAP_ADMIN_PASSWORD",
    "HYDRO_ALLOW_DEV_SECRET",
}

PLACEHOLDER_PATTERN = re.compile(r"^<[^<>]+>$")
PRIVATE_OR_HOST_PATTERN = re.compile(
    r"(specs/DEPLOY_INFO\.md|\b(?:\d{1,3}\.){3}\d{1,3}\b|localhost|127\.0\.0\.1|\.local\b|\.lan\b|https?://|ssh://)",
    re.IGNORECASE,
)
SECRET_VALUE_PATTERN = re.compile(
    r"(sk-[A-Za-z0-9_-]{12,}|ghp_[A-Za-z0-9_]{12,}|AKIA[0-9A-Z]{16}|[A-Za-z0-9+/]{32,}={0,2})"
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def env_assignments() -> dict[str, str]:
    assignments = {}
    for line in read(ENV_EXAMPLE).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key, value = stripped.split("=", 1)
        assignments[key] = value
    return assignments


def test_env_example_exists_with_required_placeholder_only_values():
    assignments = env_assignments()

    assert set(assignments) == REQUIRED_ENV_KEYS
    assert assignments["HYDRO_SESSION_COOKIE_SECURE"] == "1"
    for key, value in assignments.items():
        if key == "HYDRO_SESSION_COOKIE_SECURE":
            continue
        assert PLACEHOLDER_PATTERN.match(value), f"{key} must use an angle-bracket placeholder"


def test_deployment_examples_do_not_include_real_secrets_or_private_hosts():
    deployment_sources = [read(ENV_EXAMPLE), read(DEPLOYMENT_DOC)]
    combined_docs = "\n".join(deployment_sources)

    assert not PRIVATE_OR_HOST_PATTERN.search(combined_docs)
    assert not SECRET_VALUE_PATTERN.search(combined_docs)
    assert "specs/DEPLOY_INFO.md" not in "\n".join([*deployment_sources, read(README)])


def test_deployment_runbook_covers_runtime_security_and_sqlite_operations():
    deployment_doc = read(DEPLOYMENT_DOC)

    required_phrases = [
        "does not deploy",
        "reverse proxy",
        "TLS",
        "HYDRO_SESSION_COOKIE_SECURE=1",
        "firewall",
        "non-root",
        "SQLite",
        "ownership",
        "backup",
        "restore",
        "rollback",
        "scripts/init_db.py is destructive",
        "explicit backup/restore decision",
    ]

    for phrase in required_phrases:
        assert phrase in deployment_doc


def test_readme_links_deployment_readiness_without_promising_automation():
    readme = read(README)

    assert "docs/deployment.md" in readme
    assert ".env.example" in readme
    assert "does not add deployment automation" in readme
    assert "Real secrets must stay outside Git" in readme
