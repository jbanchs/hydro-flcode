# Apply Progress: Harden Frontend Security

## Status

All tasks completed in one focused size-exception review slice under the 400-line budget.

## Completed Tasks

- [x] 1.1 Add failing assertions in `tests/test_api.py` that `/login` returns CSP, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy.
- [x] 1.2 Add failing authenticated `/` assertions in `tests/test_api.py` using the existing login helper.
- [x] 1.3 Assert CSP permits `'self'`, Tailwind CDN, CDNJS, and blocks `object-src` plus `frame-ancestors` in `tests/test_api.py`.
- [x] 2.1 Create `app/core/security_headers.py` with CSP and companion header constants.
- [x] 2.2 Add `SecurityHeadersMiddleware` in `app/core/security_headers.py` using `setdefault` so explicit future headers are preserved.
- [x] 2.3 Keep enforced `Content-Security-Policy` default; no `app/core/config.py` toggle was needed.
- [x] 3.1 Import `SecurityHeadersMiddleware` in `app/main.py`.
- [x] 3.2 Register the middleware near existing `SessionMiddleware` without changing auth, CSRF, API, router, or database behavior.
- [x] 4.1 Run `py -m pytest` and confirm existing auth, CSRF, API, and XSS guard tests still pass.
- [x] 4.2 Manually inspect `/login` and authenticated `/` templates for Tailwind CDN, CDNJS GSAP, `/static/css/styles.css`, and `/static/js/app.js` compatibility.
- [x] 4.3 Update `README.md` with security headers, interim CDN allowances, rollback, and self-hosting/build follow-up.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/test_api.py` | Integration | ✅ 14/14 API tests passing | ✅ `/login` header test written first and failed on missing CSP | ✅ Passed after middleware registration | ✅ Companion headers asserted with exact values | ✅ Extracted shared header assertion helper |
| 1.2 | `tests/test_api.py` | Integration | ✅ 14/14 API tests passing | ✅ Authenticated `/` header test written first and failed on missing CSP | ✅ Passed after middleware registration | ✅ Authenticated page path exercises session-preserving response | ✅ Reused shared login helper and header assertion helper |
| 1.3 | `tests/test_api.py` | Integration | ✅ 14/14 API tests passing | ✅ CSP directive test written first and failed on missing CSP | ✅ Passed after middleware/constants implementation | ✅ Asserted allowed sources and restrictive directives plus no wildcard script source | ✅ Extracted CSP assertion helper |
| 2.1 | `tests/test_api.py` | Integration | ✅ 14/14 API tests passing | ✅ Header/CSP tests required constants that did not exist | ✅ Passed with `CONTENT_SECURITY_POLICY` and `SECURITY_HEADERS` | ✅ Multiple directive expectations forced full policy string | ✅ Kept policy in one constants module |
| 2.2 | `tests/test_api.py` | Integration | ✅ 14/14 API tests passing | ✅ Response tests failed before middleware existed | ✅ Passed with `SecurityHeadersMiddleware` using `setdefault` | ✅ `/login` and authenticated `/` prove middleware applies across public and protected pages | ✅ Middleware remains small and behavior-focused |
| 2.3 | `tests/test_api.py` | Integration | ✅ 14/14 API tests passing | ✅ Tests required enforced `Content-Security-Policy` header | ✅ Passed without report-only toggle | ➖ Single enforcement mode by design | ✅ No unnecessary config added |
| 3.1 | `tests/test_api.py` | Integration | ✅ 14/14 API tests passing | ✅ Tests failed until middleware imported and registered | ✅ Passed after `app/main.py` import | ➖ Structural wiring task covered by response behavior tests | ✅ Import colocated with core app config imports |
| 3.2 | `tests/test_api.py` | Integration | ✅ 14/14 API tests passing | ✅ Auth/API preservation covered by existing test suite plus new page tests | ✅ Full suite passed: 30/30 | ✅ Existing auth, CSRF, API, and XSS tests remained green | ✅ No router/database/service behavior changed |
| 4.1 | `tests/test_api.py`, full suite | Integration | ✅ 14/14 API tests passing | ✅ Regression tests failed before implementation | ✅ `py -m pytest` passed: 30/30 | ✅ Existing suite validates preserved auth/API/frequency behavior | ➖ Verification task |
| 4.2 | `app/templates/login.html`, `app/templates/index.html` | Manual inspection | N/A | ✅ CSP tests encode current CDN/static requirements | ✅ Template inspection confirmed current asset origins match CSP | ✅ Login uses Tailwind; home uses Tailwind, CDNJS GSAP, `/static/css/styles.css`, `/static/js/app.js` | ➖ Documentation/inspection task |
| 4.3 | `README.md` | Documentation | N/A | ✅ Spec required interim CDN tradeoff documentation | ✅ README updated after implementation/tests | ✅ Documents current allowances, rollback, and self-host follow-up | ✅ Kept docs concise and tied to rollback |

## Test Summary

- Total tests written: 3
- Total tests passing: 30
- Layers used: Integration (3 new tests)
- Approval tests: None — no refactoring tasks
- Pure functions created: 0
- Post-review hardening: strengthened CSP assertions to parse directives exactly and reject broad `script-src https:` or wildcard allowances.

## Commands Run

- `py -m pytest tests/test_api.py` baseline: 14 passed
- `py -m pytest tests/test_api.py` RED: 3 failed, 14 passed
- `py -m pytest tests/test_api.py` GREEN: 17 passed
- `py -m pytest`: 30 passed
- `py -m pytest tests/test_api.py` post-review baseline: 17 passed
- `py -m pytest tests/test_api.py` post-review CSP hardening: 17 passed
- `py -m pytest` post-review: 30 passed

## Deviations

- `python -m pytest` was not run locally because the orchestrator required `py -m pytest` in this workspace. CI remains configured for `python -m pytest`.
- No `app/core/config.py` toggle was added because enforced CSP passed tests and no manual validation breakage was discovered.

## Workload / PR Boundary

- Mode: size-exception single focused slice
- Boundary: security header tests, middleware, app wiring, README, and OpenSpec progress only
- Review budget impact: expected to remain under the 400-line review budget
