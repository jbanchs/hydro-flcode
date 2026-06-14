# Proposal: Harden Frontend Security

## Intent

Add response-level browser protections for HYDRO's FastAPI/Jinja2 app. The current frontend has XSS static guards, CSRF checks, and secure session settings, but no CSP or companion security headers. This slice improves browser-enforced safety without changing asset delivery yet.

## Scope

### In Scope
- Add global FastAPI/Starlette middleware for security headers.
- Define a pragmatic CSP compatible with Tailwind CDN, CDNJS GSAP, `/static`, and current templates.
- Add pytest integration coverage for headers on `/login` and authenticated `/`.
- Document that CDN allowances are interim and production hardening requires self-hosted assets.

### Out of Scope
- Replacing Tailwind CDN with a local CSS build.
- Vendoring/self-hosting GSAP unless CSP validation proves it is required.
- CSP nonce/hash plumbing; current templates do not use inline scripts.

## Capabilities

### New Capabilities
- `browser-security-policy`: Browser response security headers and CSP behavior for rendered app pages.

### Modified Capabilities
- None

## Approach

Add a small configurable middleware near app startup. Start with `default-src 'self'`, `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'none'`, `form-action 'self'`, local `connect-src`, and explicit `script-src` allowances for Tailwind CDN, CDNJS GSAP, and self/static scripts. Include `X-Content-Type-Options`, `Referrer-Policy`, and conservative `Permissions-Policy`. Prefer an enforceable policy if current pages remain functional; otherwise use/report a clearly configured report-only mode.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `app/main.py` | Modified | Register global security header middleware. |
| `app/core/config.py` | Modified | Add policy/config toggles if needed. |
| `app/templates/*.html` | Modified | Validate current CDN/script usage against CSP; avoid broadening scope. |
| `tests/test_api.py` | Modified | Assert headers and preserve frontend XSS guards. |
| `README.md` | Modified | Document interim CDN tradeoffs and follow-up hardening. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| CSP breaks Tailwind CDN runtime style behavior | Med | Validate pages and keep first policy pragmatic. |
| CDN script trust remains | Med | Document as interim; defer self-hosting to follow-up PR. |
| Header tests miss browser runtime failures | Med | Keep policy simple and call out lack of E2E coverage. |

## Rollback Plan

Revert the middleware/config/tests/docs change as one work unit. Since no persisted data or regulatory citation behavior changes, rollback restores prior response behavior immediately.

## Dependencies

- Current Tailwind CDN and CDNJS GSAP usage remains accepted for this slice.
- Local test runner: `py -m pytest`; CI test runner: `python -m pytest`.

## Success Criteria

- [ ] `/login` and authenticated `/` include the agreed CSP/security headers.
- [ ] Current pages continue loading Tailwind, GSAP, and `/static/js/app.js`.
- [ ] Existing XSS static guard coverage remains intact.
- [ ] Follow-up self-hosting/build hardening is documented, not implemented.
