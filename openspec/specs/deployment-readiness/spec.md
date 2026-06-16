# Deployment Readiness Specification

## Purpose

Define documentation-only readiness requirements for a future HYDRO production deployment without performing deployment, provisioning, automation, runtime hardening, or secret handling in Git.

## Requirements

### Requirement: Placeholder Environment Template

The system MUST provide a committed `.env.example` that documents required production environment variables with placeholders only and MUST NOT include real credentials, hostnames, IPs, tokens, or copied secret values.

#### Scenario: Template uses placeholders

- GIVEN a reviewer opens `.env.example`
- WHEN they inspect each configured value
- THEN every sensitive or deployment-specific value is a placeholder
- AND production variables such as database path, session secret, bootstrap password, and secure-cookie mode are represented.

#### Scenario: Real secret is rejected

- GIVEN a proposed `.env.example` contains a real-looking credential or host-specific secret
- WHEN the deployment-readiness review runs
- THEN the change MUST be considered non-compliant until the value is replaced with a placeholder.

### Requirement: Deployment Runbook and Scope Boundary

The system MUST provide a deploy readiness runbook/checklist covering manual verification steps and MUST state that this slice does not deploy, provision, configure servers, create CI/CD deploy jobs, or add executable infrastructure.

#### Scenario: Operator reads the runbook

- GIVEN an operator is preparing for a later deployment
- WHEN they follow the runbook
- THEN they can identify required checks before deployment
- AND they are warned that no actual deployment is performed by this slice.

### Requirement: Secret Handling Guidance

Deployment documentation MUST state that real secrets stay outside Git, exposed credentials MUST be rotated before deployment, and production secret values SHALL be supplied through the target environment or secret manager.

#### Scenario: Secret source is documented

- GIVEN production configuration is being prepared
- WHEN the operator reads secret guidance
- THEN they know not to commit secrets
- AND they know exposed credentials require rotation before use.

### Requirement: Production Runtime Configuration Guidance

Deployment documentation MUST cover HTTPS expectations, `HYDRO_SESSION_COOKIE_SECURE=1` behind TLS, reverse proxy/TLS responsibility, firewall expectations, SQLite path and ownership, and running the service as a non-root user.

#### Scenario: HTTPS deployment is reviewed

- GIVEN HYDRO will run behind a reverse proxy
- WHEN production settings are checked
- THEN secure cookies, TLS termination, firewall posture, service user, and database ownership are included in the checklist.

### Requirement: Local Runtime Template Validator

The system MUST provide a local, non-deploying validator for committed runtime environment templates. The validator MUST inspect placeholder template files only and MUST NOT read real environment files, secrets, server state, or deployment targets.

#### Scenario: Template validator succeeds for placeholder templates

- GIVEN committed runtime template files contain the required keys with placeholder-only sensitive and deployment-specific values
- WHEN a maintainer runs the local validator
- THEN validation MUST pass without contacting servers or reading real environment files.

#### Scenario: Real runtime source is not accessed

- GIVEN real `.env`, system environment, secret manager, or server runtime state exists outside committed templates
- WHEN the validator runs
- THEN it MUST NOT read, summarize, require, or validate those real sources.

### Requirement: Placeholder-Only Runtime Inputs

Committed runtime templates MUST use placeholders for sensitive or deployment-specific values, including secrets, passwords, hostnames, IPs, private paths, and deployment-specific identifiers. Production-oriented template values MAY document required shapes, but MUST NOT contain deployable credentials or real server data.

#### Scenario: Placeholder-only values are accepted

- GIVEN `.env.example` and deploy runtime templates use documented placeholders for sensitive and deployment-specific keys
- WHEN local validation runs
- THEN the templates MUST be accepted as reviewable examples.

#### Scenario: Real-looking deployment data is rejected

- GIVEN a committed runtime template contains a real-looking secret, hostname, IP address, private path, or copied deployment value
- WHEN local validation runs
- THEN validation MUST fail until the value is replaced with a placeholder.

