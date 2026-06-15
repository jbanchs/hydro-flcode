# Delta for Browser Security Policy

## MODIFIED Requirements

### Requirement: Security Headers on Rendered Pages and Public Liveness Responses

Rendered application pages and the public `/healthz` liveness response MUST include a Content-Security-Policy or explicitly configured Content-Security-Policy-Report-Only header, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy.
(Previously: Required security headers only for rendered application pages.)

#### Scenario: Public login response includes headers

- GIVEN an unauthenticated client
- WHEN the client requests `/login`
- THEN the response MUST include the configured browser security headers
- AND the response MUST remain renderable as the login page

#### Scenario: Authenticated home response includes headers

- GIVEN an authenticated client
- WHEN the client requests `/`
- THEN the response MUST include the configured browser security headers
- AND the response MUST remain renderable as the authenticated app page

#### Scenario: Public liveness response includes headers

- GIVEN an unauthenticated client
- WHEN the client requests `GET /healthz`
- THEN the response MUST include the configured browser security headers
- AND the response MUST remain static non-sensitive JSON.

## ADDED Requirements

### Requirement: Health Endpoint Header Regression Coverage

Automated tests MUST verify `/healthz` inherits the same required security-header policy expected for public browser-facing responses without changing its unauthenticated liveness semantics.

#### Scenario: Missing health headers are detected

- GIVEN the security header tests
- WHEN a required header is removed from `/healthz`
- THEN the test suite MUST fail
- AND `/healthz` MUST still be tested as unauthenticated and non-redirecting.
