# Design: Production Deploy Plan

## Technical Approach

Add a non-secret runtime artifact pack under `deploy/` and extend `docs/deployment.md` plus static pytest guards. The pack documents how operators can adapt placeholders for a later production deployment without server access, deploy automation, real secrets, or dependency changes. It follows current HYDRO runtime behavior: FastAPI entrypoint `app.main:app`, direct `uvicorn[standard]`, environment-driven config in `app/core/config.py`, SQLite path from `HYDRO_DATABASE_PATH`, and pytest-based documentation validation.

## Architecture Decisions

| Option | Tradeoff | Decision |
|--------|----------|----------|
| Direct Uvicorn systemd unit | Uses existing dependency and simplest process model; lacks Gunicorn worker management | Use direct `uvicorn app.main:app` because `requirements.txt` already supports it and Gunicorn/multi-worker SQLite behavior is out of scope. |
| Caddy reverse proxy example | Smaller TLS-safe template surface; may not match every operator standard | Provide `deploy/caddy/Caddyfile.example` as the primary example and document Nginx as an alternative to adapt later if the environment standardizes on it. |
| `/etc/hydro/hydro.env` env file | Clear Linux convention; still placeholder-only in Git | Document root/admin-managed file with restrictive permissions; committed file remains `deploy/env/hydro.env.example`. |
| SQLite backup as runbook steps | No executable backup automation; requires operator discipline | Document `sqlite3 .backup`/restore shape using placeholders and service-stop ownership checks; no scripts are added. |

## Data Flow

Operator-managed runtime only; no app code path changes.

    HTTPS client -> Caddy TLS/proxy -> private Uvicorn service -> FastAPI app
                                            |                  |
                                            | EnvironmentFile  -> app/core/config.py
                                            |                  |
                                            +-> SQLite absolute path
                                            +-> journald logs

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `deploy/README.md` | Create | Index for example-only runtime artifacts, scope boundary, and validation order. |
| `deploy/systemd/hydro.service.example` | Create | Placeholder systemd service using non-root `hydro` user, `EnvironmentFile=/etc/hydro/hydro.env`, working directory placeholder, `uvicorn app.main:app`, restart policy, and journald output. |
| `deploy/env/hydro.env.example` | Create | Placeholder-only production env file aligned with `.env.example`; no real values. |
| `deploy/caddy/Caddyfile.example` | Create | Placeholder Caddy reverse proxy/TLS example forwarding to a private app bind target. |
| `docs/deployment.md` | Modify | Link templates; add env placement, service install shape, logs, firewall/TLS checklist, SQLite backup/restore, validation tests, and rollback. |
| `.env.example` | Modify | Keep aligned only if template wording needs `/etc/hydro/hydro.env` guidance; values stay placeholders. |
| `tests/test_deployment_docs.py` | Modify | Include `deploy/` files in secret/private-host scanning and assert required phrases/templates exist. |

## Interfaces / Contracts

No Python API contracts change. Runtime template contract:

```ini
[Service]
User=hydro
Group=hydro
WorkingDirectory=<absolute-application-directory>
EnvironmentFile=/etc/hydro/hydro.env
ExecStart=<venv-python-or-uvicorn> -m uvicorn app.main:app --host <private-bind-host> --port <private-port>
Restart=on-failure
```

`HYDRO_DATABASE_PATH` must be an absolute SQLite path owned by the service user. `HYDRO_SESSION_COOKIE_SECURE=1` is required behind TLS.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit/static | Templates contain placeholders and no secrets/private hosts | Extend `tests/test_deployment_docs.py` regex scanning to `.env.example`, `docs/deployment.md`, and `deploy/`. |
| Integration | Runtime docs align with current config names and Uvicorn dependency | Static assertions for env keys, `uvicorn app.main:app`, `/etc/hydro/hydro.env`, SQLite backup/restore, journald logs, firewall/TLS checklist, and rollback. |
| E2E | Real deployment | Not applicable; no server access or deployment execution in scope. |

## Migration / Rollout

No application migration required. Rollout is documentation/template-only. Before later production use, operators must rotate exposed credentials, create `/etc/hydro/hydro.env` outside Git, verify service-user ownership, take and restore-test a SQLite backup, validate TLS/firewall, run `python -m pytest`, then perform manual smoke checks. Rollback for this change is Git-only; production rollback guidance stops service, restores selected SQLite backup, verifies ownership, restarts service, and checks logs.

## Open Questions

- [ ] None blocking. Real domain, ports, filesystem paths, and proxy standard must be supplied later as sanitized operator inputs.
