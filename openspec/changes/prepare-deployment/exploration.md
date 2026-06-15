## Exploration: prepare-deployment

### Current State
HYDRO is a small FastAPI/Jinja2/SQLite app with local-run instructions only. Runtime configuration is environment-variable based (`HYDRO_SESSION_SECRET`, `HYDRO_DATABASE_PATH`, `HYDRO_SESSION_COOKIE_SECURE`, optional bootstrap admin credentials), but there is no committed `.env.example`, production configuration guide, process manager unit, reverse proxy/TLS guidance, backup/rollback checklist, or migration strategy. The app already has important browser hardening: HTTP-only Starlette session cookies, `SameSite=Lax`, configurable Secure cookies, CSRF for login/logout, Argon2 password hashing, and same-origin CSP/security headers. CI runs pytest only and explicitly excludes deployment/quality gates.

Sensitive deployment access notes exist in ignored `specs/DEPLOY_INFO.md`; this file was deliberately not read. Deployment must not proceed until exposed server passwords are rotated and secrets are moved out of repo notes into an appropriate secret-management workflow.

### Affected Areas
- `README.md` — currently documents local setup and security headers, but lacks production deployment/readiness guidance.
- `.gitignore` — already ignores `.env`, `.env.*`, databases, archives, and `specs/DEPLOY_INFO.md`; an allowlist exists for `.env.example`.
- `requirements.txt` — includes `uvicorn[standard]` but no `gunicorn`; production docs must either use direct `uvicorn` under systemd or add Gunicorn in a later implementation slice.
- `app/core/config.py` — central environment configuration; production readiness should document required env vars and safe values rather than embedding secrets.
- `app/main.py` — session cookie security depends on `HYDRO_SESSION_COOKIE_SECURE=1` behind HTTPS.
- `app/db/database.py` — SQLite path is configurable, but there is no production path convention, backup guidance, or migration mechanism.
- `scripts/init_db.py` — destructive initialization drops and recreates tables; production docs must warn against running it over a live database without backup/restore intent.
- `app/core/security_headers.py` — CSP and security headers are production-friendly for same-origin assets, but TLS/HSTS is not handled at app level.
- `.github/workflows/ci.yml` / `tests/test_ci_workflow.py` — CI only runs pytest with test env vars and intentionally has no deploy job.
- `openspec/config.yaml` / `openspec/specs/browser-security-policy/spec.md` — existing SDD context confirms FastAPI/SQLite architecture and browser security requirements.

### Approaches
1. **Documentation and templates only** — Add deployment-readiness docs/checklists and a committed `.env.example` with placeholders; do not touch server, secrets, runtime code, or CI deployment.
   - Pros: smallest safe slice; avoids exposing secrets; gives repeatable production prep; fits forced chained PR budget; can explicitly require password rotation before any deploy.
   - Cons: does not enforce production config at runtime; no automated deploy or backup implementation yet.
   - Effort: Low

2. **Runtime hardening plus docs** — Add production config validation, optional HSTS/proxy settings, `.env.example`, and deployment docs.
   - Pros: converts some guidance into enforceable guardrails; reduces chance of insecure production startup.
   - Cons: larger review slice; requires tests; may block local/dev workflows if not carefully scoped.
   - Effort: Medium

3. **Full deployment automation** — Add systemd/nginx templates, backup scripts, migration tooling, CI/CD deploy job, and server provisioning notes.
   - Pros: more complete operational pathway.
   - Cons: too risky for first slice; may touch server assumptions; higher chance of secret leakage; exceeds exploration/prep scope.
   - Effort: High

### Recommendation
Proceed with Approach 1 as the smallest safe first slice: create a deployment preparation proposal focused on non-secret docs/config templates only. The slice should add `.env.example` with placeholders, production deployment documentation covering systemd + direct `uvicorn` first, reverse proxy/TLS expectations, `HYDRO_SESSION_COOKIE_SECURE=1`, non-root service user, firewall, SQLite production path/backup/restore guidance, destructive `init_db.py` warning, rollback checklist, and secret-handling rules. Do not deploy, do not read or copy `specs/DEPLOY_INFO.md`, do not add CI deploy jobs, and do not include real hostnames, usernames, passwords, IPs, or keys.

Prefer direct `uvicorn app.main:app` under systemd for the first documented path because `uvicorn[standard]` is already in `requirements.txt`. If process-management requirements grow, evaluate adding Gunicorn as a separate implementation slice with dependency/test/docs changes.

### Risks
- Existing server credentials were reportedly exposed in a local ignored file; passwords must be rotated before any deployment.
- Running `scripts/init_db.py` against a live production SQLite database would drop existing tables and data.
- SQLite deployment needs explicit file ownership, backup, restore, and upgrade discipline; no migration tooling exists yet.
- Secure cookies require HTTPS and `HYDRO_SESSION_COOKIE_SECURE=1`; setting this incorrectly can either weaken production cookies or break login over non-HTTPS local testing.
- Reverse proxy/TLS/HSTS/firewall choices are currently undocumented and can easily drift if handled manually.
- No automated deployment rollback or health check exists; first deployment must stay manual and checklist-driven.

### Ready for Proposal
Yes — propose a documentation/template-only deployment preparation slice. Tell the user this prepares HYDRO for a future safe deployment without touching the server, and deployment itself remains blocked until secrets are rotated and production credentials are supplied through a secure channel outside the repository.
