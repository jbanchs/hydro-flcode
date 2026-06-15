## Exploration: runtime-config-validation

### Current State
HYDRO already has a small fail-closed session-secret guard in `app/core/config.py`: importing `app.main` requires `HYDRO_SESSION_SECRET` unless `HYDRO_ALLOW_DEV_SECRET=1` is set. Runtime config is otherwise lightweight: `HYDRO_SESSION_COOKIE_SECURE` is parsed as only `"1"` meaning true, `HYDRO_DATABASE_PATH` defaults to repo-local `hydro.db`, and bootstrap admin values are consumed by `scripts/init_db.py`.

Deployment readiness is currently documentation/test guarded rather than executable runtime validated. `.env.example` and `deploy/env/hydro.env.example` share the same placeholder keys, deployment docs explain secret handling and production expectations, and `tests/test_deployment_docs.py` statically checks `.env.example`, docs, deploy templates, no real-looking secrets/private hosts, no deploy automation, `/healthz` liveness wording, and OpenSpec validation guidance. A gap remains: there is no reusable validator that checks both env templates against the app's expected config shape, and there is no operator-facing local command to validate placeholder-only templates before deployment.

### Affected Areas
- `app/core/config.py` — current source of runtime env expectations and session-secret fail-closed behavior; likely home for reusable config-validation rules if app-level checks are added.
- `app/main.py` — imports config during app construction, so stricter startup validation here could block local tests or development if not carefully scoped.
- `scripts/` — best location for a local, non-deploying validator command that can inspect committed templates without touching real env files or servers.
- `.env.example` — primary committed production environment template currently checked only by static pytest guards.
- `deploy/env/hydro.env.example` — deploy-specific env template has the same shape as `.env.example` but is not currently parsed by the existing env assignment helper.
- `docs/deployment.md` and `deploy/README.md` — operator checklist should point to any new local validation command while preserving the no-secrets/no-server/no-automation boundary.
- `tests/test_deployment_docs.py` — existing static guard suite is the natural place to add coverage for template parity, validator behavior, and documentation wording.
- `openspec/specs/deployment-readiness/spec.md` — current source of requirements for placeholder templates, docs, no automation, healthz, local smoke, and validation boundaries.

### Approaches
1. **App-level startup fail-closed checks** — Expand runtime checks so production-like startup fails when secrets, secure cookies, or database path expectations are unsafe.
   - Pros: Protects the actual app process; catches misconfiguration at the point of use.
   - Cons: Hard to infer “production” safely without a new environment-mode variable; could break local tests/imports; may require real env inspection, which is outside this slice's safer placeholder-template focus.
   - Effort: Medium

2. **Local CLI/script validator** — Add a repo-local validator that parses committed env templates and app config expectations, verifies required keys, placeholder-only sensitive values, secure-cookie production default, no dev-secret production value, and parity between `.env.example` and `deploy/env/hydro.env.example`.
   - Pros: Local and testable with `py -m pytest`; gives operators a command before deployment; avoids real secrets and servers; aligns with existing `scripts/` and static guard style.
   - Cons: Validates templates and expectations, not the real target environment; must be clearly documented as pre-deploy/template validation, not readiness or deployment automation.
   - Effort: Low

3. **Pytest-only static guards** — Extend `tests/test_deployment_docs.py` to validate both env templates, required key parity, and docs/checklist wording without adding a standalone operator command.
   - Pros: Smallest code change; follows existing guard pattern; no new user-facing command surface.
   - Cons: Operators still lack an explicit local validation command; validation remains embedded in tests instead of discoverable in deployment docs.
   - Effort: Low

4. **README/deployment checklist only** — Document manual validation steps for template placeholders and runtime expectations.
   - Pros: Very small; no runtime risk.
   - Cons: Weak safeguard; easy to drift from code; does not improve automated local confidence.
   - Effort: Low

5. **No change** — Keep current docs and tests.
   - Pros: No implementation risk.
   - Cons: Leaves deploy env template parity and operator preflight validation gaps unresolved.
   - Effort: None

### Recommendation
Use the smallest safe slice: implement a local, non-deploying `scripts/validate_runtime_config.py` template validator plus pytest coverage and concise docs/checklist updates. Keep app startup behavior unchanged except for possibly reusing constants/helper functions from `app/core/config.py` if that can be done without import-time side effects. This improves production readiness by validating committed placeholder templates and documented expectations locally, while avoiding real secrets, real env files, remote servers, CI billing fixes, and deployment automation.

For review workload, this should fit comfortably under the 400-line budget as one work unit: validator script + tests + docs/spec delta. Chained PR strategy can still be honored, but a single small slice is likely enough unless later design expands into app startup enforcement.

### Risks
- A validator command can be misunderstood as proving the real production environment is safe; docs and spec must state it validates committed templates/preflight expectations only.
- Importing `app.main` or config module carelessly in a validator/test could trigger session-secret startup behavior; prefer pure parsing/helpers or controlled test env setup.
- Overbroad secret/host regexes may create false positives in docs or examples, especially placeholders and URLs intentionally excluded/allowed by existing tests.
- App-level fail-closed production checks need a reliable production-mode signal; adding them prematurely could break local development/tests or create unsafe assumptions.

### Ready for Proposal
Yes — propose a narrowly scoped local runtime config template validator with pytest guards and documentation/spec updates. Tell the user this should not inspect real deployment files, should not connect to servers, should not fix GitHub Actions billing, and should not claim full production readiness.
