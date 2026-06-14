## Exploration: harden-frontend-security

### Current State
HYDRO is a small FastAPI/Jinja2 app with static assets mounted at `/static`. Session security is already configured through `SessionMiddleware` with `same_site="lax"`, configurable secure cookies, and CSRF validation for login/logout. A prior XSS hardening pass removed unsafe frontend HTML injection patterns; `app/static/js/app.js` now builds DOM nodes with `textContent` and `replaceChildren`, and `tests/test_api.py` includes a static guard against `innerHTML`, `eval`, string timers, inline event attributes, and `javascript:` URLs.

The remaining browser hardening gap is response-level policy. Templates currently load Tailwind from `https://cdn.tailwindcss.com` on both pages, GSAP from `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js` on the authenticated index page, and local `/static/js/app.js`. There is no CSP or related security header middleware today. Tailwind CDN is especially important because it injects runtime styles and commonly requires relaxed CSP allowances such as external script access and inline style behavior.

### Affected Areas
- `app/main.py` — best insertion point for FastAPI/Starlette middleware that adds security headers globally.
- `app/core/config.py` — likely place for environment toggles such as CSP mode, dev/prod policy, and optional report-only behavior.
- `app/templates/index.html` — loads Tailwind CDN, CDNJS GSAP, local app JavaScript, and depends on Tailwind utility classes.
- `app/templates/login.html` — loads Tailwind CDN and would be affected by any CSP `script-src` / `style-src` restrictions.
- `app/static/js/app.js` — depends on global `gsap`; may need graceful behavior if GSAP is removed, self-hosted, or blocked by CSP.
- `tests/test_api.py` — existing integration/static security tests can be extended to assert security headers and keep the XSS guard.
- `README.md` / deployment notes — may need to document production CSP expectations and CDN/self-hosting tradeoffs.

### Approaches
1. **Pragmatic CSP with current CDNs** — Add security headers and a CSP that permits the existing Tailwind CDN, CDNJS GSAP, local static assets, and minimal required style behavior.
   - Pros: smallest implementation; preserves current UI; fast to test with FastAPI `TestClient`; good immediate hardening over no policy.
   - Cons: still trusts third-party CDNs; Tailwind CDN may require relaxed `style-src` behavior; supply-chain and availability risks remain.
   - Effort: Low

2. **Self-host GSAP, keep Tailwind CDN temporarily** — Vendor or serve GSAP locally while retaining Tailwind CDN during the prototype phase; CSP allows local scripts plus Tailwind CDN only.
   - Pros: reduces one third-party runtime dependency; avoids breaking Tailwind-heavy templates; practical midpoint for a small app.
   - Cons: Tailwind CDN still weakens CSP; requires tracking GSAP updates if vendored; not a fully locked-down production policy.
   - Effort: Medium

3. **Production-grade self-hosted assets with strict CSP** — Replace Tailwind CDN with a build/self-hosted CSS artifact and self-host or remove GSAP; use strict `default-src 'self'`, `script-src 'self'`, and no CDN allowances.
   - Pros: strongest security posture; removes runtime Tailwind compiler and third-party script trust; simpler long-term CSP.
   - Cons: introduces frontend build/package workflow or generated CSS process; higher review and maintenance cost; likely larger than a small hardening change.
   - Effort: High

4. **Nonce/hash CSP for templates** — Generate per-request nonces or static hashes for scripts/styles and wire them into templates.
   - Pros: useful if inline scripts/styles become necessary; can support stricter policies without broad `'unsafe-inline'`.
   - Cons: current templates have no inline scripts; Tailwind CDN/runtime style behavior is the harder constraint; nonce plumbing adds complexity without much benefit right now.
   - Effort: Medium

### Recommendation
Proceed with a phased, pragmatic change. For `harden-frontend-security`, add a small security headers middleware and tests first, using a report-only or enforceable CSP compatible with the current app: `default-src 'self'`, restricted `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'none'`, `form-action 'self'`, local `connect-src`, and explicit script allowances for Tailwind CDN, CDNJS GSAP, and `/static`. Include companion headers such as `X-Content-Type-Options: nosniff`, `Referrer-Policy`, and a conservative permissions policy.

Document that this is an interim CSP because Tailwind CDN and CDNJS require trusting third-party scripts. The next production-hardening step should be self-hosting/removing GSAP and replacing Tailwind CDN with a local CSS build, then tightening CSP to mostly `'self'`. Do not start with nonce/hash plumbing unless inline scripts are introduced; it is architectural overhead without solving the current CDN trust problem.

Testing should stay small and TDD-friendly: add FastAPI integration tests asserting the security headers on `/login` and authenticated `/`, ensure static assets are still served, and keep/extend the existing frontend static XSS guard. If CSP is report-only in development, tests should assert the chosen dev/prod behavior explicitly through config/environment variables.

For review workload, this should remain under the 400-line budget if limited to middleware/config/tests/docs. If asset self-hosting or Tailwind build setup is included, split it into a chained follow-up PR because that changes frontend delivery rather than only browser policy.

### Risks
- A strict CSP can break Tailwind CDN because it executes runtime JavaScript and may inject styles; the initial policy must be validated against actual pages.
- Allowing Tailwind CDN and CDNJS in `script-src` improves observability/control but does not remove third-party script supply-chain risk.
- Adding nonces/hashes too early may create complexity while still requiring CDN allowances.
- Production and local development may need different behavior; mismatched defaults could either break local iteration or silently ship a weak production policy.
- Tests can prove headers exist, but without browser E2E they cannot fully prove runtime CSP compatibility.

### Ready for Proposal
Yes — propose a small FastAPI security headers/CSP change with explicit interim CDN allowances, tests for headers and existing XSS guard coverage, and documentation that stricter production hardening requires a later asset self-hosting/build step.
