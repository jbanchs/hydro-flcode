# Design: Production Mode Signal

## Technical Approach

Add a narrow production-mode gate in `app/core/config.py` and invoke it during `app.main` construction before middleware/router setup completes. Only `HYDRO_ENV` normalized with `strip().lower()` and exactly equal to `production` enables fail-closed checks; unset, empty, or aliases such as `prod` preserve current dev/test behavior. Template validation remains committed-template-only and must not import `app.main` or read `os.environ`.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Production signal | `is_production_mode()` returns `os.getenv("HYDRO_ENV", "").strip().lower() == "production"`. | Accept aliases (`prod`, `live`) or truthy parsing. | Exact matching prevents accidental production hardening in tests/dev while still tolerating whitespace/case mistakes. |
| Fail-closed location | Add `ProductionConfigError(RuntimeError)` and `validate_production_config()` in `app/core/config.py`; call from `app/main.py` during module import/app construction. | Validate lazily per request or in script only. | Startup failure is immediate and uses the existing config module/app construction path. |
| Runtime env access | Read env values inside functions instead of relying on import-time constants for production validation. | Reuse `SESSION_SECRET_KEY`/`SESSION_COOKIE_SECURE` constants only. | Tests use `monkeypatch`; function-level reads avoid stale import-time state and reduce import isolation pain. |
| Safe database rule | In production, require explicit absolute `HYDRO_DATABASE_PATH` that is not `BASE_DIR / "hydro.db"`. | Check ownership, existence, or real server paths. | Proposal excludes server/file ownership checks; absolute non-default path is enforceable within current config design. |
| Review slicing | Treat runtime config/tests/docs as separable chained PR work units if implementation grows. | Single oversized PR. | Session preflight forces chained strategy and 400-line review budget. |

## Data Flow

```text
Process env ──→ app.core.config helpers ──→ validate_production_config()
      │                         │                    │
      └── HYDRO_ENV=production ─┴── fail closed ─────┘
                               app.main import/app construction
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `app/core/config.py` | Modify | Add `ProductionConfigError`, `is_production_mode()`, dynamic cookie/session helpers if needed, and `validate_production_config()` fail-closed checks. |
| `app/main.py` | Modify | Call `validate_production_config()` before/while constructing the FastAPI app; continue using existing middleware/router pattern. |
| `tests/conftest.py` | Modify | Ensure `HYDRO_ENV` is cleared or controlled for baseline tests to prevent host env leakage. |
| `tests/test_production_config.py` | Create | Unit/import-isolation tests for exact signal parsing, production failures, and non-production no-op behavior. |
| `tests/test_deployment_docs.py` | Modify | Extend template/doc assertions for `HYDRO_ENV` and preserve validator boundary checks. |
| `.env.example` | Modify | Add placeholder guidance for `HYDRO_ENV=production`. |
| `deploy/env/hydro.env.example` | Modify | Add matching `HYDRO_ENV=production` template key. |
| `scripts/validate_runtime_config.py` | Modify | Add `HYDRO_ENV` to required template keys and require exact `production` in committed templates only. |
| `docs/deployment.md`, `deploy/README.md` | Modify | Document production signal, unsupported aliases, fail-closed rules, rollback by unsetting/changing signal, and boundaries. |

## Interfaces / Contracts

```python
class ProductionConfigError(RuntimeError): ...

def is_production_mode() -> bool: ...
def validate_production_config() -> None: ...
```

Fail closed only when `is_production_mode()` is true. Raise `ProductionConfigError` with deterministic messages prefixed `Invalid production configuration:` and one semicolon-separated message per violation:

- `HYDRO_SESSION_SECRET is required in production`
- `HYDRO_SESSION_COOKIE_SECURE must be 1 in production`
- `HYDRO_ALLOW_DEV_SECRET must not be 1 in production`
- `HYDRO_DATABASE_PATH must be set to an absolute non-default path in production`

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Signal parsing and each fail-closed rule | `monkeypatch` env values; call config helpers directly. |
| Integration | App construction fails/succeeds under isolated env | Remove `app.main`/config modules from `sys.modules` or reload after monkeypatch; assert exception type/message. |
| Docs/templates | Template parity and boundary | Existing `test_deployment_docs.py`; validator must not import `app.main` or read real env. |
| E2E | Not available | Use `py -m pytest`; no browser automation added. |

## Migration / Rollout

No data migration required. Roll out by setting `HYDRO_ENV=production` only after real secret, secure cookie, dev-secret disabled, and absolute non-default DB path are present. Rollback: unset/change `HYDRO_ENV` away from `production` to restore current startup behavior, then revert code/docs/spec/template changes if needed.

## Open Questions

None.