### Requirement: Runtime Config Validation Boundary

Runtime config validation MUST remain local, template-only, and non-deploying. It MUST NOT deploy HYDRO, provision infrastructure, access servers, fix CI billing, create deployment automation, or claim complete production readiness.

#### Scenario: Boundary wording is visible

- GIVEN a maintainer reads deployment documentation
- WHEN they find runtime config validation guidance
- THEN the documentation MUST state that validation is local template preflight only
- AND it MUST NOT describe the result as full production readiness.

#### Scenario: Scope expansion is rejected

- GIVEN a change adds SSH access, deploy scripts, server probes, CI deploy jobs, or production readiness claims to the validator slice
- WHEN deployment-readiness review runs
- THEN the change MUST be rejected as out of scope.

### Requirement: Pytest Guards for Runtime Config Validation

The test suite MUST include local pytest guards for runtime template parity, placeholder-only validation, boundary wording, and prohibited real-env/server/deploy access. These guards MUST run with the existing local pytest runner and MUST fail if SQLite backup/restore docs omit required safety wording, include non-placeholder commands/paths, read real `hydro.db`, env files, secrets, ignored sensitive notes, or servers, or introduce backup/restore automation.

#### Scenario: Validator regressions are detected

- GIVEN the validator stops enforcing required template parity or placeholder-only sensitive values
- WHEN `py -m pytest` runs locally
- THEN the relevant guard MUST fail.

#### Scenario: Boundary regressions are detected

- GIVEN docs or validator behavior imply real environment access, deployment automation, server access, or full production readiness
- WHEN `py -m pytest` runs locally
- THEN the relevant guard MUST fail.

#### Scenario: Backup restore safety regressions are detected

- GIVEN backup/restore docs omit safety boundaries or include live paths, real DB/env/secret access, server access, or destructive automation wording
- WHEN `py -m pytest` runs locally
- THEN the relevant static guard MUST fail before implementation proceeds.

### Requirement: Explicit Production Mode Signal

HYDRO MUST treat production mode as enabled only when `HYDRO_ENV` is set to the exact normalized value `production`. Aliases such as `prod`, `live`, `1`, or `true` MUST NOT enable production mode. When `HYDRO_ENV` is unset or any non-production value, development and test behavior MUST remain unchanged unless the value is explicitly `production`.

#### Scenario: Exact production enables production mode

- GIVEN `HYDRO_ENV=production`
- WHEN runtime configuration is evaluated
- THEN production mode MUST be enabled
- AND production-only fail-closed checks MUST apply.

#### Scenario: Alias does not enable production mode

- GIVEN `HYDRO_ENV=prod`
- WHEN runtime configuration is evaluated
- THEN production mode MUST NOT be enabled
- AND development/test startup behavior MUST remain unchanged.

### Requirement: Production Fail-Closed Runtime Checks

When production mode is enabled, HYDRO MUST fail startup before serving requests if the session secret is missing or unsafe, secure cookies are disabled, development-secret allowance is enabled, or configured database path expectations are unsafe/default according to the current configuration model. These checks MUST NOT read real environment files, secrets, server state, or deployment targets.

#### Scenario: Production rejects unsafe session settings

- GIVEN `HYDRO_ENV=production` and missing session secret, insecure cookie mode, or enabled dev-secret allowance
- WHEN the application is constructed
- THEN startup MUST fail closed before serving requests.

#### Scenario: Non-production startup is unaffected

- GIVEN `HYDRO_ENV` is unset or set to a non-production value
- WHEN the application is constructed with existing dev/test settings
- THEN startup MUST follow current dev/test behavior.

#### Scenario: Production rejects unsafe database path

- GIVEN `HYDRO_ENV=production` and the database path is default, relative, or otherwise unsafe under documented expectations
- WHEN startup checks run
- THEN startup MUST fail closed with a configuration error.

