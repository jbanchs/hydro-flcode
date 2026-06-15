# Delta for Deployment Readiness

## ADDED Requirements

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

## REMOVED Requirements

### Requirement: Deferred Startup Fail-Closed Expansion

(Reason: HYDRO now has an explicit `HYDRO_ENV=production` signal, so narrow production-only startup enforcement is no longer deferred.)
(Migration: Replace deferred behavior with explicit production signal and fail-closed runtime checks.)
