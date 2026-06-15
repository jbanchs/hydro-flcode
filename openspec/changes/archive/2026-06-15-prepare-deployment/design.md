# Design: Prepare Deployment

## Technical Approach

Implement this change as a documentation/template-only readiness slice. The design adds a placeholder-only environment template and a production deployment runbook that documents existing FastAPI/SQLite behavior without changing runtime code, server state, CI deploy behavior, or secrets. It maps to the proposal by covering HTTPS/reverse proxy expectations, secure cookies, SQLite ownership/backup/rollback, destructive database initialization warnings, and README discoverability.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|----------|--------|-------------------------|-----------|
| Artifact scope | Docs and templates only | Runtime config validation, deploy automation, backup scripts | Matches the proposal's safe first slice and avoids creating executable infrastructure with unverified server assumptions. |
| Process guidance | Document `uvicorn app.main:app` under a process manager such as systemd | Add Gunicorn or checked-in unit files | `requirements.txt` already includes `uvicorn[standard]`; Gunicorn/process templates are out of scope and would require dependency/runtime decisions. |
| TLS boundary | Reverse proxy owns HTTPS/TLS/HSTS/firewall guidance at documentation level | App-level TLS or HSTS changes | Existing app exposes `HYDRO_SESSION_COOKIE_SECURE`; reverse proxy hardening can be documented without code changes. |
| SQLite operations | Manual backup/restore/rollback checklist | Automated backup script or migration tooling | Current database layer uses a direct SQLite path and no migration framework; manual docs are safer for this slice. |

## Data Flow

Deployment readiness information flows from committed templates/docs to the future operator, who supplies secrets outside Git and configures the process manager/reverse proxy manually.

```text
.env.example ──→ operator-owned env file ──→ systemd/process manager ──→ uvicorn app.main:app
docs/deployment.md ──→ manual checklist ──→ reverse proxy/TLS + SQLite backup discipline
README.md ──→ link/discovery ──→ deployment runbook
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `.env.example` | Create | Placeholder-only env template for `HYDRO_SESSION_SECRET`, `HYDRO_DATABASE_PATH`, `HYDRO_SESSION_COOKIE_SECURE`, optional bootstrap admin values, and dev-only fallback warnings. |
| `docs/deployment.md` | Create | Manual readiness runbook covering secret handling, production env decisions, systemd/process-manager guidance, reverse proxy/TLS/firewall expectations, SQLite backup/restore/rollback, health checks, and destructive init warning. |
| `README.md` | Modify | Add a short Deployment Readiness section linking to `docs/deployment.md` and `.env.example`; state this is not deployment automation. |
| `tests/test_deployment_docs.py` | Create | Documentation guard tests verifying placeholders only, required env keys, destructive init warning, backup/rollback language, HTTPS/secure-cookie guidance, and README links. |

## Interfaces / Contracts

No Python interfaces change. The documented environment contract is:

```text
HYDRO_SESSION_SECRET=<required long random secret outside Git>
HYDRO_DATABASE_PATH=<absolute production SQLite path owned by service user>
HYDRO_SESSION_COOKIE_SECURE=1
HYDRO_BOOTSTRAP_ADMIN_USERNAME=<optional initial admin username>
HYDRO_BOOTSTRAP_ADMIN_PASSWORD=<optional one-time bootstrap password outside Git>
HYDRO_ALLOW_DEV_SECRET=<local development only; do not set in production>
```

Docs must use placeholders only, no hostnames/IPs/passwords/keys from private notes, and must not read or reference `specs/DEPLOY_INFO.md`.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Documentation content invariants | Add pytest file-content checks for required env names, placeholder-only examples, and absence of obvious secret values. |
| Integration | Existing app behavior unaffected | Run `py -m pytest` locally; no app code changes expected. CI continues to use `python -m pytest` per `openspec/config.yaml`. |
| E2E | Manual deployment checklist clarity | No browser E2E tooling; docs include manual validation commands/checklist only. |

## Migration / Rollout

No migration required. Rollout is a docs-only PR. Future deployment remains blocked until real credentials are rotated, secrets are supplied outside Git, and an operator performs a manual readiness review.

Rollback is reverting `.env.example`, `docs/deployment.md`, README link changes, docs tests, and this OpenSpec change; no runtime, data, server, or CI deployment state changes.

## Open Questions

- [ ] None blocking.