### Requirement: Production Signal Documentation and Templates

Committed env templates and deployment documentation MUST describe `HYDRO_ENV=production`, unsupported aliases, required production session/cookie/database expectations, and the boundary that no deploy automation or real secret inspection is performed. Templates MUST use placeholders only.

#### Scenario: Operator sees production signal guidance

- GIVEN an operator reads env templates or deployment docs
- WHEN they review production configuration guidance
- THEN `HYDRO_ENV=production` MUST be documented as the only production signal
- AND aliases MUST be documented as unsupported.

#### Scenario: Template boundary is preserved

- GIVEN committed templates are reviewed
- WHEN production values are inspected
- THEN sensitive and deployment-specific values MUST remain placeholders only.

### Requirement: Isolated Production Mode Test Coverage

The test suite MUST cover exact production detection, alias rejection, production-only fail-closed checks, unaffected dev/test startup, template/docs expectations, and validator boundaries. Tests MUST isolate environment variables so `HYDRO_ENV` or production settings cannot leak between tests.

#### Scenario: Production guard regressions are detected

- GIVEN production-mode tests run with isolated environment variables
- WHEN an unsafe production setting is allowed or alias enables production
- THEN `py -m pytest` MUST fail.

#### Scenario: Environment leakage is prevented

- GIVEN one test sets `HYDRO_ENV=production`
- WHEN another dev/test scenario runs
- THEN the production value MUST NOT leak into that scenario.

### Requirement: SQLite Backup and Rollback Discipline

Deployment documentation MUST require a SQLite backup before destructive operations or releases and MUST describe manual restore rehearsal, rollback boundaries, and production-data protection using placeholder-only commands and paths. The documentation MUST NOT access live `hydro.db`, real environment files, secrets, ignored sensitive notes, servers, or production data, and MUST NOT add destructive automation.

#### Scenario: Rollback is planned

- GIVEN a production change may affect SQLite data
- WHEN the operator reviews rollback steps
- THEN a backup is required before proceeding
- AND restoration expectations are documented before live changes.

#### Scenario: Manual restore rehearsal is documented safely

- GIVEN an operator reviews SQLite readiness guidance
- WHEN they inspect backup and restore examples
- THEN commands and paths MUST use placeholders such as `<backup-path>` and `<restore-test-db>` only
- AND guidance MUST state that rehearsal is manual and non-destructive.

#### Scenario: Live data and secret access are prohibited

- GIVEN deployment-readiness docs or tests are reviewed
- WHEN backup/restore guidance references data, env, secrets, notes, or servers
- THEN it MUST prohibit real `hydro.db` access, real env/secret reads, ignored sensitive note reads, server access, and production-data access.

### Requirement: Destructive Initialization Warning

Deployment documentation MUST warn that `scripts/init_db.py` is destructive and MUST NOT be run against live production data unless backup/restore intent is explicit and accepted.

#### Scenario: Init script warning is visible

- GIVEN an operator searches deployment docs for database initialization
- WHEN they find `scripts/init_db.py`
- THEN the destructive behavior warning is prominent
- AND production use requires an explicit backup/restore decision.

### Requirement: Non-Secret Runtime Artifact Templates

The system MUST provide example-only production runtime templates for systemd, environment file placement, and reverse proxy/TLS guidance using placeholders only. Templates MUST guide operators toward `/etc/hydro/hydro.env`, direct `uvicorn app.main:app`, non-root execution, and proxy-managed TLS without including real secrets, hosts, IPs, private paths, deploy automation, or server access instructions.

#### Scenario: Runtime templates are reviewable

- GIVEN a reviewer opens the runtime templates
- WHEN they inspect service, env, and proxy examples
- THEN the examples use placeholders only
- AND they identify systemd service shape, env file location, proxy/TLS responsibility, and non-root service user guidance.

#### Scenario: Real deployment data is excluded

