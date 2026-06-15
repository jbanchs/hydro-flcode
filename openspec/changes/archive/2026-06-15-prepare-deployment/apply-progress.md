# Apply Progress: Prepare Deployment

## Mode

Strict TDD, OpenSpec persistence, feature-branch-chain PR slice.

## Completed Tasks

- [x] 1.1 Create `tests/test_deployment_docs.py` asserting `.env.example` exists, includes required HYDRO keys, and uses placeholder-only values.
- [x] 1.2 Add tests rejecting real-looking secrets, private hostnames/IPs, tokens, passwords, and references to `specs/DEPLOY_INFO.md` in docs/examples.
- [x] 1.3 Add tests requiring `docs/deployment.md` content for TLS/reverse proxy, secure cookies, firewall, non-root service user, SQLite ownership, backup/rollback, and destructive `scripts/init_db.py` warning.
- [x] 1.4 Add tests requiring `README.md` links to `docs/deployment.md` and `.env.example` and states this is not deploy automation.
- [x] 2.1 Create `.env.example` with placeholders for required HYDRO deployment variables.
- [x] 2.2 Create `docs/deployment.md` as a manual readiness runbook.
- [x] 2.3 Document SQLite ownership, backup, restore, rollback, and destructive init warning.
- [x] 2.4 Update `README.md` with deployment readiness links and scope warning.
- [x] 3.1 Run deployment doc guard tests.
- [x] 3.2 Run full pytest suite.
- [x] 4.1 Keep PR 1 focused on docs/examples/tests under 400 changed lines.
- [x] 4.2 Prepare PR 2 boundary for verification/archive readiness; no runtime, server, CI deploy, provisioning, or secret files changed.
- [x] 3.3 Attempt `openspec validate prepare-deployment --strict`; OpenSpec CLI remains unavailable locally and is recorded as a process warning, not a successful OpenSpec CLI validation.
- [x] 4.3 Confirm native `gentle-ai sdd-status prepare-deployment` reports archive-ready; unavailable `openspec` CLI is not treated as the archive blocker for this repo because the native dispatcher is the available SDD validation source and pytest passes.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1-1.4 | `tests/test_deployment_docs.py` | Unit docs guard | ✅ `py -m pytest tests/test_ci_workflow.py` 4/4 | ✅ 4 failing tests before docs existed | ✅ `py -m pytest tests/test_deployment_docs.py` 4/4 | ✅ placeholder, secret rejection, runbook, README cases | ✅ narrowed private-host scan to deployment artifacts while keeping README secret-reference guard |
| 2.1-2.4 | `tests/test_deployment_docs.py` | Unit docs guard | ✅ RED doc tests existed first | ✅ tests referenced missing `.env.example`, `docs/deployment.md`, README section | ✅ docs/template added and tests passed | ✅ required env, runtime security, SQLite, no-automation coverage | ✅ docs kept template-only and no executable deploy artifacts |
| 3.1-3.2 | `tests/test_deployment_docs.py`, full suite | Unit/integration | ✅ full suite after docs slice | ✅ validation tasks already covered by failing guard tests | ✅ `py -m pytest` 38/38 | ✅ full suite proves existing FastAPI/SQLite behavior unchanged | ➖ None needed |
| 3.3, 4.3 | SDD validation/source-of-truth gate | Process validation | ✅ prior verify report showed pytest passing and OpenSpec unavailable | ➖ Documentation/process task; no production/test code required | ⚠️ `openspec validate prepare-deployment --strict` attempted and unavailable | ✅ `gentle-ai sdd-status prepare-deployment` reports apply all_done, verify all_done, archive ready, tasks 14/14 | ✅ Gate wording made truthful: OpenSpec CLI unavailable is a process warning, while native status is the available archive-readiness source |

## Test Summary

- Total tests written: 4
- Total tests passing: 38
- Layers used: Unit docs guard, existing FastAPI/httpx integration suite
- Approval tests: None — no refactoring tasks
- Pure functions created: 2 test helpers (`read`, `env_assignments`)

## Validation

- ✅ `py -m pytest tests/test_deployment_docs.py` — 4 passed
- ✅ `py -m pytest` — 38 passed on latest run
- ✅ `gentle-ai sdd-status prepare-deployment` — reports `next: archive`, apply all_done, verify all_done, archive ready, tasks 14/14
- ⚠️ `openspec validate prepare-deployment --strict` — attempted again and blocked locally because `openspec` executable is not installed or not on PATH; process warning only, not a successful OpenSpec CLI validation

## Workload / PR Boundary

- Mode: chained PR slice
- Chain strategy: feature-branch-chain
- Current work unit: PR 2 verification/archive readiness documentation
- Boundary: Preserve docs/template/test implementation, record pytest evidence, attempt OpenSpec CLI validation, and truthfully document that native `gentle-ai sdd-status` is the available SDD validation source for archive readiness in this repo.
- Estimated review budget impact: intended to remain below 400 changed lines; no runtime code, server access, CI deploy jobs, provisioning, or real secrets included.

## Remaining Tasks

- [x] 3.3 Attempted `openspec validate prepare-deployment --strict`; unavailable locally and documented as a process warning.
- [x] 4.3 Native `gentle-ai sdd-status prepare-deployment` reports archive-ready; `openspec` CLI unavailability is not treated as an archive blocker for this repository.

## Current Archive Gate

- Archive is recommended by the available native SDD dispatcher. `gentle-ai sdd-status prepare-deployment` reports `next: archive`, apply all_done, verify all_done, archive ready, and tasks 14/14.
- `openspec validate prepare-deployment --strict` was attempted and remains unavailable locally because the `openspec` executable is not installed or not on PATH. This is recorded as a process warning and not as a blocker because this repo uses the native `gentle-ai sdd-status` dispatcher as the available SDD validation source.
- No successful OpenSpec CLI validation is claimed.
