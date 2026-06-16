# HYDRO Deployment Readiness

This runbook prepares a future production deployment review. It does not deploy HYDRO, provision servers, configure infrastructure, create CI/CD deployment jobs, or add executable deployment automation.

## Scope Boundary

- Use this document as a manual readiness checklist before a later deployment.
- Keep real credentials, host-specific values, tokens, passwords, and private infrastructure notes outside Git.
- Supply production values through the target environment or a secret manager.
- Rotate any credential that was exposed before deployment.

## Environment Template

Start from `.env.example` or `deploy/env/hydro.env.example` and replace placeholders only in the target environment. The production environment file belongs outside Git at `/etc/hydro/hydro.env`:

Before copying values into any real environment, run `py scripts/validate_runtime_config.py` from the repository root. This command is local template preflight only: it checks committed placeholder templates and does not read real secrets, contact servers, deploy HYDRO, or prove production readiness.

- `HYDRO_SESSION_SECRET` must be a long random secret from a secret manager.
- `HYDRO_ENV=production` is the only production signal. Unsupported aliases include `prod`, `live`, `1`, and `true`.
- `HYDRO_DATABASE_PATH` must point to an absolute production SQLite path owned by the service user.
- `HYDRO_SESSION_COOKIE_SECURE=1` must be set when HYDRO runs behind TLS.
- `HYDRO_BOOTSTRAP_ADMIN_USERNAME` and `HYDRO_BOOTSTRAP_ADMIN_PASSWORD` are optional initial admin values.
- `HYDRO_ALLOW_DEV_SECRET` is local development only and must not be set in production.

When `HYDRO_ENV=production` is set, HYDRO fails startup before serving requests if the session secret is missing, secure cookies are disabled, development-secret allowance is enabled, or the database path is not an absolute non-default path. This check does not read real environment files, inspect secrets, contact servers, or run deploy automation.

## Runtime and Process Manager Checklist

- Review `deploy/systemd/hydro.service.example` before adapting a real service file.
- Run the app with `uvicorn app.main:app` under an operator-managed process manager such as systemd.
- Run HYDRO as a non-root service user.
- Ensure the service user owns the SQLite directory and database file.
- Keep the production environment file readable only by the service account and administrators.
- Inspect runtime logs through journald after service start, restart, and rollback checks.

## Liveness Smoke Check

Use `GET /healthz` as a liveness-only smoke check after service start, restart, reverse-proxy changes, and rollback checks. It returns static non-sensitive JSON and is not a readiness, database, dependency, or authenticated workflow validation endpoint.

## Local Browser Smoke Checklist

Use this local-only checklist for pre-deploy confidence while GitHub Actions is blocked by billing. It complements `py -m pytest`; it does not replace CI, create deployment automation, contact remote services, require browser automation, or require real secrets.

- [ ] Run HYDRO locally with placeholder development/test configuration only, then run `py -m pytest`.
- [ ] Open `/healthz` and confirm it returns liveness JSON only. Keep readiness, database, dependency, and authenticated workflow checks separate.
- [ ] Open `/login` and confirm the page is readable, styled, and usable with local `/static/css/styles.css`.
- [ ] Sign in locally and confirm authenticated `/` renders the regulation search workflow and Ask HYDRO panel.
- [ ] Run a search and confirm the table refreshes with readable rows, badges, and empty-result feedback when applicable.
- [ ] Ask HYDRO a source-backed question and confirm the answer is readable and citation-first.
- [ ] Ask HYDRO for missing or unsupported information and confirm the UI states that the answer cannot be confirmed from available sources.
- [ ] In browser developer tools, confirm CSS and JavaScript load from same-origin `/static/...` assets and no CDN script/style request is required.

Playwright, Selenium, Cypress, screenshots, and CI browser jobs remain deferred for this slice. Move those tools to a follow-up proposal if repeated UI regressions or pre-production readiness justify the added dependency and review cost.

## Staging Readiness Handoff

