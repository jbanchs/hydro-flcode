import re
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"
DEPLOYMENT_DOC = PROJECT_ROOT / "docs" / "deployment.md"
DEPLOY_DIR = PROJECT_ROOT / "deploy"
README = PROJECT_ROOT / "README.md"
ARCHIVED_OPENSPEC_MARKDOWN = PROJECT_ROOT / "openspec" / "changes" / "archive"
OPENSPEC_CONFIG = PROJECT_ROOT / "openspec" / "config.yaml"
DEPLOYMENT_READINESS_SPEC = PROJECT_ROOT / "openspec" / "specs" / "deployment-readiness" / "spec.md"
ARCHIVED_LOCAL_OPENSPEC_CHANGE_SPEC = (
    PROJECT_ROOT
    / "openspec"
    / "changes"
    / "archive"
    / "2026-06-15-local-openspec-validation"
    / "specs"
    / "deployment-readiness"
    / "spec.md"
)

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
SENSITIVE_LOCAL_NOTE_REFERENCE_PATTERN = re.compile(
    r"(?:specs[/\\]DEPLOY_INFO\.md|DEPLOY_INFO\.md)",
    re.IGNORECASE,
)
SECRET_VALUE_PATTERN = re.compile(
    r"(sk-[A-Za-z0-9_-]{12,}|ghp_[A-Za-z0-9_]{12,}|AKIA[0-9A-Z]{16}|[A-Za-z0-9+/]{32,}={0,2})"
)
FORBIDDEN_AUTOMATION_PATTERN = re.compile(
    r"(\bssh\s+|scp\s+|rsync\s+|ansible-playbook|terraform\s+apply|kubectl\s+apply|docker\s+stack\s+deploy|github\s+actions\s+deploy|deploy\.sh|backup\.sh|one-shot deploy|server access automation)",
    re.IGNORECASE,
)
REQUIRED_RUNTIME_ARTIFACTS = {
    "deploy/README.md",
    "deploy/systemd/hydro.service.example",
    "deploy/env/hydro.env.example",
    "deploy/caddy/Caddyfile.example",
}
FORBIDDEN_HEALTHZ_READINESS_PATTERN = re.compile(
    r"/healthz[^\n]*(?:is|as|for)\s+(?:a\s+)?(?:readiness|database|dependency|SQLite|authenticated workflow validation)",
    re.IGNORECASE,
)
STRICT_VALIDATION_COMMAND = "openspec validate local-openspec-validation --strict"
NATIVE_STATUS_COMMAND = "gentle-ai sdd-status local-openspec-validation"
FORBIDDEN_NATIVE_STATUS_STRICT_EQUIVALENCE_PATTERN = re.compile(
    r"gentle-ai\s+sdd-status[^\n.]{0,120}(?:performs|equals|is\s+strict|as\s+strict|replaces)[^\n.]{0,80}(?:OpenSpec|schema|validation)",
    re.IGNORECASE,
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def deploy_file_paths() -> list[Path]:
    if not DEPLOY_DIR.exists():
        return []

    return sorted(path for path in DEPLOY_DIR.rglob("*") if path.is_file())


def deployment_source_paths() -> list[Path]:
    return [ENV_EXAMPLE, DEPLOYMENT_DOC, *deploy_file_paths()]


def deployment_sources() -> dict[Path, str]:
    return {path: read(path) for path in deployment_source_paths()}


def archived_openspec_markdown_paths() -> list[Path]:
    return sorted(ARCHIVED_OPENSPEC_MARKDOWN.rglob("*.md"))


def combined_source_text(*, include_readme: bool = False) -> str:
    sources = deployment_sources()
    if include_readme:
        sources[README] = read(README)

    return "\n".join(sources.values())


def assert_no_forbidden_pattern(pattern: re.Pattern[str], label: str, *, include_readme: bool = False) -> None:
    for path, content in deployment_sources().items():
        match = pattern.search(content)
        assert match is None, f"{path.relative_to(PROJECT_ROOT)} includes forbidden {label}: {match.group(0)}"

    if include_readme:
        match = pattern.search(read(README))
        assert match is None, f"{README.relative_to(PROJECT_ROOT)} includes forbidden {label}: {match.group(0)}"


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
    assert_no_forbidden_pattern(PRIVATE_OR_HOST_PATTERN, "host, IP, URL, or private deployment reference")
    assert_no_forbidden_pattern(SECRET_VALUE_PATTERN, "secret-like token")
    assert "specs/DEPLOY_INFO.md" not in combined_source_text(include_readme=True)


def test_required_runtime_artifact_paths_are_declared_for_manual_review():
    combined_docs = combined_source_text(include_readme=True)

    for artifact in REQUIRED_RUNTIME_ARTIFACTS:
        assert (PROJECT_ROOT / artifact).exists()
        assert artifact in combined_docs


def test_deployment_runbook_covers_runtime_security_and_sqlite_operations():
    combined_docs = combined_source_text()

    required_phrases = [
        "does not deploy",
        "/etc/hydro/hydro.env",
        "uvicorn app.main:app",
        "journald",
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
        assert phrase in combined_docs


def test_deployment_docs_describe_healthz_as_liveness_only_smoke_check():
    combined_docs = combined_source_text()

    assert "/healthz" in combined_docs
    assert "liveness-only smoke check" in combined_docs
    assert "not a readiness, database, dependency, or authenticated workflow validation endpoint" in combined_docs
    assert FORBIDDEN_HEALTHZ_READINESS_PATTERN.search(combined_docs) is None


def test_deployment_readiness_rejects_server_access_and_deploy_automation():
    assert_no_forbidden_pattern(FORBIDDEN_AUTOMATION_PATTERN, "server access or deploy automation")


def test_readme_links_deployment_readiness_without_promising_automation():
    readme = read(README)

    assert "docs/deployment.md" in readme
    assert ".env.example" in readme
    assert "does not add deployment automation" in readme
    assert "Real secrets must stay outside Git" in readme


def test_archived_openspec_markdown_uses_generic_local_secret_note_language():
    offenders = [
        path.relative_to(PROJECT_ROOT).as_posix()
        for path in archived_openspec_markdown_paths()
        if SENSITIVE_LOCAL_NOTE_REFERENCE_PATTERN.search(read(path))
    ]

    assert offenders == [], "Archived OpenSpec markdown includes prohibited local secret-note reference(s)"


def test_archived_openspec_markdown_allows_generic_local_secret_note_language():
    archived_content = {
        path.relative_to(PROJECT_ROOT).as_posix(): read(path)
        for path in archived_openspec_markdown_paths()
    }
    generic_references = [
        relative_path
        for relative_path, content in archived_content.items()
        if "ignored local deployment secret note" in content
    ]

    expected_existing_references = {
        "openspec/changes/archive/2026-06-15-prepare-deployment/apply-progress.md",
        "openspec/changes/archive/2026-06-15-prepare-deployment/design.md",
        "openspec/changes/archive/2026-06-15-prepare-deployment/exploration.md",
        "openspec/changes/archive/2026-06-15-prepare-deployment/proposal.md",
        "openspec/changes/archive/2026-06-15-prepare-deployment/tasks.md",
        "openspec/changes/archive/2026-06-15-prepare-deployment/verify-report.md",
    }

    assert expected_existing_references.issubset(set(generic_references))


def test_readme_documents_local_openspec_validation_ladder_and_pytest_command():
    readme = read(README)

    assert STRICT_VALIDATION_COMMAND in readme
    assert "verified OpenSpec CLI" in readme
    assert NATIVE_STATUS_COMMAND in readme
    assert "local status/archive-readiness signal" in readme
    assert "not strict OpenSpec CLI schema validation" in readme
    assert "py -m pytest" in readme


def test_local_status_fallback_is_not_described_as_strict_validation():
    tracked_guidance = "\n".join(
        [
            read(README),
            read(OPENSPEC_CONFIG),
            read(DEPLOYMENT_READINESS_SPEC),
            read(ARCHIVED_LOCAL_OPENSPEC_CHANGE_SPEC),
        ]
    )
    tracked_guidance = tracked_guidance.replace(
        "GIVEN tracked documentation claims `gentle-ai sdd-status` performs strict OpenSpec CLI validation",
        "",
    )

    assert FORBIDDEN_NATIVE_STATUS_STRICT_EQUIVALENCE_PATTERN.search(tracked_guidance) is None


def test_openspec_config_records_local_validation_expectations_without_cli_dependency():
    config = read(OPENSPEC_CONFIG)

    assert "local_validation" in config
    assert STRICT_VALIDATION_COMMAND in config
    assert NATIVE_STATUS_COMMAND in config
    assert "not strict OpenSpec CLI schema validation" in config
    assert "Do not install, pin, or require an unverified OpenSpec CLI package" in config
