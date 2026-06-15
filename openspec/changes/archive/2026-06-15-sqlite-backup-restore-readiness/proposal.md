# Proposal: SQLite Backup Restore Readiness

## Intent

Make HYDRO's SQLite backup/restore readiness reviewable before deployment by adding manual, placeholder-only rehearsal guidance and static pytest guards. This closes the gap between existing high-level backup warnings and an operator-safe checklist without touching real databases, secrets, servers, or destructive restore automation.

## Scope

### In Scope
- Document a manual SQLite backup/restore rehearsal checklist with placeholder commands/paths only.
- Add warning boundaries: do not touch live `hydro.db`, real env files, secrets, ignored sensitive notes, servers, or production data during rehearsal.
- Add pytest static guards for required wording, placeholder-only examples, no backup/restore scripts, and no destructive live-restore instructions.

### Out of Scope
- Backup/restore scripts, app-level backup logic, endpoints, jobs, or server automation.
- Temp SQLite restore fixtures or executable restore rehearsals unless justified in a later slice.
- Reading or validating real env files, real deployment notes, real `hydro.db`, or production paths.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `deployment-readiness`: Tighten SQLite backup/restore rehearsal documentation and static guard requirements while preserving documentation-only deployment boundaries.

## Approach

Update deployment docs with a clearly labeled manual rehearsal checklist using placeholders such as `<backup-path>` and `<restore-test-db>`. Extend existing deployment documentation tests with static assertions that enforce boundary language and reject automation/destructive wording. No runtime code or database access changes.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `docs/deployment.md` | Modified | Add backup/restore rehearsal checklist and warning boundaries. |
| `deploy/README.md` | Modified | Reference manual validation order and backup/restore readiness. |
| `tests/test_deployment_docs.py` | Modified | Add static regression guards for docs, placeholders, and no automation. |
| `openspec/specs/deployment-readiness/spec.md` | Modified | Future delta target for tightened requirements. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Placeholder commands are mistaken for production automation | Med | Repeat operator responsibility and no-live-DB boundaries near examples. |
| Static guards become brittle | Med | Assert stable safety boundaries, not exact prose. |
| Scope creeps into restore automation | Low | Keep scripts, app logic, and temp restore fixtures out of this slice. |

## Rollback Plan

Revert documentation, test, and OpenSpec delta changes for this change. No runtime state, database, secrets, servers, or env files are modified.

## Dependencies

- Existing `deployment-readiness` spec and local pytest runner: `py -m pytest`.

## Success Criteria

- [ ] Docs provide manual SQLite backup/restore rehearsal guidance with placeholders only.
- [ ] Static tests fail if guidance touches real DB/env/secrets/servers or adds automation.
- [ ] No implementation, scripts, runtime backup logic, or destructive restore automation is added.