Use this repo-local staging handoff checklist for first MVP validation. Staging is production-like staging validation: run HYDRO with `HYDRO_ENV=production` and staging-specific secret values supplied outside Git by the operator.

This section is a documentation handoff only. It does not deploy HYDRO, contact servers, inspect private infrastructure, or prove production readiness.

### Staging handoff checklist

- [ ] Confirm the target staging runtime will use `HYDRO_ENV=production`; do not create a separate staging runtime mode.
- [ ] Confirm staging-specific secret values are supplied outside Git through the target environment or secret manager.
- [ ] Confirm every tracked template remains placeholder-only and generic.
- [ ] Confirm `/healthz` remains a liveness-only smoke check, not readiness validation.
- [ ] Confirm the operator owns any out-of-band deployment, server configuration, secret injection, backup process, and rollback execution.

### Staging dry-run checklist

Use this staging dry-run checklist locally before handoff. It is placeholder-only, non-deploying, and repo-local.

- [ ] Run `py scripts/validate_runtime_config.py` from the repository root.
- [ ] Run `py -m pytest` from the repository root.
- [ ] Confirm the dry run uses no real secrets, environment files, servers, deployment targets, or hydro.db.
- [ ] Confirm no new deployment scripts, CI gates, server probes, app code, or runtime modes were added for staging.

### Manual staging validation runbook

After staging has already been deployed outside this repository slice, the operator-owned manual staging validation runbook is:

- [ ] Open `/healthz` and confirm it returns liveness-only JSON; keep database, dependency, readiness, and authenticated workflow validation separate.
- [ ] Open `/login` and confirm the login page is reachable, readable, and served with same-origin static assets.
- [ ] Sign in and confirm authenticated / renders the regulation search workflow and Ask HYDRO panel.
- [ ] Run a search and confirm results, empty-result feedback, and table readability.
- [ ] Ask HYDRO a citation-backed question and confirm citation-backed Ask HYDRO behavior.
- [ ] Ask HYDRO for unsupported information and confirm it says the answer cannot be confirmed from available sources.
- [ ] Inspect logs through the operator-managed logging path for startup, authentication, search, Ask HYDRO, and error signals.
- [ ] Confirm rollback instructions, owner, and decision point are known before any production promotion.
- [ ] Confirm backup location, restore owner, and non-destructive restore rehearsal evidence exist outside Git.

Staging scope boundaries:

- Do not introduce HYDRO_ENV=staging.
- Do not deploy HYDRO, contact servers, probe staging hosts, or add deploy automation.
- Do not read real environment files, secrets, ignored sensitive notes, staging data, or hydro.db.
- Do not add scripts, CI gates, server probes, app code, runtime modes, or readiness semantics for /healthz.

## Manual Staging Server Bootstrap Prerequisites

Use this checklist before any later approved staging deployment work. It is documentation-only and manual operator-run on the server; this repository does not access the server, deploy HYDRO, add scripts, change CI, configure Caddy, configure systemd, read secrets, read real environment files, or read real databases.

### Audited target facts

| Fact | Recorded value | Operator note |
|------|----------------|---------------|
| Operating system | Ubuntu 22.04 | Use Ubuntu package names and commands when the operator is already in an approved shell session. |
| Package manager | `apt` | Package examples are manual operator-run on the server, not repository automation. |
| Process manager available | `systemctl` | Verification only; no systemd configuration is changed in this slice. |
| Privilege boundary | passworded sudo | The operator must enter the sudo password interactively and never record, echo, store, request, or commit sudo passwords. |
| Python audit fact | Python 3.10 | Python 3.10 is an audited server fact, not compatibility approval for HYDRO's Python 3.13 baseline. |
| Missing package | missing git | Treat `git` as an operator-installed prerequisite. |
| Missing package | missing Caddy | Caddy is deferred; if later approved, keep it package-only and unconfigured until a separate ingress/TLS change. |
| Missing package | missing sqlite3 | Treat `sqlite3` as an operator-installed prerequisite. |
| Disk | 20G disk | Confirm available capacity before staging work. |
| Memory | 2GiB RAM | Confirm available memory before staging work. |