- GIVEN a proposed runtime template includes a real credential, hostname, IP, private path, SSH target, or copied deployment value
- WHEN the deployment-readiness review runs
- THEN the change MUST be considered non-compliant until the value is removed or replaced with a placeholder.

### Requirement: Production Operations Checklist

The system MUST provide documentation covering SQLite absolute data path guidance, ownership expectations, pre-deploy backup, manual restore rehearsal, rollback boundaries, destructive initialization warnings, logging inspection, firewall checklist, and explicit scope boundaries. The documentation MUST use placeholder-only commands/paths and MUST NOT perform deployment, provision servers, add CI/CD deploy jobs, add one-shot deploy scripts, access real databases/secrets/servers, or introduce destructive automation.

#### Scenario: Operator prepares manually

- GIVEN an operator is preparing a later production deployment
- WHEN they read the operations checklist
- THEN they can identify data path, ownership, pre-deploy backup, restore rehearsal, rollback boundaries, logs, firewall, TLS, and service-user checks
- AND they understand validation remains manual, placeholder-only, and environment-specific.

#### Scenario: Automation remains out of scope

- GIVEN a change proposes SSH commands, server provisioning, CI/CD deployment, backup scripts, restore scripts, live DB reads, real secret reads, or one-shot automation
- WHEN it is reviewed against deployment readiness
- THEN the change MUST be rejected for this slice
- AND documentation MUST keep the scope as non-secret templates, placeholders, and manual guidance only.

### Requirement: Tracked Artifact Sensitive Reference Guard

Tracked deployment-readiness artifacts MUST NOT include the sensitive local deployment-note filename or path pattern. Generic wording MAY describe an ignored local deployment secret note without naming or locating it.

#### Scenario: Tracked artifacts use generic wording

- GIVEN tracked deployment-readiness documentation or OpenSpec artifacts are reviewed
- WHEN they refer to the local deployment secret note
- THEN the reference MUST use generic wording only
- AND it MUST NOT disclose the sensitive filename or path pattern.

#### Scenario: Prohibited reference is rejected

- GIVEN a tracked artifact includes the sensitive local note filename or path pattern
- WHEN deployment-readiness checks run
- THEN the change MUST be considered non-compliant until the reference is removed or generalized.

### Requirement: Archive Redaction Exception

Archived OpenSpec artifacts SHOULD remain immutable, except a narrow security-redaction change MAY replace sensitive local deployment-note references with generic wording while preserving audit meaning.

#### Scenario: Security redaction preserves audit meaning

- GIVEN an archived OpenSpec artifact exposes the sensitive local note reference pattern
- WHEN a security-redaction exception is applied
- THEN only the sensitive reference MUST be generalized
- AND the surrounding audit meaning MUST remain intact.

#### Scenario: Unrelated archive rewrite is rejected

- GIVEN an archive edit changes scope, decisions, or unrelated deployment text
- WHEN it is reviewed as part of this redaction exception
- THEN the change MUST be rejected as outside the allowed exception.

### Requirement: Guard Coverage for Archived Markdown

The test suite MUST guard tracked archived OpenSpec markdown against reintroducing the sensitive local deployment-note filename or path pattern.

#### Scenario: Archive guard detects reintroduction

- GIVEN archived OpenSpec markdown contains the prohibited sensitive reference pattern
- WHEN `py -m pytest` runs locally
- THEN the relevant test MUST fail.

#### Scenario: Generic secret language remains allowed

- GIVEN archived OpenSpec markdown uses generic wording for ignored local deployment secret notes
- WHEN `py -m pytest` runs locally
- THEN the guard MUST allow the artifact.

### Requirement: No History Rewrite or Sensitive File Access

This change MUST NOT rewrite Git history and MUST NOT read, open, copy, summarize, or otherwise access the ignored local deployment secret note.

#### Scenario: Current tracked files are sanitized only

- GIVEN the sensitive reference exists in current tracked artifacts
- WHEN the sanitation change is applied
- THEN only current tracked content and tests MUST be changed
- AND Git history MUST NOT be rewritten.

