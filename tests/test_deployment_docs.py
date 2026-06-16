import re
import subprocess
import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_EXAMPLE = PROJECT_ROOT / ".env.example"
DEPLOY_ENV_EXAMPLE = PROJECT_ROOT / "deploy" / "env" / "hydro.env.example"
DEPLOYMENT_DOC = PROJECT_ROOT / "docs" / "deployment.md"
DEPLOY_README = PROJECT_ROOT / "deploy" / "README.md"
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
    "HYDRO_ENV",
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
BACKUP_RESTORE_PLACEHOLDERS = {"<backup-path>", "<restore-test-db>"}
FORBIDDEN_BACKUP_RESTORE_AUTOMATION_PATTERN = re.compile(
    r"(backup\.sh|restore\.sh|sqlite3\s+.*hydro\.db|rsync\s+|scp\s+|ssh\s+|--replace\b|live restore)",
    re.IGNORECASE,
)
REQUIRED_BACKUP_RESTORE_CONCEPTS = [
    "manual SQLite backup/restore rehearsal checklist",
    "pre-deploy backup",
    "restore rehearsal",
    "rollback boundary",
    "non-destructive rehearsal",
]
REQUIRED_BACKUP_RESTORE_BOUNDARIES = [
    "Do not read, copy, open, or restore a live hydro.db during rehearsal.",
    "Do not read real environment files, secrets, ignored sensitive notes, or production data.",
    "Do not contact servers or run remote access commands.",
    "Do not add backup scripts, restore scripts, app backup logic, or destructive restore automation.",
]
REQUIRED_STAGING_HANDOFF_CONCEPTS = [
    "repo-local staging handoff checklist",
    "HYDRO_ENV=production",
    "production-like staging validation",
    "staging-specific secret values",
    "supplied outside Git",
]
REQUIRED_STAGING_DRY_RUN_CONCEPTS = [
    "staging dry-run checklist",
    "placeholder-only",
    "py scripts/validate_runtime_config.py",
    "py -m pytest",
]
REQUIRED_STAGING_MANUAL_VALIDATION_CONCEPTS = [
    "manual staging validation runbook",
    "/healthz",
    "liveness-only",
    "/login",
    "authenticated /",
    "search",
    "Ask HYDRO",
    "logs",
    "rollback",
    "backup",
]
REQUIRED_STAGING_SCOPE_BOUNDARIES = [
    "Do not introduce HYDRO_ENV=staging.",
    "Do not deploy HYDRO, contact servers, probe staging hosts, or add deploy automation.",
    "Do not read real environment files, secrets, ignored sensitive notes, staging data, or hydro.db.",
    "Do not add scripts, CI gates, server probes, app code, runtime modes, or readiness semantics for /healthz.",
]
REQUIRED_STAGING_BOOTSTRAP_FACTS = [
    "Ubuntu 22.04",
    "apt",
    "systemctl",
    "passworded sudo",
    "Python 3.10",
    "missing git",
    "missing Caddy",
    "missing sqlite3",
    "20G disk",
    "2GiB RAM",
]
REQUIRED_STAGING_BOOTSTRAP_PACKAGES = ["git", "python3-venv", "sqlite3"]
REQUIRED_STAGING_BOOTSTRAP_VERIFICATION_COMMANDS = [
    "python3 --version",
    "python3 -m venv --help",
    "git --version",
    "sqlite3 --version",
    "systemctl --version",
    "apt --version",
    "sudo -v",
    "df -h",
    "free -h",
]
REQUIRED_STAGING_BOOTSTRAP_BOUNDARIES = [
    "manual operator-run on the server",
    "Caddy is deferred",
    "Python 3.10 is an audited server fact, not compatibility approval for HYDRO's Python 3.13 baseline.",
    "enter the sudo password interactively",
    "never record, echo, store, request, or commit sudo passwords",
    "Use key-based authentication for any later approved server access",
]
FORBIDDEN_STAGING_SCOPE_PATTERN = re.compile(
    r"(HYDRO_ENV\s*=\s*staging|\bssh\s+|\bscp\s+|server probe|probe staging|deploy\.sh)",
    re.IGNORECASE,
)
FORBIDDEN_BOOTSTRAP_SCOPE_PATTERN = re.compile(
    r"(\bssh\s+|\bscp\s+|deploy\.sh|bootstrap\.sh|github\s+actions\s+deploy|read\s+real\s+(?:environment|env|database|db)|Caddyfile\s+configuration|systemd\s+configuration|configure\s+Caddy|configure\s+systemd)",
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
    assert assignments["HYDRO_ENV"] == "production"
    assert assignments["HYDRO_SESSION_COOKIE_SECURE"] == "1"
    for key, value in assignments.items():
        if key in {"HYDRO_ENV", "HYDRO_SESSION_COOKIE_SECURE"}:
            continue
        assert PLACEHOLDER_PATTERN.match(value), f"{key} must use an angle-bracket placeholder"


def test_production_signal_guidance_is_documented_in_templates_and_docs():
    combined_docs = combined_source_text()

    assert "HYDRO_ENV=production" in read(ENV_EXAMPLE)
    assert "HYDRO_ENV=production" in read(DEPLOY_ENV_EXAMPLE)
    assert "only production signal" in combined_docs
    assert "prod" in combined_docs
    assert "live" in combined_docs
    assert "Unsupported aliases" in combined_docs


def test_runtime_config_validator_accepts_committed_placeholder_templates():
    from scripts.validate_runtime_config import validate_runtime_templates

    result = validate_runtime_templates(ENV_EXAMPLE, DEPLOY_ENV_EXAMPLE)

    assert result.ok is True
    assert result.errors == []


def test_runtime_config_validator_rejects_key_parity_and_malformed_lines(tmp_path):
    from scripts.validate_runtime_config import validate_runtime_templates

    app_template = tmp_path / ".env.example"
    deploy_template = tmp_path / "hydro.env.example"
    app_template.write_text(read(ENV_EXAMPLE) + "\nEXTRA_KEY=<placeholder>\n", encoding="utf-8")
    deploy_template.write_text(read(DEPLOY_ENV_EXAMPLE) + "\nMALFORMED_LINE\n", encoding="utf-8")

    result = validate_runtime_templates(app_template, deploy_template)

    assert result.ok is False
    malformed_line_number = len(read(DEPLOY_ENV_EXAMPLE).splitlines()) + 2
    assert f"deploy/env/hydro.env.example: malformed assignment on line {malformed_line_number}" in result.errors
    assert ".env.example: unexpected key(s): EXTRA_KEY" in result.errors


def test_runtime_config_validator_rejects_real_looking_runtime_values(tmp_path):
    from scripts.validate_runtime_config import validate_runtime_templates

    app_template = tmp_path / ".env.example"
    deploy_template = tmp_path / "hydro.env.example"
    unsafe = read(ENV_EXAMPLE).replace(
        "HYDRO_SESSION_SECRET=<required-long-random-secret-from-secret-manager>",
        "HYDRO_SESSION_SECRET=super-secret-token-value-that-looks-real",
    ).replace(
        "HYDRO_DATABASE_PATH=<absolute-production-sqlite-path-owned-by-service-user>",
        "HYDRO_DATABASE_PATH=/var/lib/hydro/hydro.db",
    ).replace(
        "HYDRO_BOOTSTRAP_ADMIN_USERNAME=<optional-initial-admin-username>",
        "HYDRO_BOOTSTRAP_ADMIN_USERNAME=hydro.example.com",
    ).replace(
        "HYDRO_ALLOW_DEV_SECRET=<local-development-only-never-set-in-production>",
        "HYDRO_ALLOW_DEV_SECRET=1",
    )
    app_template.write_text(unsafe, encoding="utf-8")
    deploy_template.write_text(read(DEPLOY_ENV_EXAMPLE), encoding="utf-8")

    result = validate_runtime_templates(app_template, deploy_template)

    assert result.ok is False
    assert ".env.example: HYDRO_SESSION_SECRET must use an angle-bracket placeholder" in result.errors
    assert ".env.example: HYDRO_DATABASE_PATH must use an angle-bracket placeholder" in result.errors
    assert ".env.example: HYDRO_BOOTSTRAP_ADMIN_USERNAME must use an angle-bracket placeholder" in result.errors
    assert ".env.example: HYDRO_ALLOW_DEV_SECRET must stay placeholder-only and must not be 1" in result.errors


def test_runtime_config_validator_rejects_non_production_signal_in_templates(tmp_path):
    from scripts.validate_runtime_config import validate_runtime_templates

    app_template = tmp_path / ".env.example"
    deploy_template = tmp_path / "hydro.env.example"
    app_template.write_text(read(ENV_EXAMPLE).replace("HYDRO_ENV=production", "HYDRO_ENV=prod"), encoding="utf-8")
    deploy_template.write_text(read(DEPLOY_ENV_EXAMPLE), encoding="utf-8")

    result = validate_runtime_templates(app_template, deploy_template)

    assert result.ok is False
    assert ".env.example: HYDRO_ENV must be exactly production" in result.errors


def test_runtime_config_validator_cli_is_local_template_only():
    completed = subprocess.run(
        [sys.executable, "scripts/validate_runtime_config.py"],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "Runtime template validation passed for committed templates only." in completed.stdout
    assert "app.main" not in read(PROJECT_ROOT / "scripts" / "validate_runtime_config.py")
    assert "os.environ" not in read(PROJECT_ROOT / "scripts" / "validate_runtime_config.py")


def test_runtime_config_validator_docs_keep_boundary_visible():
    combined_docs = read(DEPLOYMENT_DOC) + "\n" + read(PROJECT_ROOT / "deploy" / "README.md")

    assert "py scripts/validate_runtime_config.py" in combined_docs
    assert "local template preflight only" in combined_docs
    assert "does not prove production readiness" in combined_docs


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


def test_sqlite_backup_restore_guidance_requires_manual_rehearsal_checklist():
    deployment_doc = read(DEPLOYMENT_DOC)
    deploy_readme = read(DEPLOY_README)

    for concept in REQUIRED_BACKUP_RESTORE_CONCEPTS:
        assert concept in deployment_doc

    assert "manual SQLite backup/restore readiness" in deploy_readme


def test_sqlite_backup_restore_examples_use_required_placeholders_only():
    deployment_doc = read(DEPLOYMENT_DOC)

    for placeholder in BACKUP_RESTORE_PLACEHOLDERS:
        assert placeholder in deployment_doc

    assert "/var/lib/hydro/hydro.db" not in deployment_doc
    assert "sqlite3 hydro.db" not in deployment_doc


def test_sqlite_backup_restore_guidance_rejects_live_access_and_destructive_automation():
    backup_restore_guidance = read(DEPLOYMENT_DOC) + "\n" + read(DEPLOY_README)

    for boundary in REQUIRED_BACKUP_RESTORE_BOUNDARIES:
        assert boundary in backup_restore_guidance

    assert FORBIDDEN_BACKUP_RESTORE_AUTOMATION_PATTERN.search(backup_restore_guidance) is None


def test_staging_handoff_documents_production_like_runtime_and_external_secrets():
    deployment_doc = read(DEPLOYMENT_DOC)
    deploy_readme = read(DEPLOY_README)

    for concept in REQUIRED_STAGING_HANDOFF_CONCEPTS:
        assert concept in deployment_doc

    assert "staging readiness" in deploy_readme
    assert "HYDRO_ENV=production" in deploy_readme
    assert "staging-specific secret values" in deploy_readme


def test_staging_dry_run_uses_local_placeholder_only_validation():
    deployment_doc = read(DEPLOYMENT_DOC)

    for concept in REQUIRED_STAGING_DRY_RUN_CONCEPTS:
        assert concept in deployment_doc

    assert "no real secrets, environment files, servers, deployment targets, or hydro.db" in deployment_doc


def test_manual_staging_validation_runbook_covers_operator_checks_without_readiness_healthz():
    deployment_doc = read(DEPLOYMENT_DOC)

    for concept in REQUIRED_STAGING_MANUAL_VALIDATION_CONCEPTS:
        assert concept in deployment_doc

    assert "citation-backed Ask HYDRO behavior" in deployment_doc
    assert "operator-owned" in deployment_doc
    assert FORBIDDEN_HEALTHZ_READINESS_PATTERN.search(deployment_doc) is None


def test_staging_readiness_rejects_scope_expansion_and_staging_runtime_mode():
    staging_guidance = read(DEPLOYMENT_DOC) + "\n" + read(DEPLOY_README)
    allowed_scope_boundary_language = "Do not add scripts, CI gates, server probes, app code, runtime modes, or readiness semantics for /healthz."
    allowed_dry_run_scope_language = "Confirm no new deployment scripts, CI gates, server probes, app code, or runtime modes were added for staging."
    allowed_runtime_boundary_language = "Do not introduce HYDRO_ENV=staging."
    allowed_deploy_boundary_language = "Do not deploy HYDRO, contact servers, probe staging hosts, or add deploy automation."
    checked_guidance = staging_guidance.replace(allowed_scope_boundary_language, "")
    checked_guidance = checked_guidance.replace(allowed_dry_run_scope_language, "").replace(allowed_runtime_boundary_language, "").replace(allowed_deploy_boundary_language, "")

    for boundary in REQUIRED_STAGING_SCOPE_BOUNDARIES:
        assert boundary in staging_guidance

    assert "hydro.db" in staging_guidance
    assert FORBIDDEN_STAGING_SCOPE_PATTERN.search(checked_guidance) is None


def test_staging_bootstrap_documents_audited_facts_and_manual_packages():
    deployment_doc = read(DEPLOYMENT_DOC)

    for fact in REQUIRED_STAGING_BOOTSTRAP_FACTS:
        assert fact in deployment_doc

    for package in REQUIRED_STAGING_BOOTSTRAP_PACKAGES:
        assert package in deployment_doc

    assert "operator-installed prerequisites" in deployment_doc
    assert "minimal prerequisites" in deployment_doc


def test_staging_bootstrap_documents_operator_run_verification_commands():
    deployment_doc = read(DEPLOYMENT_DOC)

    for command in REQUIRED_STAGING_BOOTSTRAP_VERIFICATION_COMMANDS:
        assert command in deployment_doc

    assert "manual operator-run on the server" in deployment_doc
    assert "documentation-only" in deployment_doc


def test_staging_bootstrap_keeps_security_and_scope_boundaries_visible():
    bootstrap_guidance = read(DEPLOYMENT_DOC) + "\n" + read(DEPLOY_README)
    allowed_boundary_language = "Do not add scripts, CI gates, server probes, app code, runtime modes, or readiness semantics for /healthz."
    allowed_top_boundary_language = "does not access the server, deploy HYDRO, add scripts, change CI, configure Caddy, configure systemd, read secrets, read real environment files, or read real databases."
    allowed_environment_boundary_language = "does not read real secrets, contact servers, deploy HYDRO, or prove production readiness."
    allowed_runtime_config_boundary_language = "does not read real environment files, inspect secrets, contact servers, or run deploy automation."
    allowed_systemd_verification_language = "Verification only; no systemd configuration is changed in this slice."
    allowed_staging_boundary_language = "Do not read real environment files, secrets, ignored sensitive notes, staging data, or hydro.db."
    allowed_backup_boundary_language = "Do not read real environment files, secrets, ignored sensitive notes, or production data."
    checked_guidance = bootstrap_guidance.replace(allowed_boundary_language, "")
    checked_guidance = checked_guidance.replace(allowed_top_boundary_language, "")
    checked_guidance = checked_guidance.replace(allowed_environment_boundary_language, "")
    checked_guidance = checked_guidance.replace(allowed_runtime_config_boundary_language, "")
    checked_guidance = checked_guidance.replace(allowed_systemd_verification_language, "")
    checked_guidance = checked_guidance.replace(allowed_staging_boundary_language, "")
    checked_guidance = checked_guidance.replace(allowed_backup_boundary_language, "")

    for boundary in REQUIRED_STAGING_BOOTSTRAP_BOUNDARIES:
        assert boundary in bootstrap_guidance

    assert "package-only and unconfigured" in bootstrap_guidance
    assert FORBIDDEN_BOOTSTRAP_SCOPE_PATTERN.search(checked_guidance) is None


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
