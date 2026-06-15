## Exploration: add-health-endpoint

### Current State
HYDRO is a FastAPI app assembled in `app/main.py` with global `SecurityHeadersMiddleware`, session middleware, static assets, the unauthenticated web router, and the authenticated `/api` router. `/` redirects unauthenticated users to `/login`; `/api/*` is protected through `APIRouter(prefix="/api", dependencies=[Depends(require_user)])`. There is no existing health endpoint. Deployment docs/templates describe manual systemd/reverse-proxy smoke checks but do not yet name a deterministic liveness URL. Security headers are applied globally after responses, so a new route should inherit CSP, nosniff, referrer, and permissions headers without route-specific work.

### Affected Areas
- `app/main.py` — central place where routers are included; likely should include a small public health router.
- `app/routers/` — existing router pattern separates web and `/api`; a new `health.py` router keeps liveness outside auth-protected `/api` and avoids mixing it into Jinja web handlers.
- `tests/test_api.py` — existing FastAPI integration tests cover auth boundaries and security headers; add health assertions here or a focused health test file.
- `app/core/security_headers.py` — no code change expected, but tests should confirm `/healthz` receives current global security headers.
- `docs/deployment.md` and `deploy/README.md` — deployment smoke/runbook text should reference unauthenticated `/healthz` for reverse proxy/systemd/manual checks.
- `openspec/specs/deployment-readiness/spec.md` — likely domain for the delta because the endpoint supports production deployment validation.

### Approaches
1. **Minimal liveness endpoint** — Add unauthenticated `GET /healthz` returning a tiny static JSON body such as `{ "status": "ok" }` with HTTP 200, no database/service checks, and no secrets or regulatory data.
   - Pros: smallest safe production slice; verifies ASGI app process, routing, middleware, and reverse-proxy path; avoids SQLite lock/latency concerns; safe to expose unauthenticated.
   - Cons: does not prove database availability or full application readiness; operators must still inspect logs and perform authenticated smoke for deeper confidence.
   - Effort: Low

2. **Readiness endpoint with SQLite check** — Add `GET /readyz` or make `/healthz` query SQLite before returning 200.
   - Pros: catches missing/unreadable database and some startup/configuration failures.
   - Cons: higher coupling to database path and schema; unauthenticated endpoint could expose operational state; SQLite checks can add lock/latency noise; less minimal for current deployment need.
   - Effort: Medium

3. **Authenticated/API health endpoint** — Place health under `/api/health` or require login.
   - Pros: preserves the existing `/api` auth boundary and limits public surface.
   - Cons: poor fit for reverse proxy, systemd, and unauthenticated manual liveness checks; requires session/login setup just to determine if the process is alive.
   - Effort: Low

### Recommendation
Proceed with Approach 1: an unauthenticated `GET /healthz` liveness endpoint implemented as a dedicated small router outside the `/api` prefix. It should return HTTP 200 and a minimal JSON body only, avoid database checks and environment/config disclosure, inherit existing security headers, and be documented as liveness rather than full readiness. Tests should prove `/healthz` works without login, does not redirect, does not require `/api` auth, emits the expected minimal body, and includes the global security headers. Deployment docs should use `/healthz` as the post-start/reverse-proxy smoke URL while keeping SQLite backup/ownership/log checks separate.

### Risks
- Operators may overinterpret liveness as readiness; docs/spec should explicitly state `/healthz` does not validate SQLite, credentials, regulatory data, or authenticated workflows.
- A public endpoint slightly increases exposed surface; keep response static and non-sensitive.
- If added to the wrong router (`/api` or web template flow), auth/redirect behavior could make it unsuitable for systemd/reverse proxy checks.

### Ready for Proposal
Yes — tell the user the smallest safe slice is a public `/healthz` liveness endpoint with static non-sensitive JSON, global security headers, integration tests, and deployment doc/runbook references; defer DB-backed readiness to a later explicit change if needed.
