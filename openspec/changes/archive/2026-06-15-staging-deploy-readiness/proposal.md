# Proposal: Staging Deploy Readiness

## Intent

Create a safe, repo-local handoff for first staging/MVP validation without deploying, touching servers, reading secrets, or changing runtime modes. Staging is production-like validation using `HYDRO_ENV=production` with staging-specific secret values supplied outside Git.

## Scope

### In Scope
- Add docs/checklist guidance for staging preflight and dry-run validation.
- Add a manual staging validation runbook for an operator after out-of-band deployment.
- Add pytest static guards for staging wording, placeholder-only values, and prohibited scope expansion.

### Out of Scope
- Deployment execution, server access, scripts, SSH, probes, or provisioning.
- Secrets, real env files, `hydro.db`, ignored sensitive notes, or real staging values.
- CI gate changes, CI billing fixes, deploy jobs, or `HYDRO_ENV=staging`.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `deployment-readiness`: Add staging dry-run/runbook requirements while preserving local-only, placeholder-only, non-deploying boundaries.

## Approach

Update existing deployment-readiness documentation and tests only. Document a local dry run using existing validation (`py scripts/validate_runtime_config.py`, `py -m pytest`) and a manual post-deploy checklist for `/healthz`, `/login`, authenticated `/`, Ask HYDRO citation behavior, logs, rollback, and backup confirmation. Static guards should assert concepts, not brittle exact prose.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `docs/deployment.md` | Modified | Add staging preflight, dry-run, and manual validation runbook. |
| `deploy/README.md` | Modified | Link staging readiness into runtime artifact order. |
| `tests/test_deployment_docs.py` | Modified | Guard staging boundaries and required wording. |
| `openspec/specs/deployment-readiness/spec.md` | Modified | Later delta spec should add staging readiness requirements. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Docs imply real deployment readiness | Med | State repo-local handoff and operator-owned deployment boundary. |
| `HYDRO_ENV=staging` confusion | Med | Explicitly require `HYDRO_ENV=production` for production-like staging validation. |
| Static guards become brittle | Med | Assert boundary concepts over exact paragraphs. |

## Rollback Plan

Revert the documentation, OpenSpec delta, and pytest guard changes. No runtime, server, database, CI, or secret state is changed.

## Dependencies

- Existing deployment-readiness docs, runtime templates, validator, and pytest suite.
- Operator supplies staging secrets/config outside Git after this repo-local slice.

## Success Criteria

- [ ] Maintainers can follow a local dry-run checklist without secrets or server access.
- [ ] Operators have a manual staging validation runbook after out-of-band deployment.
- [ ] Pytest guards fail on `HYDRO_ENV=staging`, deploy automation, server access, real env/secret reads, or `hydro.db` access.
