# Proposal: Production Mode Signal

## Intent

Introduce an explicit `HYDRO_ENV=production` runtime signal so HYDRO can fail closed on production-only misconfiguration without changing dev/test behavior when the signal is unset.

## Scope

### In Scope
- Add exact-match production mode detection for `HYDRO_ENV=production`.
- Add production-only startup/config checks for real session secret presence, secure cookies, disabled dev secret allowance, and explicit safe database path expectations supported by current config design.
- Update tests, env templates, deployment docs, and local template validation expectations without reading real env files.

### Out of Scope
- Real `.env` reads, secret inspection, server checks, deploy automation, GitHub Actions, TLS validation, or file ownership checks.
- Changing dev/test startup behavior unless production mode is explicitly set.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `deployment-readiness`: Add reliable production-mode signal and replace deferred startup fail-closed expansion with narrow production-only runtime checks.

## Approach

Implement production-mode parsing and fail-closed checks in `app/core/config.py`, then invoke them during app construction before serving requests. Only normalized exact `production` enables checks. Keep template validation local/template-only, and document placeholders plus operational boundaries.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `app/core/config.py` | Modified | Production parser and fail-closed checks. |
| `app/main.py` | Modified | Trigger checks during app construction. |
| `tests/` | Modified | Isolated production-mode and template guard coverage. |
| `.env.example`, `deploy/env/hydro.env.example` | Modified | Add `HYDRO_ENV` placeholder guidance. |
| `scripts/validate_runtime_config.py` | Modified | Template parity only; no real env reads. |
| `docs/deployment.md`, `deploy/README.md` | Modified | Operator guidance and boundaries. |
| `openspec/specs/deployment-readiness/spec.md` | Modified | Delta requirements for signal/checks. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Production env leaks into tests | Med | Clear/control `HYDRO_ENV` in pytest setup and targeted tests. |
| Ambiguous aliases like `prod` | Low | Support only exact normalized `production`; document unsupported aliases. |
| Validator scope creep | Med | Preserve template-only tests and docs boundary. |

## Rollback Plan

Unset or change `HYDRO_ENV` away from `production` to restore current startup behavior, then revert the code/docs/spec/template changes if needed. No data migration is involved.

## Dependencies

- Existing deployment-readiness capability and current config/session middleware startup path.

## Success Criteria

- [ ] Production mode fails startup when session secret is missing, secure cookies are disabled, dev secret is allowed, or DB path is unsafe/default.
- [ ] Dev/test behavior remains unchanged when `HYDRO_ENV` is unset or non-production.
- [ ] Templates/docs/specs describe `HYDRO_ENV=production` without secrets or deploy automation.
