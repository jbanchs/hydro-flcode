"""Validate committed HYDRO runtime environment templates only."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REQUIRED_ENV_KEYS = {
    "HYDRO_SESSION_SECRET",
    "HYDRO_DATABASE_PATH",
    "HYDRO_SESSION_COOKIE_SECURE",
    "HYDRO_BOOTSTRAP_ADMIN_USERNAME",
    "HYDRO_BOOTSTRAP_ADMIN_PASSWORD",
    "HYDRO_ALLOW_DEV_SECRET",
}

PLACEHOLDER_KEYS = REQUIRED_ENV_KEYS - {"HYDRO_SESSION_COOKIE_SECURE"}
DISPLAY_NAMES = {
    ".env.example": ".env.example",
    "hydro.env.example": "deploy/env/hydro.env.example",
}


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: list[str]


def display_name(path: Path) -> str:
    return DISPLAY_NAMES.get(path.name, path.name)


def is_placeholder(value: str) -> bool:
    return value.startswith("<") and value.endswith(">") and value.count("<") == 1 and value.count(">") == 1


def parse_env_template(path: Path) -> tuple[dict[str, str], list[str]]:
    assignments: dict[str, str] = {}
    errors: list[str] = []
    label = display_name(path)

    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            errors.append(f"{label}: malformed assignment on line {line_number}")
            continue
        key, value = stripped.split("=", 1)
        if not key:
            errors.append(f"{label}: malformed assignment on line {line_number}")
            continue
        assignments[key] = value

    return assignments, errors


def validate_template(path: Path) -> list[str]:
    assignments, errors = parse_env_template(path)
    label = display_name(path)
    keys = set(assignments)
    missing = sorted(REQUIRED_ENV_KEYS - keys)
    unexpected = sorted(keys - REQUIRED_ENV_KEYS)

    if missing:
        errors.append(f"{label}: missing key(s): {', '.join(missing)}")
    if unexpected:
        errors.append(f"{label}: unexpected key(s): {', '.join(unexpected)}")

    if assignments.get("HYDRO_SESSION_COOKIE_SECURE") != "1":
        errors.append(f"{label}: HYDRO_SESSION_COOKIE_SECURE must be 1")

    for key in sorted(PLACEHOLDER_KEYS & keys):
        value = assignments[key]
        if key == "HYDRO_ALLOW_DEV_SECRET" and value == "1":
            errors.append(f"{label}: HYDRO_ALLOW_DEV_SECRET must stay placeholder-only and must not be 1")
        elif not is_placeholder(value):
            errors.append(f"{label}: {key} must use an angle-bracket placeholder")

    return errors


def validate_runtime_templates(app_template: Path, deploy_template: Path) -> ValidationResult:
    errors = [*validate_template(app_template), *validate_template(deploy_template)]
    app_assignments, _ = parse_env_template(app_template)
    deploy_assignments, _ = parse_env_template(deploy_template)

    if set(app_assignments) != set(deploy_assignments):
        errors.append("runtime templates must contain identical key sets")

    return ValidationResult(ok=not errors, errors=errors)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    result = validate_runtime_templates(root / ".env.example", root / "deploy" / "env" / "hydro.env.example")
    if result.ok:
        print("Runtime template validation passed for committed templates only.")
        return 0
    print("Runtime template validation failed:")
    for error in result.errors:
        print(f"- {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
