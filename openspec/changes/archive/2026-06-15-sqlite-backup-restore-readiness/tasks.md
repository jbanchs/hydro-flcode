# Tasks: SQLite Backup Restore Readiness

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 120-220 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single docs+test work unit |
| Delivery strategy | force-chained |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: stacked-to-main
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Add static guards and matching SQLite rehearsal docs | PR 1 | Single docs+test slice under budget; tests stay with docs. |

## Phase 1: RED Static Guards

- [x] 1.1 In `tests/test_deployment_docs.py`, add failing guards requiring `docs/deployment.md` to include manual SQLite backup/restore rehearsal checklist wording.
- [x] 1.2 In `tests/test_deployment_docs.py`, add failing guards requiring `<backup-path>` and `<restore-test-db>` placeholder examples only.
- [x] 1.3 In `tests/test_deployment_docs.py`, add failing guards rejecting real `hydro.db`, env/secret/private-note/server access, backup/restore scripts, and destructive live-restore wording.
- [x] 1.4 Run `py -m pytest tests/test_deployment_docs.py` and capture the expected RED failures.

## Phase 2: GREEN Documentation

- [x] 2.1 Update `docs/deployment.md` `SQLite Backup, Restore, and Rollback` guidance with a manual, non-destructive rehearsal checklist using placeholders only.
- [x] 2.2 Add warning boundaries in `docs/deployment.md`: no live DB, real env files, secrets, ignored sensitive notes, servers, production data, or destructive automation.
- [x] 2.3 Update `deploy/README.md` validation order to reference manual SQLite backup/restore readiness without duplicating the runbook.
- [x] 2.4 Re-run `py -m pytest tests/test_deployment_docs.py` and make RED guards pass without adding scripts or runtime code.

## Phase 3: Refactor and Verification

- [x] 3.1 Refactor guard helpers/constants in `tests/test_deployment_docs.py` for stable concept checks over exact prose.
- [x] 3.2 Run full `py -m pytest` to verify deployment-readiness and existing runtime config guards.
- [x] 3.3 Check `git diff --stat` remains under the 400-line review budget and contains only docs, tests, and OpenSpec artifacts.

## Phase 4: Archive Prep

- [x] 4.1 Confirm `openspec/changes/sqlite-backup-restore-readiness/specs/deployment-readiness/spec.md` matches implemented wording boundaries.
- [x] 4.2 Prepare archive notes: no runtime interfaces, no DB access, rollback is reverting docs/tests/OpenSpec delta.
