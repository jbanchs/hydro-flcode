# Design: Runtime Config Validation

## Technical Approach

Add a pure local Python validator at `scripts/validate_runtime_config.py` that parses only committed env templates: `.env.example` and `deploy/env/hydro.env.example`. The validator will enforce key parity, placeholder-only sensitive/deployment-specific values, `HYDRO_SESSION_COOKIE_SECURE=1`, and no production-template dev-secret bypass. It will not import `app.main`, read real env files, contact servers, or change runtime startup behavior. Existing pytest deployment guards remain the safety net and will cover the new command, docs wording, and boundary protections.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Validator location | Create `scripts/validate_runtime_config.py` as a standalone script/module | Put checks in `app.main` startup or only in pytest | `scripts/` already hosts operator/dev commands; app startup validation needs a production-mode signal and could break local tests. |
| Inputs | Read only `.env.example` and `deploy/env/hydro.env.example` by repo-relative path | Read `.env`, `/etc/hydro/hydro.env`, or `os.environ` | Proposal boundary is template-only validation; real secrets and deployment environments are out of scope. |
| Config source | Duplicate a small explicit required-key contract in the validator/tests | Import `app.main`; deeply introspect config at import time | `app.main` calls `get_session_secret_key()` during construction and can fail without env; explicit contract is safer and reviewable. |
| Delivery | One small work-unit PR, but compatible with forced chained strategy | Split script, tests, and docs by file type | Reviewable behavior requires script + tests + docs/spec together; keep under 400 changed lines if possible. |

## Data Flow

```text
py scripts/validate_runtime_config.py
        │
        ├── parse .env.example
        ├── parse deploy/env/hydro.env.example
        ├── validate exact key parity and expected values
        └── print result / exit 0 or non-zero
```

Pytest imports/calls the script with fixture temp files or direct helper functions to prove pass/fail behavior without reading real env files.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `scripts/validate_runtime_config.py` | Create | Pure parser/validator and CLI entrypoint for committed templates only. |
| `tests/test_deployment_docs.py` | Modify | Add coverage for validator success/failure, template parity, docs wording, and no real-env/app-main boundary. |
| `.env.example` | Modify if needed | Keep production template aligned with validator contract. |
| `deploy/env/hydro.env.example` | Modify if needed | Keep deploy env template aligned with `.env.example`. |
| `docs/deployment.md` | Modify | Document local template preflight command and its limits. |
| `deploy/README.md` | Modify | Add command to manual validation order without implying deployment automation. |
| `openspec/specs/deployment-readiness/spec.md` | Modify | Add requirement/scenarios for local runtime config template validation. |

## Interfaces / Contracts

Validator contract:

```python
REQUIRED_ENV_KEYS = {
    "HYDRO_SESSION_SECRET",
    "HYDRO_DATABASE_PATH",
    "HYDRO_SESSION_COOKIE_SECURE",
    "HYDRO_BOOTSTRAP_ADMIN_USERNAME",
    "HYDRO_BOOTSTRAP_ADMIN_PASSWORD",
    "HYDRO_ALLOW_DEV_SECRET",
}
```

- Non-comment assignments use `KEY=VALUE`; malformed lines fail validation.
- Both template files must contain exactly the required keys with identical key sets.
- `HYDRO_SESSION_COOKIE_SECURE` must be `1`.
- All other values must be angle-bracket placeholders.
- `HYDRO_ALLOW_DEV_SECRET` must remain a placeholder, not `1`.
- CLI exit code `0` means committed templates pass; non-zero means template validation failed.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Parser and validation failures | Import pure helper functions with temp template files; no `app.main` import. |
| Integration | Real committed templates and docs | Extend `tests/test_deployment_docs.py` to call validator and inspect docs/spec wording. |
| E2E | Not applicable | No browser/deployment automation for this slice. |

Verification command: `py -m pytest`.

## Migration / Rollout

No migration required. Roll out as a local preflight only. Rollback is reverting the script, tests, docs, template/spec changes; runtime behavior remains unchanged.

## Open Questions

None.
