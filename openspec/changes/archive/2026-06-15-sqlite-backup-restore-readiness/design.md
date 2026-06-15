# Design: SQLite Backup Restore Readiness

## Technical Approach

Tighten the existing deployment-readiness documentation by adding a manual, placeholder-only SQLite backup/restore rehearsal checklist and static pytest guards. This change remains documentation/test-only: no scripts, app logic, real database access, server access, restore fixtures, or executable automation. The design follows the existing `tests/test_deployment_docs.py` pattern of stable regex/content guards over exact prose.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Documentation location | Extend `docs/deployment.md` as the primary runbook and `deploy/README.md` as the short validation-order index. | Create a new backup guide. | Existing deployment readiness content already owns SQLite backup/rollback warnings; keeping the checklist there reduces navigation cost. |
| Guard style | Add static pytest assertions for required safety concepts, placeholders, and forbidden destructive/automation patterns. | Snapshot or exact-paragraph matching. | Static concept guards protect boundaries without making wording brittle. |
| Scope boundary | Keep rehearsal commands as non-runnable placeholder examples using values like `<backup-path>` and `<restore-test-db>`. | Add restore scripts, temp DB fixtures, or live SQLite checks. | Proposal explicitly forbids real DB access and automation in this slice. |
| Delivery slicing | One review slice: docs plus the tests that verify those docs. | Separate docs-only and tests-only PRs. | Tests are the acceptance guard for the doc behavior and should travel with the user-visible guidance. |

## Data Flow

Manual operator review only:

    Operator reads docs/deployment.md
        ├─ confirms backup/restore rehearsal boundaries
        ├─ adapts placeholders outside Git only
        └─ runs py -m pytest to verify tracked docs stay safe

No application request flow, service/router/database runtime path, network call, or SQLite connection is introduced.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `docs/deployment.md` | Modify | Expand `SQLite Backup, Restore, and Rollback` into a manual rehearsal checklist with placeholder-only commands/paths, no-live-DB warnings, and destructive-operation boundaries. |
| `deploy/README.md` | Modify | Reference the manual backup/restore readiness check in validation order without duplicating the full runbook. |
| `tests/test_deployment_docs.py` | Modify | Add static guards for required checklist concepts, placeholder-only examples, forbidden real paths/secrets/private notes, forbidden backup/restore scripts, and destructive live-restore wording. |

## Interfaces / Contracts

No runtime interfaces change. Test contracts should be stable and concept-based:

```python
BACKUP_RESTORE_PLACEHOLDERS = {"<backup-path>", "<restore-test-db>"}
FORBIDDEN_BACKUP_RESTORE_AUTOMATION_PATTERN = re.compile(
    r"(backup\.sh|restore\.sh|sqlite3\s+.*hydro\.db|rsync\s+|scp\s+|ssh\s+|--replace\b|live restore)",
    re.IGNORECASE,
)
```

Assertions should verify: `docs/deployment.md` includes manual rehearsal/checklist language, examples use angle-bracket placeholders, live `hydro.db`/real env/secrets/server/private-note references are prohibited, and no backup/restore scripts or destructive automation are documented.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit/static docs | Required backup/restore safety boundaries and placeholders. | Extend `tests/test_deployment_docs.py` with regex/content assertions against tracked docs. |
| Integration | Existing deployment documentation suite remains coherent with runtime config guards. | Run full `py -m pytest`. |
| E2E | Not applicable. | No browser/server/database workflow is part of this change. |

## Migration / Rollout

No migration required. This is a docs and static-test guard change only. Rollback is reverting `docs/deployment.md`, `deploy/README.md`, `tests/test_deployment_docs.py`, and the OpenSpec delta artifacts.

## Open Questions

- [ ] None.
