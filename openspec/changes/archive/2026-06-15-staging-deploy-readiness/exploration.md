## Exploration: staging-deploy-readiness

### Current State
HYDRO already has a strong repo-local deployment readiness base: placeholder-only env templates, deployment/runtime docs, systemd and Caddy examples, production-mode fail-closed checks, `/healthz` liveness, local browser smoke coverage, SQLite backup/restore readiness guidance, OpenSpec deployment-readiness requirements, and pytest guards that keep validation local and non-secret. CI workflow exists and runs pytest, but GitHub Actions execution is treated as deferred/external when billing is blocked. No staging-specific readiness runbook or dry-run checklist currently ties these existing pieces into a first staging deployment/MVP validation path.

### Affected Areas
- `docs/deployment.md` — main manual readiness runbook; best location for staging preflight/dry-run and first validation guidance.
- `deploy/README.md` — runtime artifact index and manual validation order; can point to staging readiness without adding automation.
- `.env.example` and `deploy/env/hydro.env.example` — placeholder-only runtime templates; may need staging-safe guidance but must avoid real hosts/secrets.
- `scripts/validate_runtime_config.py` — existing local template validator; should remain template-only and non-deploying.
- `tests/test_deployment_docs.py` — static guard pattern for docs/templates, automation boundaries, placeholder-only values, backup/restore wording, and OpenSpec guidance.
- `tests/test_production_config.py` — verifies `HYDRO_ENV=production` behavior; relevant if staging uses production-mode settings for deployment rehearsal.
- `tests/test_health.py` and `tests/test_local_browser_smoke.py` — existing repo-local smoke confidence for `/healthz`, HTML, static assets, auth flow, and security headers.
- `.github/workflows/ci.yml` and `tests/test_ci_workflow.py` — CI exists as pytest-only but remote CI gating remains deferred.
- `openspec/specs/deployment-readiness/spec.md` — source-of-truth requirements and boundaries for non-secret deployment readiness.

### Approaches
1. **Docs/checklist only** — Add staging readiness guidance to existing deployment docs.
   - Pros: Smallest change; no runtime risk; keeps servers/secrets untouched.
   - Cons: Easy to regress without tests; relies on operator discipline.
   - Effort: Low

2. **Pytest static guards** — Add tests that enforce staging guidance, placeholder-only examples, no server access, no deploy automation, and local validation wording.
   - Pros: Fits current strict TDD pattern; protects boundaries over time.
   - Cons: More implementation than docs-only; regex guards can be brittle if wording drifts.
   - Effort: Low/Medium

3. **Staging env template variant** — Add a dedicated staging placeholder env example.
   - Pros: Makes staging preparation concrete.
   - Cons: Risks duplicating template parity rules; may confuse production-mode expectations unless tightly documented.
   - Effort: Medium

4. **Dry-run checklist** — Document a repo-local dry run: `py scripts/validate_runtime_config.py`, `py -m pytest`, review templates, rehearse backup/restore decisions with placeholders, and list operator-owned staging checks.
   - Pros: Bridges local confidence to staging without touching servers; aligns with existing docs/tests.
   - Cons: Still manual; cannot prove real staging readiness.
   - Effort: Low

5. **Manual staging validation runbook** — Add first staging/MVP validation steps for a human operator after they deploy out-of-band: `/healthz`, `/login`, authenticated `/`, Ask HYDRO citation behavior, logs, rollback and backup confirmation.
   - Pros: Gives the operator a safe path for first staging validation; separates repo-local prep from out-of-band deployment.
   - Cons: Must be explicit that the repo does not perform deployment or inspect secrets.
   - Effort: Low/Medium

6. **Deployment script** — Add executable deploy or predeploy automation.
   - Pros: Could reduce manual steps later.
   - Cons: Out of scope now; risks server/secrets access and review expansion.
   - Effort: High

7. **CI gate** — Require remote GitHub Actions as a staging gate.
   - Pros: Useful once CI is available.
   - Cons: Deferred by current constraints; not safe to make mandatory while billing/account state is external.
   - Effort: Medium

8. **Real server deploy** — Perform or document real server-specific deployment.
   - Pros: Validates real environment.
   - Cons: Explicitly out of scope; would touch servers/secrets and violate the change boundary.
   - Effort: High

### Recommendation
Use the smallest safe slice: combine **docs/checklist**, **dry-run checklist**, **manual staging validation runbook**, and **pytest static guards**. Do not add deploy scripts, CI deploy gates, server probes, or real staging values. Keep staging readiness as a non-secret, repo-local handoff: maintainers prove local confidence with `py scripts/validate_runtime_config.py` and `py -m pytest`, then an operator performs any staging deployment out-of-band and validates with documented manual checks.

Avoid a separate staging env template unless proposal/spec discovers a concrete operator need. Existing templates can cover staging by describing placeholder-only target-environment values and requiring production-like safety settings when staging is meant to rehearse production behavior.

### Risks
- Wording could accidentally imply complete staging readiness or deployment automation instead of repo-local preparation.
- Static guards may become over-specific if they assert exact prose rather than critical boundary concepts.
- Staging guidance could conflict with `HYDRO_ENV=production` semantics if it suggests `HYDRO_ENV=staging`; the safer default is production-like staging config for deployment rehearsal, with no new runtime mode.
- Operators may over-trust `/healthz`; docs must repeat that it is liveness-only and not DB/readiness/auth validation.

### Ready for Proposal
Yes — propose a documentation-and-static-guard change that creates a staging readiness handoff/runbook, keeps all values placeholder-only, preserves local-only validation boundaries, and explicitly excludes deploy scripts, CI deployment gates, server access, real secrets, and real deployment execution.
