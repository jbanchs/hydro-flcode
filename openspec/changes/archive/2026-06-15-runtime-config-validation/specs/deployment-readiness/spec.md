# Delta for Deployment Readiness

## ADDED Requirements

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

The test suite MUST include local pytest guards for runtime template parity, placeholder-only validation, boundary wording, and prohibited real-env/server/deploy access. These guards MUST run with the existing local pytest runner.

#### Scenario: Validator regressions are detected

- GIVEN the validator stops enforcing required template parity or placeholder-only sensitive values
- WHEN `py -m pytest` runs locally
- THEN the relevant guard MUST fail.

#### Scenario: Boundary regressions are detected

- GIVEN docs or validator behavior imply real environment access, deployment automation, server access, or full production readiness
- WHEN `py -m pytest` runs locally
- THEN the relevant guard MUST fail.

### Requirement: Deferred Startup Fail-Closed Expansion

The system MUST NOT add new app startup fail-closed production checks for this slice beyond existing guards. Additional startup enforcement SHALL be deferred until HYDRO has a reliable production-mode signal.

#### Scenario: Runtime validation does not change app startup

- GIVEN the local template validator is added
- WHEN HYDRO application startup behavior is reviewed
- THEN no new production-mode fail-closed checks MUST be introduced by this slice.

#### Scenario: Reliable production signal is missing

- GIVEN a proposed startup guard depends on an unreliable or ambiguous production-mode signal
- WHEN the proposal is reviewed
- THEN the guard MUST be deferred to a future change.
