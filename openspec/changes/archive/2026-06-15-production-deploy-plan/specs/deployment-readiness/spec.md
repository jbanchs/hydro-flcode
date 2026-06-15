# Delta for Deployment Readiness

## ADDED Requirements

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

The system MUST provide documentation covering SQLite absolute data path guidance, ownership expectations, backup/restore and rollback checks, destructive initialization warnings, logging inspection, firewall checklist, and explicit scope boundaries. The documentation MUST NOT perform deployment, provision servers, add CI/CD deploy jobs, add one-shot deploy scripts, or introduce real secrets.

#### Scenario: Operator prepares manually

- GIVEN an operator is preparing a later production deployment
- WHEN they read the operations checklist
- THEN they can identify data path, ownership, backup, rollback, logs, firewall, TLS, and service-user checks
- AND they understand validation remains manual and environment-specific.

#### Scenario: Automation remains out of scope

- GIVEN a change proposes SSH commands, server provisioning, CI/CD deployment, backup scripts, or one-shot deploy automation
- WHEN it is reviewed against deployment readiness
- THEN the change MUST be rejected for this slice
- AND the documentation MUST keep the scope as non-secret templates and guidance only.
