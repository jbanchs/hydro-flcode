# Proposal: Staging Server Bootstrap

## Intent

Add a repo-local, documentation/spec/test slice for manual staging server bootstrap prerequisites before any deployment work. The audit facts to reflect are Ubuntu 22.04, `apt`, `systemctl`, passworded `sudo`, Python 3.10, missing `git`/Caddy/`sqlite3`, 20G disk, and 2GiB RAM.

## Scope

### In Scope
- Document a manual operator checklist for minimal prerequisites: `git`, `python3-venv`, and `sqlite3`.
- Document verification checklist for Python, venv, git, sqlite3, systemd, apt, sudo, disk, and memory.
- Update OpenSpec delta and local pytest static guards for bootstrap boundaries.

### Out of Scope
- Server access, SSH/SCP commands, deployment, scripts, CI changes, secrets/passwords, real env/db reads.
- Caddy/systemd configuration, firewall/TLS exposure, app startup, database initialization.
- Caddy install/configure work; Caddy remains deferred unless later approved as package-only and unconfigured.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `deployment-readiness`: Add manual staging server bootstrap prerequisites and verification checklist while preserving no-server/no-automation boundaries.

## Approach

Follow the exploration recommendation: docs/checklist only. Update deployment docs and artifact index with placeholder-only, operator-run guidance; add a deployment-readiness delta; extend static tests to prevent scope creep and require target audit facts.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `docs/deployment.md` | Modified | Add manual bootstrap prerequisites and verification checklist. |
| `deploy/README.md` | Modified | Link/index bootstrap checklist if needed. |
| `tests/test_deployment_docs.py` | Modified | Guard required wording and prohibited scope. |
| `openspec/changes/staging-server-bootstrap/specs/deployment-readiness/spec.md` | New | Delta requirement for bootstrap checklist. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Apt guidance reads as automation | Med | Label as manual operator-run only; no scripts or remote commands. |
| Caddy implies public ingress readiness | Med | Defer Caddy configuration/install from this slice. |
| Python 3.10 may not satisfy app runtime | Med | Document as audit fact, not compatibility approval. |
| Passworded sudo leaks credentials | Low | State password is entered interactively and never recorded. |

## Rollback Plan

Revert the docs, test guard, and OpenSpec delta changes for this change folder; no server, CI, secrets, runtime, or deployment state is modified.

## Dependencies

- Existing deployment-readiness docs/spec and local pytest runner `py -m pytest`.

## Success Criteria

- [ ] Checklist includes all audited facts and minimal packages without deploying HYDRO.
- [ ] Tests fail on server access, scripts, Caddy/systemd config, secrets, env/db reads, or CI changes.
