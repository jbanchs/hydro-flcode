# Delta for Deployment Readiness

## MODIFIED Requirements

### Requirement: SQLite Backup and Rollback Discipline

Deployment documentation MUST require a SQLite backup before destructive operations or releases and MUST describe manual restore rehearsal, rollback boundaries, and production-data protection using placeholder-only commands and paths. The documentation MUST NOT access live `hydro.db`, real environment files, secrets, ignored sensitive notes, servers, or production data, and MUST NOT add destructive automation.
(Previously: Required backup before destructive operations/releases and documented restore/rollback expectations at a high level.)

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

### Requirement: Production Operations Checklist

The system MUST provide documentation covering SQLite absolute data path guidance, ownership expectations, pre-deploy backup, manual restore rehearsal, rollback boundaries, destructive initialization warnings, logging inspection, firewall checklist, and explicit scope boundaries. The documentation MUST use placeholder-only commands/paths and MUST NOT perform deployment, provision servers, add CI/CD deploy jobs, add one-shot deploy scripts, access real databases/secrets/servers, or introduce destructive automation.
(Previously: Covered SQLite path, ownership, backup/restore and rollback checks, destructive warnings, logs, firewall, and non-secret operational boundaries.)

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

### Requirement: Pytest Guards for Runtime Config Validation

The test suite MUST include local pytest guards for runtime template parity, placeholder-only validation, boundary wording, and prohibited real-env/server/deploy access. These guards MUST run with the existing local pytest runner and MUST fail if SQLite backup/restore docs omit required safety wording, include non-placeholder commands/paths, read real `hydro.db`, env files, secrets, ignored sensitive notes, or servers, or introduce backup/restore automation.
(Previously: Guarded runtime templates, placeholder-only validation, boundary wording, and prohibited real-env/server/deploy access.)

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
