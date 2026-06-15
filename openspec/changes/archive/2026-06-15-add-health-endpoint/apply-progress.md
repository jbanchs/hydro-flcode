# Apply Progress: Add Health Endpoint

## Mode

Strict TDD, using local command override `py -m pytest`.

## Completed Tasks

- [x] 1.1 Create `tests/test_health.py` unauthenticated status/body coverage.
- [x] 1.2 Add no-redirect/no-session `/healthz` coverage with `follow_redirects=False`.
- [x] 1.3 Add `/healthz` security-header assertions.
- [x] 1.4 Extend deployment docs tests for liveness-only wording and readiness misuse rejection.
- [x] 2.1 Create dependency-free `app/routers/health.py`.
- [x] 2.2 Include health router at app root in `app/main.py`.
- [x] 2.3 Run focused health/deployment-doc pytest targets.
- [x] 3.1 Update `docs/deployment.md` liveness smoke-check guidance.
- [x] 3.2 Update `deploy/README.md` manual validation guidance.
- [x] 3.3 Add non-executing systemd operator comment.
- [x] 3.4 Add Caddy proxy comment for `/healthz`.
- [x] 4.1 Run full pytest.
- [x] 4.2 Keep the change as one focused under-budget work unit.
- [x] 4.3 Record apply evidence for verification/archive.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1-1.3, 2.1-2.3 | `tests/test_health.py` | Integration | ✅ `py -m pytest tests/test_api.py tests/test_deployment_docs.py` → 29 passed | ✅ Wrote `/healthz` tests first; failed with 404 before route existed | ✅ `py -m pytest tests/test_health.py tests/test_deployment_docs.py` health tests passed after route include | ✅ Covered exact JSON, no redirect/session, and security headers | ✅ Extracted `get_healthz_response`; focused tests still passed |
| 1.4, 3.1-3.4 | `tests/test_deployment_docs.py` | Docs/runtime | ✅ `py -m pytest tests/test_api.py tests/test_deployment_docs.py` → 29 passed | ✅ Wrote docs safety-net test first; failed because `/healthz` wording was absent | ✅ Added docs/runtime template references; focused tests passed after regex correction | ✅ Positive liveness-only wording plus negative readiness misuse regex | ✅ Focused tests passed after refactor/safety-net adjustment |
| 4.1-4.3 | `openspec/changes/add-health-endpoint/tasks.md` | Process evidence | ✅ Focused suite green before full run | ✅ Verification task required full-suite evidence before completion | ✅ `py -m pytest` → 46 passed | ➖ Process evidence only | ✅ Tasks and apply-progress updated after green suite |

## Test Summary

- **Total tests written**: 4
- **Total tests passing**: 46
- **Layers used**: Integration (3), docs/runtime (1)
- **Approval tests**: None — no refactoring tasks
- **Pure functions created**: 0

## Commands Run

- `py -m pytest tests/test_api.py tests/test_deployment_docs.py` → 29 passed baseline
- `py -m pytest tests/test_health.py tests/test_deployment_docs.py` → RED: 4 failed, 8 passed
- `py -m pytest tests/test_health.py tests/test_deployment_docs.py` → 12 passed
- `py -m pytest` → 46 passed

## Deviations

None — implementation follows the design.

## Issues

The first negative docs regex also matched the required exclusion sentence. It was narrowed to reject claims that `/healthz` is/as/for readiness-like validation while allowing the mandated “not a readiness...” wording.

## Workload / PR Boundary

- Mode: single focused work-unit slice under review budget.
- Boundary: add `/healthz` route, tests, and deployment docs/runtime template references only.
- Estimated review budget impact: low; expected under 400 changed lines.
