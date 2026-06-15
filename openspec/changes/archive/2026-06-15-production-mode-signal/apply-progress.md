# Apply Progress: Production Mode Signal

## Goal

Implement PR 1, PR 2, and PR 3 work units for OpenSpec change `production-mode-signal` with cumulative progress preserved, then prepare archive readiness notes for `openspec/specs/deployment-readiness/spec.md`.

## Mode

Strict TDD active. Runner: `py -m pytest`.

## Workload / PR Boundary

- Delivery strategy: force-chained
- Chain strategy: feature-branch-chain
- Completed work units: PR 1 env/test baseline + RED production config tests; PR 2 config/runtime validation helpers; PR 3 startup integration plus docs/templates/validator.
- Apply-prep boundary: repo-local progress artifact plus archive notes only. No product code changes.

## Completed Tasks

- [x] 1.1 Update `tests/conftest.py` to clear/control `HYDRO_ENV` and production vars for baseline tests.
- [x] 1.2 Create `tests/test_production_config.py` with RED tests for exact `production`, whitespace/case normalization, and alias rejection.
- [x] 1.3 Add RED tests in `tests/test_production_config.py` for missing secret, insecure cookie, dev-secret allowance, and unsafe DB path failures.
- [x] 2.1 Add `ProductionConfigError`, `is_production_mode()`, and dynamic env reads in `app/core/config.py`.
- [x] 2.2 Add `validate_production_config()` in `app/core/config.py` with deterministic `Invalid production configuration:` messages.
- [x] 2.3 Refactor config tests only as needed so non-production startup remains unchanged when `HYDRO_ENV` is unset or alias.
- [x] 3.1 Call `validate_production_config()` from `app/main.py` before serving requests or completing middleware/router setup.
- [x] 3.2 Extend `tests/test_production_config.py` with import-isolated app construction fail/succeed scenarios.
- [x] 4.1 Update `.env.example` and `deploy/env/hydro.env.example` with placeholder-only `HYDRO_ENV=production` guidance.
- [x] 4.2 Update `scripts/validate_runtime_config.py` and `tests/test_deployment_docs.py` for template parity without real env reads/importing `app.main`.
- [x] 4.3 Update `docs/deployment.md` and `deploy/README.md` with exact signal, unsupported aliases, rollback, and boundaries.
- [x] 5.1 Run `py -m pytest` and confirm production guard, docs/template, and non-production isolation scenarios pass.
- [x] 5.2 Prepare archive notes for `openspec/specs/deployment-readiness/spec.md` after verification.

## Archive Notes for `openspec/specs/deployment-readiness/spec.md`

