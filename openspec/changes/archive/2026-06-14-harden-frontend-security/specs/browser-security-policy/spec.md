# Browser Security Policy Specification

## Purpose

Define browser-enforced response security protections for HYDRO rendered pages while preserving current authentication, API, CDN, and static asset behavior.

## Requirements

### Requirement: Security Headers on Rendered Pages

Rendered application pages MUST include a Content-Security-Policy or explicitly configured Content-Security-Policy-Report-Only header, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy.

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

### Requirement: CSP Allows Current Asset Sources Only

The CSP MUST allow HYDRO's current same-origin templates, `/static` assets, Tailwind CDN, and CDNJS GSAP usage, and MUST avoid broader source allowances unless required by the current UI.

#### Scenario: Current frontend dependencies remain allowed

- GIVEN a rendered HYDRO page using Tailwind CDN, CDNJS GSAP, and `/static/js/app.js`
- WHEN the browser evaluates the CSP
- THEN those current dependencies MUST be permitted by policy
- AND no unrelated CDN wildcard SHOULD be allowed

#### Scenario: Dangerous browser capabilities are restricted

- GIVEN any rendered HYDRO page
- WHEN the browser evaluates the CSP
- THEN object embedding MUST be blocked
- AND framing by other origins MUST be blocked

### Requirement: Auth and API Behavior Is Preserved

Security headers MUST NOT change authentication redirects, session cookies, CSRF behavior, or API response semantics.

#### Scenario: Unauthenticated access still redirects

- GIVEN an unauthenticated client
- WHEN the client requests an authenticated page
- THEN the existing authentication redirect behavior MUST be preserved
- AND security headers MAY be present on the response

#### Scenario: Existing API tests remain valid

- GIVEN the existing API and XSS guard test suite
- WHEN `py -m pytest` runs locally, or CI runs `python -m pytest`
- THEN existing auth, CSRF, and XSS expectations MUST continue to pass

### Requirement: Security Header Tests

Automated tests MUST verify the configured headers on `/login` and authenticated `/`, and SHOULD assert enough CSP directives to catch accidental policy weakening.

#### Scenario: Header regression is detected

- GIVEN the security header tests
- WHEN a required header is removed from `/login` or authenticated `/`
- THEN the test suite MUST fail

#### Scenario: CSP compatibility is documented by tests

- GIVEN the security header tests
- WHEN the CSP header is inspected
- THEN tests MUST confirm self/static access and current CDN allowances
- AND tests SHOULD confirm restrictive directives such as object-src and frame-ancestors

### Requirement: Interim CDN Tradeoff Is Documented

Documentation MUST state that Tailwind CDN and CDNJS allowances are interim, and production hardening SHOULD self-host or build frontend assets in a follow-up change.

#### Scenario: Reader sees follow-up hardening guidance

- GIVEN a maintainer reading project documentation
- WHEN they review frontend security notes
- THEN they MUST see the interim CDN tradeoff
- AND they SHOULD see the recommended self-hosting/build follow-up
