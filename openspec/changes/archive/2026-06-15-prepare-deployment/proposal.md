# Proposal: Prepare Deployment

## Intent

Prepare HYDRO for a future safe production deployment by documenting required configuration, operational checks, and rollback practices without touching servers, exposing secrets, or adding deployment automation.

## Scope

### In Scope
- Add committed `.env.example` with placeholders only.
- Add deployment checklist/runbook for manual readiness review.
- Document production config guidance: HTTPS, secure cookies, SQLite path/ownership, service user, firewall, and reverse proxy/TLS expectations.
- Document backup/restore and rollback notes for SQLite deployments.
- Warn that `scripts/init_db.py` is destructive and must not run against live production data without backup/restore intent.
- State that real secrets stay out of Git and exposed credentials must be rotated before deployment.

### Out of Scope
- Server access, real hostnames, usernames, passwords, IPs, keys, or copied secrets.
- Deployment automation, CI/CD deploy jobs, provisioning, or process-manager units as executable infrastructure.
- Runtime hardening changes, Gunicorn adoption, migrations, or backup scripts.

## Capabilities

### New Capabilities
- `deployment-readiness`: Documents safe deployment preparation, environment templates, secret handling, production config, backup, and rollback expectations.

### Modified Capabilities
- None.

## Approach

Use the exploration recommendation: keep this first slice documentation/template-only. Add placeholders and operational guidance for direct `uvicorn app.main:app` under a process manager, reverse proxy/TLS handled outside the app, `HYDRO_SESSION_COOKIE_SECURE=1` behind HTTPS, and SQLite backup discipline. Do not read ignored secret notes.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `.env.example` | New | Placeholder-only environment template. |
| `README.md` or deployment docs | Modified/New | Production readiness checklist and runbook links/content. |
| `scripts/init_db.py` | Referenced | Document destructive behavior; no code change required. |
| `openspec/specs/deployment-readiness/spec.md` | New | Future capability spec created by sdd-spec. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Secrets leak into docs | Med | Use placeholders only; never read the ignored local deployment secret note; state real secrets stay out of Git. |
| Operator runs destructive DB init | Med | Prominent warning and backup/restore checklist. |
| Docs imply deployment is complete | Low | Clearly label as readiness-only; no server access or automation. |

## Rollback Plan

Revert the documentation/template changes and the OpenSpec change artifacts. No runtime, data, server, or CI deployment state is changed.

## Dependencies

- Existing FastAPI/SQLite config behavior in `app/core/config.py` and `app/db/database.py`.
- Production deployment remains blocked until exposed credentials are rotated and secrets are provided outside Git.

## Success Criteria

- [ ] `.env.example` contains placeholders only and no real secrets.
- [ ] Deployment docs cover production config, backup, rollback, and destructive init warnings.
- [ ] Docs explicitly exclude server access, automation, and real credentials from this slice.
