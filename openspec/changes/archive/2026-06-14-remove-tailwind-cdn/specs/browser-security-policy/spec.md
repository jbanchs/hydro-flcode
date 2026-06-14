# Delta for Browser Security Policy

## MODIFIED Requirements

### Requirement: CSP Allows Current Asset Sources Only

The CSP MUST allow HYDRO's same-origin templates and `/static` assets only for frontend script and style execution, MUST NOT allow Tailwind CDN, CDNJS, GSAP CDN loading, or broader source allowances, and SHOULD remove `style-src 'unsafe-inline'` when no inline style dependency remains.
(Previously: Tailwind CDN was explicitly allowed as interim debt and current dependencies included CDN-hosted Tailwind.)

#### Scenario: Same-origin frontend assets remain allowed without Tailwind CDN

- GIVEN a rendered HYDRO page using `/static/js/app.js` and local CSS
- WHEN the browser evaluates the CSP
- THEN same-origin script and style assets MUST be permitted by policy
- AND `https://cdn.tailwindcss.com` MUST NOT be permitted by `script-src`

#### Scenario: Dangerous browser capabilities are restricted

- GIVEN any rendered HYDRO page
- WHEN the browser evaluates the CSP
- THEN object embedding MUST be blocked
- AND framing by other origins MUST be blocked

#### Scenario: Third-party script CDNs are blocked by policy

- GIVEN a rendered HYDRO page attempts to load GSAP from CDNJS or Tailwind from its CDN
- WHEN the browser evaluates the `script-src` directive
- THEN those third-party scripts MUST be blocked by policy

#### Scenario: Inline style allowance is removed when feasible

- GIVEN templates and static JavaScript no longer require inline styles
- WHEN the CSP header is generated
- THEN `style-src` MUST be restricted to same-origin styles
- AND `style-src 'unsafe-inline'` MUST NOT be present

### Requirement: Security Header Tests

Automated tests MUST verify the configured headers on `/login` and authenticated `/`, and SHOULD assert enough CSP directives and rendered asset references to catch accidental policy weakening, including reintroducing Tailwind CDN, CDNJS, or `style-src 'unsafe-inline'`.
(Previously: Tests confirmed self/static access, Tailwind CDN allowance, and CDNJS absence.)

#### Scenario: Header regression is detected

- GIVEN the security header tests
- WHEN a required header is removed from `/login` or authenticated `/`
- THEN the test suite MUST fail

#### Scenario: CSP compatibility is documented by tests

- GIVEN the security header tests
- WHEN the CSP header is inspected
- THEN tests MUST confirm same-origin script and style access
- AND tests MUST confirm Tailwind CDN, CDNJS, and unsafe inline styles are absent when feasible

#### Scenario: Frontend no longer references external styling or animation CDNs

- GIVEN the rendered templates and static JavaScript
- WHEN tests inspect frontend asset references
- THEN they MUST find no Tailwind CDN or CDNJS GSAP script reference
- AND they MUST find no runtime dependency on `window.gsap`

### Requirement: Interim CDN Tradeoff Is Documented

Documentation MUST state that Tailwind CDN has been removed, frontend styling is served from app-owned static assets, and maintainers SHOULD validate `/login` and authenticated `/` readability after CSS changes.
(Previously: Documentation identified Tailwind CDN as remaining interim debt.)

#### Scenario: Reader sees local asset hardening guidance

- GIVEN a maintainer reading project documentation
- WHEN they review frontend security notes
- THEN they MUST see Tailwind CDN described as removed
- AND they MUST see local static CSS and manual readability checks documented

## ADDED Requirements

### Requirement: Local CSS Preserves Usable UI

Rendered pages MUST serve equivalent app-owned CSS for current login, authenticated home, and JavaScript-created UI states, preserving readability and key layout behavior without a frontend build pipeline.

#### Scenario: Login page remains usable with local CSS

- GIVEN an unauthenticated client
- WHEN the client requests `/login`
- THEN the page MUST load local CSS without Tailwind CDN
- AND the login form MUST remain readable and operable

#### Scenario: Authenticated UI remains usable with local CSS

- GIVEN an authenticated client
- WHEN the client requests `/` and interacts with dynamic UI states
- THEN static and JavaScript-created elements MUST remain readable and distinguishable
- AND no third-party CSS runtime MUST be required
