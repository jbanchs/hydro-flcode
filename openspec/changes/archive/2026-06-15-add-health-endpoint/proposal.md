# Proposal: Add Health Endpoint

## Intent

Provide a deterministic public liveness URL for manual deployment, systemd, and reverse-proxy smoke checks without exposing secrets or coupling liveness to SQLite readiness.

## Scope

### In Scope
- Add unauthenticated `GET /healthz` returning HTTP 200 with static non-sensitive JSON.
- Keep `/healthz` outside `/api` auth and web login redirect flow while inheriting global security headers.
- Add integration tests for status, body, unauthenticated access, no redirect, and security headers.
- Update deployment docs/runtime template references to use `/healthz` for liveness smoke checks.

### Out of Scope
- Database/readiness checks, `/readyz`, authenticated workflow validation, or service dependency probing.
- Deployment/provisioning automation, CI/CD deploy jobs, or real environment values/secrets.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `deployment-readiness`: Adds a documented public liveness endpoint for deployment smoke checks.
- `browser-security-policy`: Extends security-header expectations to the public liveness response.

## Approach

Implement the smallest safe slice: a dedicated health router mounted by `app/main.py`, returning a tiny static JSON body such as `{ "status": "ok" }`. Do not query SQLite or disclose configuration. Tests prove the endpoint is public, stable, and protected by existing global middleware. Docs describe it as liveness only, not readiness.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `app/main.py` | Modified | Include public health router. |
| `app/routers/health.py` | New | Define `GET /healthz`. |
| `tests/test_api.py` or focused health tests | Modified/New | Cover endpoint behavior and headers. |
| `docs/deployment.md` | Modified | Reference `/healthz` in smoke checks. |
| `deploy/README.md` | Modified | Reference `/healthz` in runtime guidance. |
| `openspec/specs/*` | Modified | Delta specs for deployment readiness and security policy. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Operators mistake liveness for readiness | Medium | Docs/specs explicitly exclude DB/auth workflow validation. |
| Public endpoint exposes operational data | Low | Static response only; no secrets, config, DB, or version data. |
| Endpoint accidentally inherits auth/redirect behavior | Low | Place outside `/api`; test unauthenticated no-redirect access. |

## Rollback Plan

Remove the health router include/file, delete related tests, and revert deployment documentation/spec deltas. No data migration or regulatory citation behavior is affected.

## Dependencies

- Existing FastAPI router pattern and global `SecurityHeadersMiddleware`.
- No external services, DB checks, or new packages.

## Success Criteria

- [ ] `GET /healthz` returns HTTP 200 and static non-sensitive JSON without authentication.
- [ ] `/healthz` does not redirect and is not under `/api` auth.
- [ ] Response includes existing global security headers.
- [ ] Deployment docs/templates reference `/healthz` as liveness, not readiness.