#### Scenario: Ignored local note remains untouched

- GIVEN the ignored local deployment secret note exists outside tracked artifacts
- WHEN the sanitation work is performed
- THEN the note MUST NOT be read, copied, summarized, or named in artifacts.

### Requirement: Public Liveness Health Endpoint

The system MUST provide an unauthenticated `GET /healthz` liveness endpoint for manual deployment, systemd, and reverse-proxy smoke checks. The endpoint MUST return HTTP 200 with static non-sensitive JSON and MUST NOT query SQLite, validate readiness, probe dependencies, expose configuration, expose secrets, or validate authenticated workflows.

#### Scenario: Liveness request succeeds without authentication

- GIVEN an unauthenticated client
- WHEN the client requests `GET /healthz`
- THEN the response MUST return HTTP 200
- AND the response body MUST be static non-sensitive JSON such as `{"status":"ok"}`.

#### Scenario: Liveness does not perform readiness checks

- GIVEN SQLite is unavailable or application dependencies are not ready
- WHEN the client requests `GET /healthz`
- THEN the endpoint MUST NOT query SQLite or dependency state
- AND the response MUST remain a liveness-only static response.

#### Scenario: Health endpoint is not part of auth flow

- GIVEN an unauthenticated client without a session
- WHEN the client requests `GET /healthz`
- THEN the response MUST NOT redirect to `/login`
- AND it MUST NOT require API authentication or CSRF state.

### Requirement: Liveness Documentation

Deployment documentation MUST reference `/healthz` for liveness smoke checks and MUST clearly state that it is not a readiness, database, dependency, or authenticated workflow validation endpoint.

#### Scenario: Operator reads smoke-check guidance

- GIVEN an operator reviews deployment documentation
- WHEN they find health-check guidance
- THEN `/healthz` MUST be documented as a liveness smoke-check URL
- AND readiness and database validation MUST be explicitly excluded.

#### Scenario: Misuse as readiness is prevented

- GIVEN a proposed document describes `/healthz` as readiness or dependency validation
- WHEN deployment-readiness review runs
- THEN the change MUST be considered non-compliant until the wording is corrected.

### Requirement: Health Endpoint Test Coverage

Automated tests MUST verify `/healthz` status, static body, unauthenticated access, no login redirect, no database/readiness dependency, and expected security-header inheritance.

#### Scenario: Health regression is detected

- GIVEN the health endpoint tests
- WHEN `/healthz` requires authentication, redirects, changes body shape, or performs readiness work
- THEN the test suite MUST fail.

### Requirement: Local HTML and Static Asset Smoke Coverage

The system MUST provide local pytest smoke coverage for server-rendered HTML, DOM hooks/text, security headers, and app-owned static CSS/JavaScript references using the existing pytest/FastAPI `TestClient` stack only, without new browser automation dependencies, remote CI, deployment, or secrets.

#### Scenario: Local smoke validates rendered pages

- GIVEN a developer has installed project test dependencies
- WHEN they run `py -m pytest` locally
- THEN smoke coverage MUST verify `/healthz`, `/login`, and authenticated `/` return expected responses and security headers
- AND rendered pages MUST expose required local CSS, JavaScript, stable DOM hooks, and key text.

#### Scenario: Static reference regression is detected

- GIVEN a rendered page references a missing local static asset or forbidden external script/style source
- WHEN local pytest smoke coverage runs
- THEN the test suite MUST fail before any deployment or browser automation is required.

### Requirement: Manual Browser Checklist

README/deployment documentation MUST provide a concise manual local browser checklist for visual readability and JavaScript behavior that pytest cannot execute. The checklist MUST remain local-only and MUST NOT require Playwright, Selenium, Cypress, screenshots, remote CI, deployment, or secrets.

#### Scenario: Maintainer performs local browser smoke

