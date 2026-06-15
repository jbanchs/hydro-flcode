## Exploration: production-deploy-plan

### Current State
HYDRO is a FastAPI/Jinja2/SQLite app with environment-driven runtime settings. `requirements.txt` includes `uvicorn[standard]` but not Gunicorn, so the current executable runtime path is direct `uvicorn app.main:app`. Production readiness is currently documentation/template-only: `.env.example`, `docs/deployment.md`, and the archived `prepare-deployment` change cover placeholders, non-root execution, reverse proxy/TLS expectations, firewall posture, SQLite ownership/backups, and the destructive `scripts/init_db.py` warning. There are no committed systemd units, reverse-proxy templates, deploy scripts, service-user setup snippets, backup scripts, or production smoke-check artifacts.

### Affected Areas
- `docs/deployment.md` — Existing deployment runbook; would be extended or linked from any runtime artifact guidance.
- `.env.example` — Existing placeholder-only production environment template; should remain secret-free and may inform systemd `EnvironmentFile` examples.
- `requirements.txt` — Contains `uvicorn[standard]` only; adding Gunicorn would be a dependency/runtime decision, not just documentation.
- `app/core/config.py` — Defines `HYDRO_SESSION_SECRET`, `HYDRO_DATABASE_PATH`, `HYDRO_SESSION_COOKIE_SECURE`, and dev-secret behavior that runtime templates must respect.
- `app/main.py` — Starlette session cookie security depends on `HYDRO_SESSION_COOKIE_SECURE=1` behind TLS.
- `app/db/database.py` — SQLite path is resolved at runtime; service user and filesystem permissions matter.
- `scripts/init_db.py` — Drops and recreates tables; production plans must avoid running it on live data without explicit backup/restore acceptance.
- `openspec/specs/deployment-readiness/spec.md` — Current source-of-truth requirements are readiness documentation only; runtime/service artifacts need a new delta spec.
- `.github/workflows/ci.yml` / `tests/test_ci_workflow.py` — CI runs `python -m pytest` only; deploy automation should not be introduced in this first slice.

### Approaches
1. **Manual runtime artifact pack** — Add checked-in examples/templates for a systemd service, environment-file placement, reverse proxy config, SQLite backup/restore checklist, and smoke-check runbook; do not connect to the server or include real hostnames/secrets.
   - Pros: Smallest safe improvement beyond docs; gives operators concrete files to adapt; can be tested with static guard tests; stays under the 400-line review budget if split carefully.
   - Cons: Still not deploy automation; templates may need later adjustment once rotated credentials and real server paths are available.
   - Effort: Medium

2. **One-shot deploy script/runbook automation** — Add a script to create users/directories, copy files, install dependencies, configure services/proxy, and restart HYDRO.
   - Pros: Reduces manual operator steps later; can encode ordering and safety checks.
   - Cons: Too risky before credential rotation and server validation; host-specific assumptions can leak into Git; harder to test without server access; likely exceeds safe first-slice scope.
   - Effort: High

3. **Gunicorn-based production runtime** — Add Gunicorn dependency and document/run `gunicorn -k uvicorn.workers.UvicornWorker app.main:app` under systemd.
   - Pros: Familiar production process model; multiple worker management if the app grows.
   - Cons: Adds a new dependency and tuning surface; SQLite write behavior plus multiple workers needs deliberate validation; direct Uvicorn is already supported and simpler.
   - Effort: Medium

4. **Reverse-proxy-first template only** — Add Nginx or Caddy examples plus TLS/firewall checklist, leaving systemd/database/logging to prose.
   - Pros: Narrow slice; improves TLS and secure-cookie clarity.
   - Cons: Incomplete deployment plan because process management, env placement, SQLite permissions, logs, and backup discipline remain vague.
   - Effort: Low

### Recommendation
Proceed with Approach 1 as the smallest safe first slice: create a proposal/spec/design for a **non-secret production runtime artifact pack**. It should add example-only templates and documentation for direct `uvicorn app.main:app` under systemd, a root-owned/restricted environment file path such as `/etc/hydro/hydro.env`, a non-root `hydro` service user, an absolute SQLite path under an operator-owned data directory, journald/systemd log handling, pre-release SQLite backup/restore checks, and one reverse-proxy example. Prefer **Caddy** if the goal is smallest TLS-safe template surface, or **Nginx** if the target operator already standardizes on Nginx; absent server details, keep the proxy artifact explicitly example-only and placeholder-based.

Do not add a one-shot deploy script yet. Keep any implementation as templates plus static tests/docs guards. Use direct Uvicorn first because it is already in `requirements.txt`; defer Gunicorn until there is a concrete concurrency/process-management requirement and SQLite behavior is reviewed.

Credentials, real hostnames, IPs, server paths, and any private infrastructure details must wait until exposed credentials are rotated and the operator supplies sanitized deployment values. No server access belongs in this change.

### Risks
- Accidentally reading or encoding ignored deployment secrets would contaminate the repo; local ignored deployment secret notes must remain untouched and unnamed in committed artifacts.
- Runtime templates can create false confidence if they are treated as already validated on the real server.
- SQLite with multiple workers/processes needs care; avoid introducing Gunicorn/multi-worker defaults in the first slice.
- `scripts/init_db.py` is destructive; any production initialization guidance must require explicit backup/restore acceptance and avoid live-data execution by default.
- TLS/firewall correctness depends on real infrastructure; keep placeholders and require operator validation after credential rotation.

### Ready for Proposal
Yes — propose a non-secret runtime artifact pack as the next OpenSpec change. The orchestrator should tell the user this is still deployment preparation, not deployment: no server connection, no secrets, no CI/CD deploy job, no one-shot script, and no use of existing exposed credentials until rotation is complete.
