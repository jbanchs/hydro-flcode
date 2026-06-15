# Design: Add Health Endpoint

## Technical Approach

Add a minimal FastAPI router at the app root for `GET /healthz`. Mount it in `app/main.py` outside the `/api` router so it bypasses `Depends(require_user)` and outside the web home route so it cannot redirect to `/login`. Keep the response static and dependency-free: no SQLite, config, version, host, or environment data. The route still passes through `SecurityHeadersMiddleware` because middleware wraps the whole FastAPI app.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Route placement | Create `app/routers/health.py` and include it from `app/main.py` with no prefix | Add to `web.py`; add under `/api`; inline in `main.py` | A dedicated root router follows existing router style while avoiding web redirects and API auth dependencies. |
| Response schema | Return `{"status": "ok"}` with HTTP 200 | Include DB state, app version, uptime, environment, hostname | Liveness must be deterministic and non-sensitive; readiness and dependency checks are explicitly out of scope. |
| Auth behavior | No route-level dependency and no session check | Reuse API auth; special-case auth middleware | Existing auth is router-level for `/api` and explicit in web handlers, so an independent router is the smallest bypass. |
| Security headers | Rely on existing global `SecurityHeadersMiddleware`; do not add route-specific headers | Duplicate headers in handler; exempt `/healthz` | Middleware already applies headers app-wide through `app.add_middleware`, and tests should preserve that contract. |
| Delivery split | One small work unit containing route, tests, docs/templates | Separate tests/docs/code PRs | Under 400 lines expected; tests and docs belong with the behavior they validate/explain. |

## Data Flow

```text
GET /healthz
  -> FastAPI app middleware stack
  -> health router handler
  -> JSONResponse {"status":"ok"}
  -> SecurityHeadersMiddleware adds global headers
```

No database, session, service, or regulation retrieval flow is touched.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `app/routers/health.py` | Create | Define public `GET /healthz` route returning static JSON. |
| `app/main.py` | Modify | Import and include `health.router` before/alongside existing routers. |
| `tests/test_api.py` or `tests/test_health.py` | Modify/Create | Assert status 200, exact JSON, unauthenticated access, no redirect, and security headers. |
| `docs/deployment.md` | Modify | Document `/healthz` as liveness-only smoke check, not readiness. |
| `deploy/README.md` | Modify | Add manual validation guidance for `/healthz`. |
| `deploy/systemd/hydro.service.example` | Modify | Add non-executing comment/reference for operator liveness smoke check after restart. |
| `deploy/caddy/Caddyfile.example` | Modify | Add placeholder-safe comment that `/healthz` should proxy like normal app traffic. |

## Interfaces / Contracts

```http
GET /healthz
200 OK
Content-Type: application/json

{"status":"ok"}
```

Contract constraints: unauthenticated; no redirect; no cookies required; no SQLite calls; no secret/config/version disclosure; includes existing `Content-Security-Policy`, `X-Content-Type-Options`, `Referrer-Policy`, and `Permissions-Policy` headers.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Handler response shape if isolated test is useful | Direct FastAPI `TestClient` request is enough; no separate service unit needed. |
| Integration | Public endpoint behavior and middleware | `TestClient(app, follow_redirects=False).get("/healthz")`; assert 200, `{"status":"ok"}`, no `location`, no auth setup, global headers. |
| Docs/runtime | Deployment docs and runtime templates mention liveness safely | Extend `tests/test_deployment_docs.py` to require `/healthz`, liveness-only wording, and no private host/automation patterns. |
| E2E | Not applicable | No E2E tool is configured in OpenSpec testing capabilities. |

Run `python -m pytest`.

## Migration / Rollout

No data migration required. Roll out with the app release, then operators may use `/healthz` for manual post-start, reverse-proxy, and rollback smoke checks. Rollback is removing the router include/file and reverting tests/docs/template references; no persisted data is affected.

## Open Questions

None.
