# Tasks: Sanitize Deploy Info References

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 80-140 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR with tests, narrow archive redaction, verification/archive artifacts |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Add archive guard test first | PR 1 | Failing pytest proves prohibited tracked references are caught. |
| 2 | Redact tracked archive wording narrowly | PR 1 | Preserve audit meaning; do not access ignored local note. |
| 3 | Verify and archive SDD change | PR 1 | Include verify report and archive after green tests. |

## Phase 1: Test-First Guard

- [x] 1.1 In `tests/test_deployment_docs.py`, add RED pytest coverage scanning `openspec/changes/archive/**/*.md` for prohibited sensitive local-note references.
- [x] 1.2 Ensure assertion output reports only relative tracked paths and generic labels, never the sensitive filename or path.
- [x] 1.3 Run `python -m pytest tests/test_deployment_docs.py` and confirm the new guard fails before redaction.

## Phase 2: Narrow Archive Redaction

- [x] 2.1 In the affected archived OpenSpec markdown, replace only the sensitive local-note reference with generic wording.
- [x] 2.2 Preserve surrounding audit meaning, decisions, scope, and deployment-readiness context unchanged.
- [x] 2.3 Do not read, open, copy, summarize, or name the ignored local deployment note.

## Phase 3: Green Verification

- [x] 3.1 Re-run `python -m pytest tests/test_deployment_docs.py`; verify generic secret language is allowed.
- [x] 3.2 Run `python -m pytest` for full regression coverage.
- [x] 3.3 Create `openspec/changes/sanitize-deploy-info-references/verify-report.md` with commands, results, and no-sensitive-access confirmation.

## Phase 4: Archive

- [x] 4.1 Confirm the deployment-readiness delta is ready to merge into `openspec/specs/deployment-readiness/spec.md` without adding sensitive wording during archive.
- [x] 4.2 Confirm this change is ready to move to the dated OpenSpec archive after verification; do not archive during apply.
- [x] 4.3 Confirm current tracked artifacts and tasks contain generic wording only.