### Minimal prerequisite checklist

The minimal prerequisites for a later approved staging bootstrap are operator-installed prerequisites only:

- [ ] `git`
- [ ] `python3-venv`
- [ ] `sqlite3`

If installation is approved out of band, the operator may run package commands manually in their authorized shell session, for example `sudo apt update` and `sudo apt install git python3-venv sqlite3`. These commands are documentation-only examples; they are not scripts, not CI, not remote commands, and not deployment automation.

Use key-based authentication for any later approved server access. Do not place key material, hostnames, credentials, or access instructions in this repository.

### Operator-run verification checklist

Run these commands only from the operator's approved shell session on the target host:

- [ ] Python: `python3 --version`
- [ ] Virtual environment support: `python3 -m venv --help`
- [ ] Git: `git --version`
- [ ] SQLite CLI: `sqlite3 --version`
- [ ] systemd tooling: `systemctl --version`
- [ ] apt tooling: `apt --version`
- [ ] sudo boundary: `sudo -v`
- [ ] Disk capacity: `df -h`
- [ ] Memory capacity: `free -h`

Caddy is deferred in this bootstrap slice. Do not create or modify Caddyfiles, systemd units, firewall rules, TLS settings, deployment scripts, CI jobs, secrets, real environment files, or real database files here.

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
- To rollback only the production-mode signal, unset or change `HYDRO_ENV` away from `production` after confirming the operator accepts restoring development/test startup behavior.

### Manual SQLite backup/restore rehearsal checklist

This manual SQLite backup/restore rehearsal checklist is a placeholder-only readiness review. It is a non-destructive rehearsal that the operator adapts outside Git before a live deployment.

- [ ] Record the pre-deploy backup location as `<backup-path>` before any release or destructive operation.
- [ ] Record the isolated restore rehearsal target as `<restore-test-db>`; it must not be the live database.
- [ ] Rehearse the restore decision manually with placeholder commands and paths only.
- [ ] Confirm the rollback boundary: reverting this repository change only removes docs, tests, and OpenSpec artifacts; live data rollback remains an operator-run restore from `<backup-path>` into an isolated target such as `<restore-test-db>`.
- [ ] Confirm restoration expectations, ownership checks, service restart order, and liveness smoke checks before live changes.

Safety boundaries:

- Do not read, copy, open, or restore a live hydro.db during rehearsal.
- Do not read real environment files, secrets, ignored sensitive notes, or production data.
- Do not contact servers or run remote access commands.
- Do not add backup scripts, restore scripts, app backup logic, or destructive restore automation.
- Keep any real backup path, database path, host, credential, or private operator note outside Git.

## Destructive Initialization Warning

`scripts/init_db.py is destructive`. Do not run it against live production data unless an explicit backup/restore decision is accepted before execution.

## Manual Readiness Checklist

- [ ] `py scripts/validate_runtime_config.py` passes as local template preflight only and does not prove production readiness.
- [ ] Real secrets are supplied outside Git through the target environment or secret manager.
- [ ] `HYDRO_ENV=production` is set only when production session, cookie, and database expectations are ready.
- [ ] Exposed credentials have been rotated before use.
- [ ] TLS and reverse proxy behavior are configured by the operator.
- [ ] Firewall posture exposes only the intended reverse proxy entrypoint.
- [ ] HYDRO runs as a non-root service user.
- [ ] SQLite path ownership and permissions are verified.
- [ ] Backup, restore, and rollback steps are documented before deployment.
- [ ] `scripts/init_db.py` is not run on live data without accepted destructive-operation intent.
- [ ] `/healthz` liveness-only smoke check is reachable through the normal reverse proxy path.
- [ ] Local browser smoke checklist has been completed with placeholder-only configuration and no real secrets recorded in tracked files.

## Runtime Artifact Index

- `deploy/README.md`
- `deploy/systemd/hydro.service.example`
- `deploy/env/hydro.env.example`
- `deploy/caddy/Caddyfile.example`
