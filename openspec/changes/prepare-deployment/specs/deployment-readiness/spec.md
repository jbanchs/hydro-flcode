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

### Requirement: SQLite Backup and Rollback Discipline

Deployment documentation MUST require a SQLite backup before destructive operations or releases and MUST describe restore/rollback expectations for production data.

#### Scenario: Rollback is planned

- GIVEN a production change may affect SQLite data
- WHEN the operator reviews rollback steps
- THEN a backup is required before proceeding
- AND restoration expectations are documented before live changes.

### Requirement: Destructive Initialization Warning

Deployment documentation MUST warn that `scripts/init_db.py` is destructive and MUST NOT be run against live production data unless backup/restore intent is explicit and accepted.

#### Scenario: Init script warning is visible

- GIVEN an operator searches deployment docs for database initialization
- WHEN they find `scripts/init_db.py`
- THEN the destructive behavior warning is prominent
- AND production use requires an explicit backup/restore decision.
