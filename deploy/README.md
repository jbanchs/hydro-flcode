# HYDRO Runtime Artifact Examples

This directory contains example-only runtime artifacts for a later HYDRO production deployment review. It does not deploy HYDRO, provision servers, create CI/CD deployment jobs, or provide executable deployment automation.

## Scope

- Keep every committed value as a placeholder or generic example.
- Keep real secrets, real hostnames, real IP addresses, private paths, and operator notes outside Git.
- Create the real environment file outside the repository at `/etc/hydro/hydro.env`.
- Use `HYDRO_ENV=production` as the only production signal. Unsupported aliases include `prod`, `live`, `1`, and `true`.
- Run HYDRO as a non-root service user.
- Let the reverse proxy own TLS and public ingress.

## Artifacts

- `deploy/README.md` — this index and scope boundary.
- `deploy/systemd/hydro.service.example` — placeholder systemd service shape.
- `deploy/env/hydro.env.example` — placeholder runtime environment file shape.
- `deploy/caddy/Caddyfile.example` — placeholder reverse proxy and TLS shape.

## Manual Validation Order

1. Run `py scripts/validate_runtime_config.py` as local template preflight only; it checks committed placeholders and does not prove production readiness.
2. Review placeholders and replace them only in the target environment.
3. Confirm `/etc/hydro/hydro.env` exists outside Git with restrictive permissions.
4. Confirm `HYDRO_ENV=production`, a real session secret, `HYDRO_SESSION_COOKIE_SECURE=1`, no development-secret allowance, and an absolute non-default database path are present in the real runtime environment.
5. Confirm the service user owns the SQLite database path and parent directory.
6. Confirm the reverse proxy owns TLS and the firewall exposes only the proxy entrypoint.
7. Confirm manual SQLite backup/restore readiness in `docs/deployment.md`: record the pre-deploy backup, restore rehearsal target, rollback boundary, and safety boundaries with placeholders only.
8. Use `GET /healthz` as a liveness-only smoke check through the normal reverse proxy path; it is not a readiness, database, dependency, or authenticated workflow validation endpoint.
9. Run project validation with `py -m pytest` from a workstation or CI context.

Real deployment values and remote server procedures are intentionally out of scope.