- GIVEN the app is running locally with safe development/test configuration
- WHEN a maintainer follows the checklist in a browser
- THEN they MUST verify `/healthz`, `/login`, authenticated `/`, local styling, search interaction, and Ask HYDRO states
- AND they MUST record issues without adding real secrets to tracked files.

#### Scenario: Playwright remains deferred

- GIVEN a change proposes Playwright, screenshots, browser downloads, or CI browser jobs for this slice
- WHEN it is reviewed against local-browser-smoke scope
- THEN the change MUST be rejected or moved to a follow-up proposal.

### Requirement: Local Validation Boundary

The smoke path MUST provide local confidence while GitHub Actions is billing-blocked and MUST preserve existing deployment-readiness boundaries: `/healthz` remains liveness-only, no CI/deployment fix is implied, no remote service is contacted, and no secret-bearing artifact is read, created, copied, or named.

#### Scenario: CI or deployment is unavailable

- GIVEN GitHub Actions is blocked by billing or deployment infrastructure is unavailable
- WHEN a developer needs pre-deployment confidence
- THEN they MUST be able to run the local pytest smoke checks and manual checklist without remote dependencies.

#### Scenario: Secret handling boundary is preserved

- GIVEN local smoke documentation or tests are reviewed
- WHEN they describe configuration needs
- THEN they MUST use placeholder or safe test configuration only
- AND they MUST NOT disclose, require, or inspect real deployment secrets.

### Requirement: Local OpenSpec Validation Guidance

Developer-facing SDD/OpenSpec guidance MUST document the local validation ladder for active changes: use `openspec validate <change> --strict` only when a verified OpenSpec CLI is already installed, otherwise use `gentle-ai sdd-status <change>` as a native status and archive-readiness signal. The guidance MUST state that `gentle-ai sdd-status` is not strict OpenSpec CLI schema validation.

#### Scenario: Strict CLI is available

- GIVEN a developer has a verified local OpenSpec CLI available
- WHEN they validate `local-openspec-validation`
- THEN guidance MUST direct them to run `openspec validate local-openspec-validation --strict`
- AND the result MAY be described as strict OpenSpec CLI validation.

#### Scenario: Native fallback is used

- GIVEN no verified local OpenSpec CLI is available
- WHEN a developer checks `local-openspec-validation`
- THEN guidance MUST direct them to `gentle-ai sdd-status local-openspec-validation`
- AND it MUST NOT describe that command as strict OpenSpec CLI schema validation.

### Requirement: No Unverified CLI or Deployment Scope Expansion

This change MUST NOT install, pin, globally require, or recommend an unverified OpenSpec CLI package. It MUST NOT introduce secrets, deployment automation, production config changes, CI billing fixes, runtime app changes, or remote-service dependencies.

#### Scenario: CLI installation is proposed

- GIVEN a change adds installation or pinning for an unverified OpenSpec CLI
- WHEN deployment-readiness review runs
- THEN the change MUST be rejected as out of scope.

#### Scenario: Operational boundaries are preserved

- GIVEN validation documentation or guards are updated
- WHEN reviewers inspect the change
- THEN no secrets, deployment automation, production config, CI billing fix, or runtime app behavior MUST be added.

### Requirement: Pytest Guards for Validation Wording and Artifacts

The test suite MUST include local pytest guard coverage for OpenSpec validation wording and stable artifact expectations. The guard MUST prevent wording that equates `gentle-ai sdd-status` with strict OpenSpec CLI validation and SHOULD verify repo-local OpenSpec config/archive expectations without depending on broad archive rewrites.

#### Scenario: Misleading fallback wording is detected

- GIVEN tracked documentation claims `gentle-ai sdd-status` performs strict OpenSpec CLI validation
- WHEN `py -m pytest` runs locally
- THEN the relevant guard MUST fail.

#### Scenario: Required OpenSpec expectations remain present

