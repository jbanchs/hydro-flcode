# Tasks: Harden Frontend Security

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 180-280 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single focused slice despite force-chained preference |
| Delivery strategy | force-chained |
| Chain strategy | size-exception |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: size-exception
400-line budget risk: Low

This change is small enough for one review slice: middleware, registration, tests, and README are tightly coupled and should remain together for rollback clarity.

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Add browser security headers with regression tests and docs | PR 1 | Single slice under 400 lines; tests/docs included with behavior |

## Phase 1: Test-First Coverage

- [x] 1.1 Add failing assertions in `tests/test_api.py` that `/login` returns CSP, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy.
- [x] 1.2 Add failing authenticated `/` assertions in `tests/test_api.py` using the existing login helper.
- [x] 1.3 Assert CSP permits `'self'`, Tailwind CDN, CDNJS, and blocks `object-src` plus `frame-ancestors` in `tests/test_api.py`.

## Phase 2: Middleware Implementation

- [x] 2.1 Create `app/core/security_headers.py` with CSP and companion header constants.
- [x] 2.2 Add `SecurityHeadersMiddleware` in `app/core/security_headers.py` using `setdefault` so explicit future headers are preserved.
- [x] 2.3 Keep enforced `Content-Security-Policy` default; only add `app/core/config.py` toggle if tests/manual validation require report-only mode.

## Phase 3: App Wiring

- [x] 3.1 Import `SecurityHeadersMiddleware` in `app/main.py`.
- [x] 3.2 Register the middleware near existing `SessionMiddleware` without changing auth, CSRF, API, router, or database behavior.

## Phase 4: Verification and Documentation

- [x] 4.1 Run `py -m pytest` locally and confirm existing auth, CSRF, API, and XSS guard tests still pass. CI remains configured for `python -m pytest`.
- [x] 4.2 Manually inspect `/login` and authenticated `/` for Tailwind CDN, CDNJS GSAP, `/static/css/styles.css`, and `/static/js/app.js` compatibility.
- [x] 4.3 Update `README.md` with security headers, interim CDN allowances, rollback, and self-hosting/build follow-up.
