# Apply Progress: Local OpenSpec Validation

## Mode

Strict TDD. Test runner: `py -m pytest`.

## Completed Tasks

- [x] 1.1 Add failing assertions in `tests/test_deployment_docs.py` for README validation ladder wording and `py -m pytest` verification.
- [x] 1.2 Add failing assertions in `tests/test_deployment_docs.py` rejecting claims that `gentle-ai sdd-status` is strict OpenSpec CLI/schema validation.
- [x] 1.3 Add failing assertions in `tests/test_deployment_docs.py` for stable `openspec/config.yaml` local validation expectations.
- [x] 2.1 Update `README.md` with `openspec validate local-openspec-validation --strict` only when a verified CLI exists.
- [x] 2.2 Update `README.md` to describe `gentle-ai sdd-status local-openspec-validation` as native status/archive-readiness, not strict schema validation.
- [x] 2.3 Update `openspec/config.yaml` rules/context with local validation ladder expectations; do not add executable CLI dependency.
- [x] 3.1 Sync `openspec/specs/deployment-readiness/spec.md` with the accepted local validation guidance and no-deploy/no-secrets boundaries.
- [x] 3.2 Prepare archive readiness by ensuring `openspec/changes/local-openspec-validation/` contains proposal, spec, design, and this `tasks.md`.
- [x] 4.1 Run `py -m pytest tests/test_deployment_docs.py` and fix only guard/docs issues.
- [x] 4.2 Run `py -m pytest` for full local verification.
- [x] 4.3 Refactor brittle string checks in `tests/test_deployment_docs.py` into small helpers only if needed.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1-1.3 / 2.1-2.3 / 3.1 | `tests/test_deployment_docs.py` | Unit/static docs guard | ✅ 9/9 baseline passed with `py -m pytest tests/test_deployment_docs.py` | ✅ Added failing docs/config validation assertions first; 2 failures confirmed | ✅ `py -m pytest tests/test_deployment_docs.py` passed 12/12 after README/config/spec updates | ✅ Covered README ladder, forbidden fallback equivalence, config expectations, and active change spec text | ✅ Refined wording guard to avoid rejecting explicit negative statements and spec scenario examples; tests stayed green |
| 3.2 | `tests/test_deployment_docs.py` plus OpenSpec artifact presence | Unit/static docs guard | ✅ Existing OpenSpec artifacts read before edits | ✅ Existing task required artifact readiness before apply-progress existed | ✅ Proposal, design, delta spec, tasks, and apply-progress are present | ➖ Structural artifact readiness only | ➖ None needed |
| 4.1-4.3 | `tests/test_deployment_docs.py` | Unit/static docs guard | ✅ Focused guard suite available | ✅ Focused suite exposed one overly broad forbidden-pattern false positive during full run | ✅ `py -m pytest tests/test_deployment_docs.py` passed 12/12 | ✅ Full `py -m pytest` passed 54/54 after including active change spec and excluding the intentionally forbidden Given example | ✅ Guard was narrowed to misleading equivalence verbs while allowing explicit boundary wording |

## Test Summary

- **Total tests written**: 3
- **Total tests passing**: 54
- **Layers used**: Unit/static docs guard (3 new tests)
- **Approval tests**: None — no behavioral refactoring task
- **Pure functions created**: 0

## Files Changed

| File | Action | What Was Done |
|------|--------|---------------|
| `tests/test_deployment_docs.py` | Modified | Added local OpenSpec validation guard tests and constants for README/config/spec expectations. |
| `README.md` | Modified | Added local OpenSpec validation ladder, fallback boundary, and local `py -m pytest` verification guidance. |
| `openspec/config.yaml` | Modified | Added local validation metadata without adding CLI dependency or executable config. |
| `openspec/specs/deployment-readiness/spec.md` | Modified | Synced accepted local validation, no unverified CLI, and pytest guard requirements. |
| `openspec/changes/local-openspec-validation/tasks.md` | Modified | Marked all implementation and verification tasks complete. |
| `openspec/changes/local-openspec-validation/apply-progress.md` | Created | Recorded cumulative Strict TDD apply evidence and verification results. |

## Verification

- `py -m pytest tests/test_deployment_docs.py` → 12 passed
- `py -m pytest` → 54 passed

## Deviations

None — implementation matches the design.

## Issues

- The first forbidden-equivalence regex was too broad and flagged explicit negative/spec example wording. It was narrowed so the guard rejects misleading claims while allowing statements that say the fallback is not strict validation.

## Workload / PR Boundary

- Mode: stacked PR slice / single focused docs+guard work unit
- Current work unit: Unit 1, docs+pytest guard
- Boundary: local validation documentation, OpenSpec metadata/spec sync, pytest guards, and local verification only
- Estimated review budget impact: within the 120-220 line forecast and below the 400-line review budget
