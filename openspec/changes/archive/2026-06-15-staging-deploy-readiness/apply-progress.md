# Apply Progress: Staging Deploy Readiness

## Status

- Mode: Strict TDD
- Work unit: single docs+static-guards slice
- Delivery: force-chained, stacked-to-main
- Completed tasks: 12/12
- Rollback: revert docs, tests, and OpenSpec artifacts only.

## Completed Tasks

- [x] 1.1 Add staging concept guards for `docs/deployment.md`.
- [x] 1.2 Add forbidden-boundary guards for staging scope expansion.
- [x] 1.3 Capture RED failures with focused pytest.
- [x] 2.1 Add repo-local staging handoff checklist.
- [x] 2.2 Add placeholder-only local staging dry-run checklist.
- [x] 2.3 Add operator-owned manual staging validation runbook.
- [x] 2.4 Link staging readiness from `deploy/README.md`.
- [x] 2.5 Leave `README.md` unchanged because it already exposes `docs/deployment.md`.
- [x] 3.1 Refactor guards into concept groups and regex checks.
- [x] 3.2 Verify focused staging docs tests are GREEN.
- [x] 4.1 Run full `py -m pytest` validation.
- [x] 4.2 Confirm only docs/tests/OpenSpec artifacts changed.
- [x] 4.3 Record archive mapping and rollback notes.

## TDD Cycle Evidence

| Task Group | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1-1.3 staging static guards | `tests/test_deployment_docs.py` | Unit/static | ✅ 22/22 baseline passed | ✅ 4 failing staging doc guard tests captured | ✅ Focused tests passed after docs update | ✅ Required handoff, dry-run, manual validation, and forbidden-boundary paths covered | ✅ Concept groups and regex boundary checks kept compact |
| 2.1-2.5 staging documentation | `tests/test_deployment_docs.py` | Unit/static | ✅ Baseline captured before edits | ✅ Tests required missing staging docs first | ✅ `py -m pytest tests/test_deployment_docs.py` passed | ✅ Docs cover runtime mode, external secrets, dry-run, `/healthz`, `/login`, authenticated `/`, search, Ask HYDRO, logs, rollback, backup | ➖ Documentation structure was already clean; added chunked checklist/runbook sections |
| 3.1-3.2 guard refactor | `tests/test_deployment_docs.py` | Unit/static | ✅ Focused tests passing before refactor | ✅ Existing guard expectations protected behavior | ✅ Focused tests passed after refactor | ✅ Forbidden pattern allows explicit boundary wording while catching scope expansion | ✅ Reduced brittle exact prose by using compact concept groups |
| 4.1-4.3 verification/archive prep | Full suite | Unit/integration/static | ✅ Focused suite green before full run | N/A verification task after implementation | ✅ `py -m pytest` passed 88/88 | ✅ Full suite includes deployment docs plus API/config/health coverage | ➖ No further refactor needed |

## Test Summary

- Total tests written: 4
- Total tests passing: 88 full suite; 26 deployment docs focused suite
- Layers used: Unit/static guards and existing integration suite in full pytest
- Approval tests: None — no refactoring of existing runtime behavior
- Pure functions created: 0

## Requirement Mapping

- Repo-Local Staging Handoff Checklist: `docs/deployment.md`, `deploy/README.md`, `tests/test_deployment_docs.py`
- Staging Dry-Run Checklist: `docs/deployment.md`, `tests/test_deployment_docs.py`
- Manual Staging Validation Runbook: `docs/deployment.md`, `tests/test_deployment_docs.py`
- Pytest Guards for Staging Boundaries: `tests/test_deployment_docs.py`

## Tests Run

- RED: `py -m pytest tests/test_deployment_docs.py` → 4 failed, 22 passed.
- GREEN: `py -m pytest tests/test_deployment_docs.py` → 26 passed.
- REFACTOR: `py -m pytest tests/test_deployment_docs.py` → 26 passed.
- Full: `py -m pytest` → 88 passed.

## Deviations

- `README.md` was not modified because its Deployment Readiness section already links `docs/deployment.md` and `deploy/README.md` clearly.
- OpenSpec CLI strict validation was not run; configured boundary says use only when a verified OpenSpec CLI is already installed locally. Full pytest was run instead for this apply slice.

## Risks

- Static guards intentionally allow explicit boundary wording that mentions prohibited items. Future edits should keep prohibited examples only inside negative boundary statements.
