# Apply Progress: Sanitize Deploy Info References

## Mode

Strict TDD, OpenSpec persistence, single PR work unit.

## Completed Tasks

- [x] 1.1 In `tests/test_deployment_docs.py`, add RED pytest coverage scanning archived OpenSpec markdown for prohibited sensitive local-note references.
- [x] 1.2 Ensure assertion output reports only relative tracked paths and generic labels, never the sensitive filename or path.
- [x] 1.3 Run focused deployment docs tests and confirm the new guard fails before redaction.
- [x] 2.1 In affected archived OpenSpec markdown, replace only sensitive local-note references with generic wording.
- [x] 2.2 Preserve surrounding audit meaning, decisions, scope, and deployment-readiness context unchanged.
- [x] 2.3 Do not read, open, copy, summarize, or name the ignored local deployment note.
- [x] 3.1 Re-run focused deployment docs tests; verify generic secret language is allowed.
- [x] 3.2 Run full pytest regression coverage.
- [x] 3.3 Create verification report with commands, results, and no-sensitive-access confirmation.
- [x] 4.1 Confirm deployment-readiness delta is archive-ready to merge without adding sensitive wording.
- [x] 4.2 Confirm this change is ready for dated OpenSpec archive movement after verification; archive was not performed during apply.
- [x] 4.3 Confirm current tracked artifacts and tasks contain generic wording only.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1-1.3 | `tests/test_deployment_docs.py` | Unit/static docs guard | ✅ `py -m pytest tests/test_deployment_docs.py` → 6 passed | ✅ Added archive markdown guard first | ✅ Guard failed before redaction: 1 failed, 6 passed | ✅ Added companion allowed-generic-language assertion | ✅ Focused suite green after helper/constant additions |
| 2.1-2.3 | `tests/test_deployment_docs.py` + archived markdown | Unit/static docs guard | ✅ Existing focused suite failure proved guard coverage | ✅ Failure identified tracked archive offenders without sensitive file access | ✅ Narrow archive wording redaction made focused suite pass | ✅ Generic wording remains explicitly allowed | ✅ No production/runtime code changed |
| 3.1-3.2 | `tests/test_deployment_docs.py` | Regression | ✅ Focused suite green before full regression | ✅ N/A — verification task validates completed behavior | ✅ `py -m pytest tests/test_deployment_docs.py` → 8 passed; `py -m pytest` → 42 passed | ✅ Focused and full suites cover both guard and allowed generic wording | ✅ No additional refactor needed |
| 3.3 | `verify-report.md` + `tests/test_deployment_docs.py` | Process verification | ✅ Existing verify report present and focused guard green | ✅ N/A — report artifact already existed from verify phase | ✅ Confirmed report includes command evidence and no-sensitive-access confirmation | ✅ Re-ran focused guard: `py -m pytest tests/test_deployment_docs.py` → 8 passed | ✅ Marked task truthfully without changing tests |
| 4.1-4.3 | `tasks.md`, `apply-progress.md`, tracked OpenSpec artifacts | Archive readiness | ✅ Active change artifacts and focused guard reviewed | ✅ N/A — process readiness only; archive intentionally not performed | ✅ Confirmed delta remains in active change for archive phase and artifacts use generic wording | ✅ Archive movement deferred as requested; readiness tasks marked as confirmations, not archive execution | ✅ Task wording adjusted to distinguish readiness from actual archive |

## Test Summary

- **Total tests written**: 2
- **Total tests passing**: 42 full suite; 8 focused deployment docs tests
- **Layers used**: Unit/static documentation guards (2 new assertions)
- **Approval tests**: None — no behavior-preserving code refactor
- **Pure functions created**: 0

## Verification

- `py -m pytest tests/test_deployment_docs.py` before edits: 6 passed
- RED run after guard test: 1 failed, 6 passed
- Focused GREEN run after redaction/triangulation: 8 passed
- Full regression: `py -m pytest` → 42 passed
- Archive-readiness confirmation: `py -m pytest tests/test_deployment_docs.py` → 8 passed

## Sensitive Access Confirmation

The ignored local deployment secret note was not read, opened, copied, summarized, or named in generated artifacts. Changes used only tracked archive markdown and generic wording.

## Remaining Tasks

None in apply. Actual OpenSpec archive movement remains a separate archive-phase action.

## Workload / PR Boundary

- Mode: single PR
- Current work unit: archive-readiness process confirmation
- Boundary: starts from existing green verify report and ends with all apply/process tasks checked; actual archive movement remains for the archive phase
- Estimated review budget impact: low; documentation/test-only cleanup remains below the 400-line budget forecast.