- Add `Explicit Production Mode Signal`: HYDRO treats production mode as enabled only when `HYDRO_ENV.strip().lower() == "production"`; aliases such as `prod`, `live`, `1`, and `true` remain non-production.
- Add `Production Fail-Closed Runtime Checks`: when production mode is enabled, startup fails before serving requests if the session secret is missing/unsafe, secure cookies are disabled, development-secret allowance is enabled, or `HYDRO_DATABASE_PATH` is missing, relative, or the default database path.
- Add `Production Signal Documentation and Templates`: committed templates and deployment docs document `HYDRO_ENV=production`, unsupported aliases, placeholder-only values, rollback by unsetting/changing the signal, and the boundary that no deploy automation or real secret/server inspection is performed.
- Add `Isolated Production Mode Test Coverage`: tests cover exact signal detection, alias rejection, fail-closed production checks, unaffected dev/test startup, template/docs expectations, validator boundaries, and environment isolation.
- Remove/replace deferred startup fail-closed language because the explicit production signal now gates the narrow production-only enforcement.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/conftest.py` | Test infrastructure | ✅ `py -m pytest tests/conftest.py` collected 0 items / no failures | ✅ Isolation requirement identified before edit | N/A — infrastructure baseline; focused run after edit deferred to PR 1 focused file run | ➖ Structural env isolation | ➖ None needed |
| 1.2 | `tests/test_production_config.py` | Unit | N/A (new) | ✅ `py -m pytest tests/test_production_config.py` failed because `is_production_mode` did not exist | ✅ PR 2 run passed after implementation | ✅ exact production, whitespace/case normalization, alias rejection cases | ➖ None needed |
| 1.3 | `tests/test_production_config.py` | Unit | N/A (new) | ✅ `py -m pytest tests/test_production_config.py` failed because `ProductionConfigError` / `validate_production_config` did not exist | ✅ PR 2 run passed after implementation | ✅ missing secret, insecure cookie, dev-secret allowance, unset/default/relative DB path cases | ➖ None needed |
| 2.1 | `tests/test_production_config.py` | Unit | ✅ RED baseline: 16 failures from missing config API before edit | ✅ Existing PR 1 RED tests referenced missing `ProductionConfigError` / `is_production_mode` | ✅ `py -m pytest tests/test_production_config.py` passed 16/16 | ✅ production, normalized production, and aliases exercised different paths | ➖ None needed |
| 2.2 | `tests/test_production_config.py` | Unit | ✅ RED baseline: 16 failures from missing config API before edit | ✅ Existing PR 1 RED validation tests referenced missing `validate_production_config` | ✅ `py -m pytest tests/test_production_config.py` passed 16/16 | ✅ each production violation plus unsafe DB variants exercised fail-closed logic | ➖ None needed |
| 2.3 | `tests/test_production_config.py`, `tests/test_api.py` | Unit/Integration | ✅ `py -m pytest tests/test_production_config.py` passed after minimal implementation | ✅ Non-production alias/no-op behavior already covered by PR 1 RED tests | ✅ `py -m pytest tests/test_production_config.py tests/test_api.py` passed 37/37 | ✅ aliases/unset behavior remains non-production; API tests confirm existing behavior unaffected | ➖ No test refactor required |
| 3.1 | `tests/test_production_config.py` | Integration/import isolation | ✅ `py -m pytest tests/test_production_config.py tests/test_deployment_docs.py` passed 33/33 before PR 3 edits | ✅ app construction invalid production test failed because `app.main` did not call validation | ✅ focused suite passed 38/38 after wiring `validate_production_config()` before app creation | ✅ invalid production fails; valid production succeeds; alias keeps dev behavior | ➖ Minimal startup call only |
| 3.2 | `tests/test_production_config.py` | Integration/import isolation | ✅ 33/33 focused baseline before edits | ✅ import-isolated app construction scenarios written before production wiring | ✅ focused suite passed 38/38 | ✅ fail/succeed/non-production alias scenarios cover distinct paths | ➖ Helper extracted for import isolation |
| 4.1 | `tests/test_deployment_docs.py` | Docs/templates | ✅ 33/33 focused baseline before edits | ✅ env template `HYDRO_ENV=production` expectations failed before template update | ✅ focused suite passed 38/38 | ✅ root and deploy templates both asserted | ➖ None needed |
| 4.2 | `tests/test_deployment_docs.py` | Unit/docs validator | ✅ 33/33 focused baseline before edits | ✅ validator non-production signal test failed because `HYDRO_ENV` was not required/enforced | ✅ focused suite passed 38/38 | ✅ exact production accepted; `prod` rejected; boundary still asserts no `app.main` or `os.environ` | ✅ malformed-line assertion generalized after template length changed |
| 4.3 | `tests/test_deployment_docs.py` | Docs | ✅ 33/33 focused baseline before edits | ✅ docs guidance test failed before docs mentioned exact signal/aliases | ✅ focused suite passed 38/38 | ✅ docs/templates include exact signal, unsupported aliases, rollback, and no-read/no-automation boundary | ➖ None needed |
| 5.1 | Full suite | Verification | ✅ Focused suite 38/38 green | N/A — verification task | ✅ `py -m pytest` passed 81/81 after stale cookie config regression fix | ✅ full suite covers production guard, dynamic cookie setting, docs/templates, API, health, smoke, CI docs | ➖ None needed |
| 5.2 | `openspec/changes/production-mode-signal/apply-progress.md` | Archive prep | ✅ Verified cumulative apply evidence and task 5.1 full-suite result from Engram | N/A — documentation/archive-prep task after verification | ✅ Archive notes prepared from verified delta spec and implementation evidence | ➖ Single archive-prep output | ➖ None needed |

## Tests Run

- Not run in this apply-prep pass; no product code changed.
- Preserved prior evidence: `py -m pytest tests/test_production_config.py tests/test_deployment_docs.py` → 33 passed before PR 3 edits.
- Preserved prior evidence: `py -m pytest tests/test_production_config.py tests/test_deployment_docs.py` → 4 failed / 34 passed after RED tests, expected failures for missing startup wiring/templates/validator/docs.
- Preserved prior evidence: `py -m pytest tests/test_production_config.py tests/test_deployment_docs.py` → 1 failed / 37 passed after first implementation; malformed-line assertion needed generalizing after template length changed.
- Preserved prior evidence: `py -m pytest tests/test_production_config.py tests/test_deployment_docs.py` → 38 passed after refactor.
- Preserved prior evidence: `py -m pytest` → 80 passed.
- Post-review blocker fix evidence: `py -m pytest tests/test_production_config.py` → 20 passed; `py -m pytest` → 81 passed. The fix made `SessionMiddleware` read `HYDRO_SESSION_COOKIE_SECURE` dynamically at app construction time.

## Files Changed

- `openspec/changes/production-mode-signal/apply-progress.md` — created repo-local cumulative apply progress with PR 1/PR 2/PR 3 TDD evidence and archive notes.
- `openspec/changes/production-mode-signal/tasks.md` — task 5.2 marked complete after archive notes were prepared.

## Deviations

None — apply-prep matches the requested scope and does not change product code.

## Remaining Tasks

None.
