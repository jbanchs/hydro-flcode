## Exploration: sqlite-backup-restore-readiness

### Current State
HYDRO uses SQLite through `HYDRO_DATABASE_PATH`, defaulting to repo-local `hydro.db` outside production. Production mode already fails closed if the database path is missing, relative, or the default repo DB. Tests set `HYDRO_DATABASE_PATH` to `tests/.tmp_hydro_test.db` and assert `scripts/init_db.py` does not touch `hydro.db`. Deployment docs already require backup/restore decisions and warn that `scripts/init_db.py` is destructive, but the guidance is high-level and intentionally avoids backup scripts. Existing deployment pytest guards cover docs/templates, prohibited deploy/server automation, no real secrets/private hosts, and current SQLite operations wording.

### Affected Areas
- `docs/deployment.md` — Main place to clarify manual SQLite backup/restore rehearsal guidance, safe sample commands, and no-real-DB boundaries.
- `deploy/README.md` — Runtime artifact index and manual validation order should point to backup/restore readiness without implying automation.
- `tests/test_deployment_docs.py` — Existing static guards can enforce docs wording, no automation scripts, no real/private paths, and destructive-restore boundaries.
- `tests/conftest.py` — Already guards test DB isolation; a temp-only backup/restore rehearsal fixture/test could follow this pattern if needed.
- `app/core/config.py` — Defines `HYDRO_DATABASE_PATH` and production fail-closed path expectations; no app change is needed for this slice.
- `app/db/database.py` — Central SQLite connection helper; backup logic should not move here for readiness docs/tests.
- `scripts/init_db.py` — Destructive initializer using `HYDRO_DATABASE_PATH`; docs/tests should keep its production warning prominent.
- `.env.example` and `deploy/env/hydro.env.example` — Placeholder-only runtime templates already include `HYDRO_DATABASE_PATH`; no new real paths should be added.
- `openspec/specs/deployment-readiness/spec.md` — Current requirements already cover backup/restore discipline and no backup scripts; deltas can tighten rehearsal/test-guard expectations.

### Approaches
1. **Docs/checklist only** — Expand deployment docs with a manual backup/restore rehearsal checklist and explicit “do not touch live DB during rehearsal” boundary.
   - Pros: smallest and safest; aligns with existing deployment-doc slice; no destructive behavior or runtime impact.
   - Cons: weak regression protection unless paired with tests; operator could still misread generic guidance.
   - Effort: Low

2. **Pytest static guards** — Add tests that require backup/restore rehearsal wording, placeholder-only command examples, no `backup.sh`/deploy automation, and no live DB restore instruction.
   - Pros: matches existing `tests/test_deployment_docs.py` pattern; prevents wording regressions; does not read secrets or real DB.
   - Cons: guards wording, not operational correctness; regexes must avoid overfitting.
   - Effort: Low

3. **Local non-destructive sample backup command guidance** — Document placeholder SQLite CLI examples using `.backup`/restore shape against operator-selected paths, with service-stop and ownership checks.
   - Pros: gives operators concrete rehearsal shape without repo automation; useful next step from current vague guidance.
   - Cons: command examples can be mistaken as copy/paste production automation unless boundaries are very explicit.
   - Effort: Low

4. **Script wrapper** — Add a repo script to perform backup or restore steps.
   - Pros: repeatable commands and easier local testing.
   - Cons: conflicts with existing “no backup scripts/deploy automation” boundary; restore automation is destructive-risky; likely exceeds smallest safe slice.
   - Effort: Medium

5. **Restore rehearsal fixture using temp SQLite DB only** — Add a pytest test that creates a temp SQLite database, backs it up/restores it locally, and asserts no real DB path is used.
   - Pros: proves Python/SQLite backup mechanics safely; can run under `py -m pytest`; reinforces temp-only discipline.
   - Cons: more than documentation readiness; may imply app-supported restore workflow if not scoped carefully.
   - Effort: Medium

6. **App-level DB backup logic** — Add backup endpoints/services or application-managed backup behavior.
   - Pros: integrated operator feature eventually.
   - Cons: not appropriate now; introduces auth/security/data-loss surface; risks touching production DB paths; outside current readiness boundary.
   - Effort: High

### Recommendation
Proceed with a smallest safe slice combining Approaches 1, 2, and a constrained part of 3: improve `docs/deployment.md`/`deploy/README.md` with manual, placeholder-only SQLite backup and restore rehearsal guidance, and add pytest static guards in `tests/test_deployment_docs.py`. Keep it documentation/test-guard only: no scripts, no app-level backup logic, no real database access, no restore automation, and no changes to `HYDRO_DATABASE_PATH` behavior. Defer the temp-SQLite restore rehearsal fixture unless the proposal explicitly wants executable proof of SQLite mechanics; it is safe if temp-only, but not necessary for the first reviewable slice.

### Risks
- Concrete SQLite command examples could be read as production automation unless every example uses placeholders and repeats operator responsibility.
- Static tests may become brittle if they assert exact prose rather than stable safety boundaries.
- Any restore fixture must be carefully isolated to `tmp_path`; accidental use of `HYDRO_DATABASE_PATH` would violate the no-real-DB requirement.
- Script wrappers or app backup logic would expand scope into destructive operations and should be rejected for this change.

### Ready for Proposal
Yes — propose a docs + pytest static-guard change for SQLite backup/restore readiness. Tell the user the recommended scope is manual rehearsal guidance with placeholder-only sample SQLite CLI shapes and regression guards, explicitly excluding scripts, app backup logic, production DB access, and automated destructive restore.
