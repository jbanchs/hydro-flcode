# Apply Progress: Runtime Config Validation

## Status

Strict TDD slice complete for local runtime template validation. The implementation remains local, template-only, non-deploying, and does not import `app.main` or read real environment files.

## Completed Tasks

- [x] 1.1 Add failing tests for parser errors, key parity, missing/extra keys, and malformed assignments.
- [x] 1.2 Add failing tests rejecting real-looking runtime values and `HYDRO_ALLOW_DEV_SECRET=1`.
- [x] 1.3 Add failing tests proving local template-only boundaries.
- [x] 2.1 Create `scripts/validate_runtime_config.py` with pure parsing helpers and repo-relative paths.
- [x] 2.2 Implement validation for key parity, placeholders, secure cookie, and non-zero failure output.
- [x] 2.3 Confirm checked-in templates already satisfy the validator contract; no template edits required.
- [x] 3.1 Update `docs/deployment.md` with local template preflight wording.
- [x] 3.2 Update `deploy/README.md` manual checklist with validator command and boundary wording.
- [x] 3.3 Update `openspec/specs/deployment-readiness/spec.md` with the local validator requirements for archive baseline sync.
- [x] 4.1 Run focused and full pytest suites.
- [x] 4.2 Verify no startup fail-closed checks, secret reads, server probes, deploy jobs, or production-readiness claims were added.
- [x] 4.3 Prepare archive notes mapping implementation to deployment-readiness scenarios and rollback scope.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1-2.2 | `tests/test_deployment_docs.py` | Unit/integration | ✅ 12/12 existing deployment docs tests passed | ✅ Validator tests written before script existed | ✅ `py -m pytest tests/test_deployment_docs.py` passed 16/16 after implementation | ✅ Success, malformed line, extra key, parity, unsafe value, and CLI cases | ✅ Pure helpers extracted; tests remained green |
| 3.1-3.2 | `tests/test_deployment_docs.py` | Documentation guard | ✅ 16/16 focused tests passed before docs edits | ✅ Docs boundary test failed before docs updates | ✅ Focused suite passed 17/17 after docs updates | ✅ Command, local-template-only wording, and no-production-readiness wording covered | ➖ None needed |
| 3.3 | `tests/test_deployment_docs.py` | Spec/archive prep | ✅ Existing focused/full suites already covered active delta wording | N/A — non-code archive baseline sync from existing approved delta | ✅ Baseline spec updated from active delta requirements | ✅ Local validator, placeholder-only inputs, boundary, pytest guards, and deferred startup scenarios mapped | ➖ None needed |
| 4.1-4.2 | Full suite | Regression | N/A | N/A | ✅ `py -m pytest` passed 59/59 | ✅ Existing deployment boundary guards plus new validator guards passed | ➖ None needed |
| 4.3 | OpenSpec artifacts | Archive prep | ✅ Prior verification evidence available in apply-progress | N/A — archive notes only, no product behavior | ✅ Scenario mapping and rollback scope documented below | ✅ Each active deployment-readiness scenario maps to implementation evidence or boundary evidence | ➖ None needed |

## Test Summary

- **Total tests written**: 5
- **Total tests passing**: 59
- **Layers used**: Unit/integration documentation guards
- **Approval tests**: None — no refactoring tasks
- **Pure functions created**: 5 (`display_name`, `is_placeholder`, `parse_env_template`, `validate_template`, `validate_runtime_templates`)

## Verification

- `py -m pytest tests/test_deployment_docs.py` — 17 passed
- `py -m pytest` — 59 passed
- `py -m pytest tests/test_deployment_docs.py` — 17 passed (apply-prep confirmation for tasks 3.3 and 4.3)

## Workload / PR Boundary

- Mode: chained PR slice
- Chain strategy: feature-branch-chain
- Current work unit: Unit 1 — local template validator with RED/GREEN tests and docs
- Boundary: Adds only local committed-template validation, tests, docs, and apply/task artifacts. No deployment automation, server access, real env reads, or startup fail-closed expansion.
- Estimated review budget impact: Within the forecasted 220-340 changed lines.

## Archive Notes

### Deployment-Readiness Scenario Mapping

| Requirement | Scenario(s) | Implementation / evidence |
|-------------|-------------|---------------------------|
| Local Runtime Template Validator | Template validator succeeds for placeholder templates; Real runtime source is not accessed | `scripts/validate_runtime_config.py` reads `.env.example` and `deploy/env/hydro.env.example` only; `tests/test_deployment_docs.py` validates committed templates and guards against `app.main` / `os.environ` access. |
| Placeholder-Only Runtime Inputs | Placeholder-only values are accepted; Real-looking deployment data is rejected | Validator requires angle-bracket placeholders for sensitive/deployment-specific values and rejects secrets, hostnames, private paths, and `HYDRO_ALLOW_DEV_SECRET=1`; focused pytest guards cover both success and failure cases. |
| Runtime Config Validation Boundary | Boundary wording is visible; Scope expansion is rejected | `docs/deployment.md` and `deploy/README.md` describe the command as local template preflight only and explicitly exclude production readiness, server access, real secrets, and deployment automation. |
| Pytest Guards for Runtime Config Validation | Validator regressions are detected; Boundary regressions are detected | `tests/test_deployment_docs.py` includes validator behavior, CLI, docs wording, and boundary guards that run under `py -m pytest`. |
| Deferred Startup Fail-Closed Expansion | Runtime validation does not change app startup; Reliable production signal is missing | Validator remains a standalone script and does not import `app.main`; no startup production-mode checks or runtime app behavior were added. |

### Rollback Scope

Rollback is limited to reverting `scripts/validate_runtime_config.py`, the runtime-config tests in `tests/test_deployment_docs.py`, deployment documentation/checklist wording, the deployment-readiness spec additions, and this change's OpenSpec task/progress artifacts. Runtime application startup, server access, deployment automation, real env files, and secret handling remain unchanged.

## Remaining Tasks

- None — ready for verify.
