# Proposal: Production Deploy Plan

## Intent

Prepare HYDRO for a later production deployment by adding non-secret runtime templates and operator guidance. This is deployment preparation only: no server access, real secrets, CI/CD deploy jobs, or one-shot automation.

## Scope

### In Scope
- Example systemd service for direct `uvicorn app.main:app` using a non-root service user.
- Environment file placement/template guidance for `/etc/hydro/hydro.env` with placeholders only.
- Reverse proxy template/guidance, TLS/firewall checklist, logging notes, and docs links.
- SQLite absolute data path, ownership, backup/restore, and destructive init warnings.

### Out of Scope
- Reading/copying local ignored deployment secret notes, real credentials, hostnames, IPs, or private paths.
- Server provisioning, SSH access, deployment execution, or one-shot deploy scripts.
- Adding Gunicorn, multi-worker defaults, backup scripts, or CI/CD deploy automation.

## Capabilities

### New Capabilities
None

### Modified Capabilities
- `deployment-readiness`: Expand documentation-only readiness into non-secret production runtime artifact templates and operator checklists.

## Approach

Use the manual runtime artifact pack from exploration: commit example-only templates plus documentation guards. Keep direct Uvicorn because it already exists in `requirements.txt`; defer Gunicorn until concurrency and SQLite behavior are validated. Add static review/test guards where useful to reject secrets and preserve placeholders.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `deploy/` | New | Example systemd/proxy/env templates and runtime notes. |
| `docs/deployment.md` | Modified | Link templates; add operator checklist and rollback guidance. |
| `.env.example` | Modified | Ensure placeholder-only alignment with production env guidance. |
| `openspec/specs/deployment-readiness/spec.md` | Modified | New requirements for runtime artifacts after archive. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Secrets leak into Git | Med | Do not read sensitive deployment info; use placeholders and static guards. |
| Templates imply validated deployment | Med | Mark artifacts example-only and require operator validation. |
| SQLite data loss | Med | Require backup/restore checks; warn against `scripts/init_db.py` on live data. |
| Proxy/TLS mismatch | Low | Keep placeholders and checklist-based validation. |

## Rollback Plan

Revert the proposal/spec/design/task implementation files and remove added template/docs changes. Since no server state, secrets, or database changes are introduced, rollback is Git-only.

## Dependencies

- Existing `uvicorn[standard]` runtime dependency.
- Credential rotation and sanitized deployment values before any real deployment.

## Success Criteria

- [ ] Templates and docs contain placeholders only and no real deployment secrets.
- [ ] Operators can identify service, env file, proxy/TLS, firewall, logs, SQLite path, and backup steps.
- [ ] Scope boundaries explicitly reject server access, deploy automation, and Gunicorn introduction.
