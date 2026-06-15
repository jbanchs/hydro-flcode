# Tasks: Production Mode Signal

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 420-650 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 env/test baseline → PR 2 config/runtime checks → PR 3 startup/docs/templates |
| Delivery strategy | force-chained |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Isolate env and add RED production config tests | PR 1 | base = feature/tracker branch; tests fail before config helpers exist |
| 2 | Add config helpers and fail-closed validation | PR 2 | base = PR 1 branch; makes unit tests pass |
| 3 | Wire startup plus templates/docs/validator | PR 3 | base = PR 2 branch; app construction and operator guidance |

## Phase 1: Env Isolation Baseline / RED Tests

- [x] 1.1 Update `tests/conftest.py` to clear/control `HYDRO_ENV` and production vars for baseline tests.
- [x] 1.2 Create `tests/test_production_config.py` with RED tests for exact `production`, whitespace/case normalization, and alias rejection.
- [x] 1.3 Add RED tests in `tests/test_production_config.py` for missing secret, insecure cookie, dev-secret allowance, and unsafe DB path failures.

## Phase 2: Config Implementation / GREEN

- [x] 2.1 Add `ProductionConfigError`, `is_production_mode()`, and dynamic env reads in `app/core/config.py`.
- [x] 2.2 Add `validate_production_config()` in `app/core/config.py` with deterministic `Invalid production configuration:` messages.
- [x] 2.3 Refactor config tests only as needed so non-production startup remains unchanged when `HYDRO_ENV` is unset or alias.

## Phase 3: Startup Integration

- [x] 3.1 Call `validate_production_config()` from `app/main.py` before serving requests or completing middleware/router setup.
- [x] 3.2 Extend `tests/test_production_config.py` with import-isolated app construction fail/succeed scenarios.

## Phase 4: Templates, Docs, Validator

- [x] 4.1 Update `.env.example` and `deploy/env/hydro.env.example` with placeholder-only `HYDRO_ENV=production` guidance.
- [x] 4.2 Update `scripts/validate_runtime_config.py` and `tests/test_deployment_docs.py` for template parity without real env reads/importing `app.main`.
- [x] 4.3 Update `docs/deployment.md` and `deploy/README.md` with exact signal, unsupported aliases, rollback, and boundaries.

## Phase 5: Verification / Archive Prep

- [x] 5.1 Run `py -m pytest` and confirm production guard, docs/template, and non-production isolation scenarios pass.
- [x] 5.2 Prepare archive notes for `openspec/specs/deployment-readiness/spec.md` after verification.
