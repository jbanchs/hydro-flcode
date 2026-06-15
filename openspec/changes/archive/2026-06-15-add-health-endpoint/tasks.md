# Tasks: Add Health Endpoint

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 180-260 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR / one work-unit commit |
| Delivery strategy | force-chained |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: stacked-to-main
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Add `/healthz` liveness route with tests and deployment docs | PR 1 | Single focused slice under budget; tests/docs included with behavior. |

## Phase 1: RED Tests

- [x] 1.1 Create or update `tests/test_health.py` to assert unauthenticated `GET /healthz` returns 200 and exact `{"status":"ok"}`.
- [x] 1.2 Add `follow_redirects=False` coverage in `tests/test_health.py` proving `/healthz` has no `/login` redirect, auth, CSRF, or session requirement.
- [x] 1.3 Add security-header assertions for `/healthz`: CSP or CSP-Report-Only, `X-Content-Type-Options`, `Referrer-Policy`, and `Permissions-Policy`.
- [x] 1.4 Extend `tests/test_deployment_docs.py` to require `/healthz` liveness wording and reject readiness/database/dependency validation wording.

## Phase 2: GREEN Route Implementation

- [x] 2.1 Create `app/routers/health.py` with a dependency-free `GET /healthz` handler returning static JSON `{"status":"ok"}`.
- [x] 2.2 Modify `app/main.py` to import and include `app.routers.health.router` at the app root with no `/api` prefix or auth dependency.
- [x] 2.3 Run focused pytest targets for health and deployment-doc tests, then keep changes minimal until RED tests pass.

## Phase 3: Docs and Runtime Templates

- [x] 3.1 Update `docs/deployment.md` to document `/healthz` as liveness-only smoke check, not readiness or database validation.
- [x] 3.2 Update `deploy/README.md` with manual post-start/reverse-proxy smoke-check guidance for `/healthz`.
- [x] 3.3 Update `deploy/systemd/hydro.service.example` with a non-executing operator comment referencing `/healthz` after restart.
- [x] 3.4 Update `deploy/caddy/Caddyfile.example` with a placeholder-safe comment that `/healthz` proxies like normal app traffic.

## Phase 4: Verification and Archive Prep

- [x] 4.1 Run `python -m pytest` and confirm health, security-header, and deployment-doc scenarios pass.
- [x] 4.2 Review diff stays under 400 changed lines and keep one work-unit commit with tests and docs together.
- [x] 4.3 Prepare SDD verification evidence and archive notes for `openspec/changes/add-health-endpoint`.
