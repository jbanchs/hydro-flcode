# HYDRO Deployment Readiness

This runbook prepares a future production deployment review. It does not deploy HYDRO, provision servers, configure infrastructure, create CI/CD deployment jobs, or add executable deployment automation.

## Scope Boundary

- Use this document as a manual readiness checklist before a later deployment.
- Keep real credentials, host-specific values, tokens, passwords, and private infrastructure notes outside Git.
- Supply production values through the target environment or a secret manager.
- Rotate any credential that was exposed before deployment.

## Environment Template

Start from `.env.example` or `deploy/env/hydro.env.example` and replace placeholders only in the target environment. The production environment file belongs outside Git at `/etc/hydro/hydro.env`:

- `HYDRO_SESSION_SECRET` must be a long random secret from a secret manager.
- `HYDRO_DATABASE_PATH` must point to an absolute production SQLite path owned by the service user.
- `HYDRO_SESSION_COOKIE_SECURE=1` must be set when HYDRO runs behind TLS.
- `HYDRO_BOOTSTRAP_ADMIN_USERNAME` and `HYDRO_BOOTSTRAP_ADMIN_PASSWORD` are optional initial admin values.
- `HYDRO_ALLOW_DEV_SECRET` is local development only and must not be set in production.

## Runtime and Process Manager Checklist

- Review `deploy/systemd/hydro.service.example` before adapting a real service file.
- Run the app with `uvicorn app.main:app` under an operator-managed process manager such as systemd.
- Run HYDRO as a non-root service user.
- Ensure the service user owns the SQLite directory and database file.
- Keep the production environment file readable only by the service account and administrators.
- Inspect runtime logs through journald after service start, restart, and rollback checks.

## Reverse Proxy, TLS, and Firewall

- Review `deploy/caddy/Caddyfile.example` as the placeholder reverse proxy template.
- Put HYDRO behind a reverse proxy that owns HTTPS, TLS termination, and any HSTS policy.
- Set `HYDRO_SESSION_COOKIE_SECURE=1` behind TLS so browser sessions use secure cookies.
- Expose only the reverse proxy entrypoint through the firewall.
- Keep the application process bound to a private interface or socket managed by the operator.

## SQLite Backup, Restore, and Rollback

- Take a SQLite backup before releases, destructive operations, or any change that may affect production data.
- Use SQLite backup and restore tooling selected by the operator; this repository intentionally does not add backup scripts.
- Document where the backup is stored and how the operator will restore it before proceeding.
- Define rollback expectations before live changes: stop the service, restore the selected SQLite backup, verify ownership, restart the service, and run a smoke check.

## Destructive Initialization Warning

`scripts/init_db.py is destructive`. Do not run it against live production data unless an explicit backup/restore decision is accepted before execution.

## Manual Readiness Checklist

- [ ] Real secrets are supplied outside Git through the target environment or secret manager.
- [ ] Exposed credentials have been rotated before use.
- [ ] TLS and reverse proxy behavior are configured by the operator.
- [ ] Firewall posture exposes only the intended reverse proxy entrypoint.
- [ ] HYDRO runs as a non-root service user.
- [ ] SQLite path ownership and permissions are verified.
- [ ] Backup, restore, and rollback steps are documented before deployment.
- [ ] `scripts/init_db.py` is not run on live data without accepted destructive-operation intent.

## Runtime Artifact Index

- `deploy/README.md`
- `deploy/systemd/hydro.service.example`
- `deploy/env/hydro.env.example`
- `deploy/caddy/Caddyfile.example`
