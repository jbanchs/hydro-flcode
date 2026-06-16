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
3. Review staging readiness in `docs/deployment.md`: first MVP staging uses `HYDRO_ENV=production` for production-like staging validation with staging-specific secret values supplied outside Git.
4. Review manual staging server bootstrap prerequisites in `docs/deployment.md`: the checklist is documentation-only, manual operator-run on the server, and limited to audit facts, `git`, `python3-venv`, `sqlite3`, package verification, passworded sudo, Python 3.10 compatibility caution, and key-based authentication recommendation.
5. Keep Caddy deferred; any later approval must remain package-only and unconfigured until a separate ingress/TLS change.
6. Confirm `/etc/hydro/hydro.env` exists outside Git with restrictive permissions.
7. Confirm `HYDRO_ENV=production`, a real session secret, `HYDRO_SESSION_COOKIE_SECURE=1`, no development-secret allowance, and an absolute non-default database path are present in the real runtime environment.
8. Confirm the service user owns the SQLite database path and parent directory.
9. Confirm the reverse proxy owns TLS and the firewall exposes only the proxy entrypoint.
10. Confirm manual SQLite backup/restore readiness in `docs/deployment.md`: record the pre-deploy backup, restore rehearsal target, rollback boundary, and safety boundaries with placeholders only.
11. Use `GET /healthz` as a liveness-only smoke check through the normal reverse proxy path; it is not a readiness, database, dependency, or authenticated workflow validation endpoint.
12. Run project validation with `py -m pytest` from a workstation or CI context.

Real deployment values and remote server procedures are intentionally out of scope.
