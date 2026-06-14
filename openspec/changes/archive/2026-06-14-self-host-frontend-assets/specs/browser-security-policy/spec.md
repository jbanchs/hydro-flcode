# Delta for Browser Security Policy

## MODIFIED Requirements

### Requirement: CSP Allows Current Asset Sources Only

The CSP MUST allow HYDRO's current same-origin templates, `/static` assets, and Tailwind CDN usage, MUST NOT allow CDNJS or GSAP script loading, and MUST avoid broader source allowances unless required by the current UI.
(Previously: CSP allowed Tailwind CDN and CDNJS GSAP as current frontend dependencies.)

#### Scenario: Current frontend dependencies remain allowed without CDNJS

- GIVEN a rendered HYDRO page using Tailwind CDN and `/static/js/app.js`
- WHEN the browser evaluates the CSP
- THEN those current dependencies MUST be permitted by policy
- AND `https://cdnjs.cloudflare.com` MUST NOT be permitted by `script-src`

#### Scenario: Dangerous browser capabilities are restricted

- GIVEN any rendered HYDRO page
- WHEN the browser evaluates the CSP
- THEN object embedding MUST be blocked
- AND framing by other origins MUST be blocked

#### Scenario: GSAP from CDNJS is blocked by policy

- GIVEN a rendered HYDRO page attempts to load GSAP from CDNJS
- WHEN the browser evaluates the `script-src` directive
- THEN the CDNJS GSAP script MUST be blocked by policy
- AND Tailwind CDN MUST remain explicitly allowed as interim debt

### Requirement: Security Header Tests

Automated tests MUST verify the configured headers on `/login` and authenticated `/`, and SHOULD assert enough CSP directives to catch accidental policy weakening, including reintroducing CDNJS in `script-src`.
(Previously: Tests confirmed self/static access and current CDN allowances, including CDNJS.)

#### Scenario: Header regression is detected

- GIVEN the security header tests
- WHEN a required header is removed from `/login` or authenticated `/`
- THEN the test suite MUST fail

#### Scenario: CSP compatibility is documented by tests

- GIVEN the security header tests
- WHEN the CSP header is inspected
- THEN tests MUST confirm self/static access and Tailwind CDN allowance
- AND tests MUST confirm CDNJS is absent from `script-src`

#### Scenario: Frontend no longer references GSAP CDN

- GIVEN the rendered authenticated app template and static JavaScript
- WHEN tests inspect frontend asset references
- THEN they MUST find no CDNJS GSAP script reference
- AND they MUST find no runtime dependency on `window.gsap`

### Requirement: Interim CDN Tradeoff Is Documented

Documentation MUST state that Tailwind CDN is an interim allowance, CDNJS/GSAP has been removed, and production hardening SHOULD self-host or build remaining frontend assets in a follow-up change.
(Previously: Documentation stated both Tailwind CDN and CDNJS allowances were interim.)

#### Scenario: Reader sees follow-up hardening guidance

- GIVEN a maintainer reading project documentation
- WHEN they review frontend security notes
- THEN they MUST see Tailwind CDN identified as remaining interim debt
- AND they MUST see CDNJS/GSAP described as removed from this slice