- GIVEN tracked OpenSpec config or documentation removes required local validation guidance
- WHEN `py -m pytest` runs locally
- THEN the relevant guard MUST fail.

### Requirement: Repo-Local Staging Handoff Checklist

Deployment documentation MUST provide a repo-local staging handoff checklist for first MVP validation. The checklist MUST state that staging uses `HYDRO_ENV=production` with staging-specific secret values supplied outside Git, and MUST NOT introduce `HYDRO_ENV=staging`, real deployment execution, server access, secret reads, env-file reads, database access, scripts, CI gates, or readiness semantics for `/healthz`.

#### Scenario: Maintainer reviews staging handoff

- GIVEN a maintainer opens the staging handoff checklist
- WHEN they inspect staging configuration guidance
- THEN `HYDRO_ENV=production` MUST be identified as the staging runtime mode
- AND staging secrets MUST be described as operator-supplied outside Git.

#### Scenario: Staging scope expansion is rejected

- GIVEN staging docs propose `HYDRO_ENV=staging`, server access, real secrets, deploy scripts, CI gates, or database reads
- WHEN deployment-readiness review runs
- THEN the change MUST be considered non-compliant until those items are removed.

### Requirement: Staging Dry-Run Checklist

Deployment documentation MUST provide a local dry-run checklist using existing local validation only. The checklist MUST include the runtime-template validator and pytest runner, and MUST remain placeholder-only, non-deploying, and repo-local.

#### Scenario: Maintainer performs dry run locally

- GIVEN the repository is checked out without real staging secrets
- WHEN the maintainer follows the dry-run checklist
- THEN they MUST be directed to run existing local validation such as `py scripts/validate_runtime_config.py` and `py -m pytest`
- AND no real env, secret, server, deployment target, or `hydro.db` access MUST be required.

#### Scenario: Dry run remains documentation-only

- GIVEN a dry-run checklist update is reviewed
- WHEN it adds scripts, deploy automation, CI gate changes, server probes, or real config reads
- THEN deployment-readiness review MUST reject it for this slice.

### Requirement: Manual Staging Validation Runbook

Deployment documentation MUST provide an operator-owned manual staging validation runbook for after an out-of-band staging deployment. The runbook MUST cover `/healthz` liveness, `/login`, authenticated `/`, Ask HYDRO citation behavior, logs, rollback, and backup confirmation without performing or automating deployment.

#### Scenario: Operator validates out-of-band staging

- GIVEN staging has already been deployed outside this repository slice
- WHEN the operator follows the manual staging runbook
- THEN they MUST validate `/healthz`, `/login`, authenticated `/`, citation-backed Ask HYDRO behavior, logs, rollback readiness, and backup confirmation.

#### Scenario: Healthz remains liveness-only

- GIVEN the runbook references `/healthz`
- WHEN reviewers inspect the staging validation steps
- THEN `/healthz` MUST be described as liveness-only
- AND it MUST NOT be treated as readiness, database, dependency, or authenticated workflow validation.

### Requirement: Pytest Guards for Staging Boundaries

The test suite MUST include local pytest static guards for staging readiness wording and boundaries. Guards MUST assert required concepts rather than brittle exact prose, including production-like staging with `HYDRO_ENV=production`, placeholder-only values, no `HYDRO_ENV=staging`, no real deployment/server/secrets/env/db access, no scripts or CI gate changes, and `/healthz` liveness-only wording.

#### Scenario: Required staging concepts are guarded

- GIVEN staging readiness documentation is changed
- WHEN `py -m pytest` runs locally
- THEN guards MUST fail if required staging handoff, dry-run, manual validation, placeholder-only, or liveness-only concepts are missing.

#### Scenario: Prohibited staging concepts are guarded

- GIVEN docs or tests introduce `HYDRO_ENV=staging`, real secret/env/db/server access, deploy automation, scripts, or CI gate changes
- WHEN `py -m pytest` runs locally
- THEN the relevant static guard MUST fail before implementation proceeds.
