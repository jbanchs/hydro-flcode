# Delta for Deployment Readiness

## ADDED Requirements

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
