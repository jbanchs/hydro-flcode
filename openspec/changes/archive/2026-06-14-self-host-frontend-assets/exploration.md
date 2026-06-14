## Exploration: self-host-frontend-assets

### Current State
HYDRO is a small FastAPI/Jinja2 app with static assets mounted under `/static` and no application `package.json` or frontend bundler detected. The only Python/runtime dependencies are in `requirements.txt`; `.opencode` package files are tool-local and should not be treated as app dependencies.

The current CSP is enforced in `app/core/security_headers.py` and allows `script-src 'self' https://cdn.tailwindcss.com https://cdnjs.cloudflare.com` plus `style-src 'self' 'unsafe-inline'`. `app/templates/login.html` and `app/templates/index.html` both load Tailwind from `https://cdn.tailwindcss.com`; `index.html` also loads GSAP from CDNJS before `/static/js/app.js`. The local app script uses `gsap.from(...)` only for an entrance animation, then uses safe DOM APIs (`textContent`, `replaceChildren`, `createElement`) for search and HYDRO answer rendering.

Tests already parse CSP directives and assert the interim CDN allowances in `tests/test_api.py`; they also include a static frontend XSS guard. The archived `harden-frontend-security` change and README explicitly document these CDN allowances as technical debt to remove in a follow-up.

### Affected Areas
- `app/templates/login.html` — loads Tailwind CDN and relies heavily on Tailwind utility classes for layout and styling.
- `app/templates/index.html` — loads Tailwind CDN, CDNJS GSAP, and local `/static/js/app.js`; also contains many Tailwind utility classes.
- `app/static/js/app.js` — has a hard dependency on global `gsap` for a non-essential animation.
- `app/static/css/styles.css` — currently tiny; could expand into the app-owned stylesheet if avoiding a build tool.
- `app/core/security_headers.py` — CSP source list must tighten after CDN/runtime style dependencies are removed.
- `tests/test_api.py` — CSP assertions must change from interim allowances to strict self-hosted expectations, and template/static asset assertions should prove CDN references are gone.
- `README.md` and `openspec/specs/browser-security-policy/spec.md` — documentation/specs currently describe CDN allowances as interim and would need follow-up updates.
- `requirements.txt` / package config — no frontend build dependencies exist today; introducing Tailwind CLI/npm would create new dependency and CI concerns.

### Approaches
1. **Remove GSAP, keep Tailwind CDN temporarily** — Delete the CDNJS script and replace the single `gsap.from(...)` call with no animation or a small CSS transition.
   - Pros: smallest safe slice; removes one third-party script origin; reduces runtime failure/offline risk; likely well under the 400-line review budget; easy to verify with template/CSP tests.
   - Cons: Tailwind CDN and `style-src 'unsafe-inline'` remain; CSP is improved but not fully hardened; UI loses or simplifies one animation.
   - Effort: Low

2. **Vendor/self-host GSAP, keep Tailwind CDN temporarily** — Add a pinned `app/static/vendor/gsap.min.js`, load it locally, and remove CDNJS from CSP.
   - Pros: preserves current animation behavior; removes CDNJS network/supply-chain dependency at runtime; CSP can drop `https://cdnjs.cloudflare.com`.
   - Cons: vendored minified code increases review noise and maintenance burden; license/update tracking becomes explicit; Tailwind CDN still prevents strict CSP; offline behavior still depends on Tailwind.
   - Effort: Medium

3. **Replace Tailwind CDN with handcrafted static CSS** — Move the limited current utility usage into app-owned CSS classes in `app/static/css/styles.css`, update templates to semantic classes, and remove Tailwind CDN.
   - Pros: no new build tool; strongest small-app offline behavior; CSP can become `script-src 'self'` and `style-src 'self'`; review remains understandable if split from GSAP work.
   - Cons: template churn is larger because many utility classes must be replaced; visual regression risk without browser E2E/screenshot tests; future design iteration loses Tailwind utility ergonomics.
   - Effort: Medium

4. **Introduce Tailwind build pipeline** — Add an app-owned package/build setup to compile Tailwind CSS into static CSS, then remove Tailwind CDN.
   - Pros: preserves Tailwind authoring model; production CSS can be self-hosted; long-term frontend workflow scales better if the UI grows.
   - Cons: adds npm/toolchain dependency to a Python-only app; more CI/config/documentation surface; likely exceeds a small review slice when combined with CSP/test/doc changes; `.opencode` package files must be ignored as app packages.
   - Effort: High

### Recommendation
Use chained, reviewable slices. The smallest safe proposal should remove GSAP rather than vendor it: the current GSAP usage is one non-essential animation, so deleting or replacing it avoids importing a vendored minified dependency while immediately allowing CSP to drop `https://cdnjs.cloudflare.com`. Update tests to assert CDNJS is absent from templates and CSP, while documenting that Tailwind remains the only interim external frontend dependency.

Handle Tailwind in a second proposal/slice. For HYDRO's current small UI and no bundler, prefer handcrafted static CSS over introducing a Tailwind build pipeline unless the product needs ongoing utility-first design work. That second slice can replace Tailwind CDN, migrate the limited templates to app-owned CSS, tighten CSP to `script-src 'self'` and `style-src 'self'`, and add tests proving no CDN URLs remain in rendered templates/security policy.

This sequencing respects the forced chained PR strategy and 400-line review budget: PR 1 removes GSAP/CDNJS and tightens CSP narrowly; PR 2 removes Tailwind CDN and `unsafe-inline` with visual/manual validation notes.

### Risks
- Removing GSAP may slightly change page polish, but the animation is not functional behavior.
- Vendoring GSAP would preserve behavior but adds minified third-party code that is poor review material and needs license/update tracking.
- Replacing Tailwind with handcrafted CSS can produce visual regressions because no E2E or screenshot testing is detected.
- Introducing a build tool increases CI/dependency complexity for a currently Python-only app.
- Tests can prove CSP/template references, but browser-level CSP/rendering compatibility still needs manual validation without Playwright/Cypress/Selenium.

### Ready for Proposal
Yes — propose the first chained slice as GSAP removal/CDNJS CSP hardening only. Tell the user Tailwind removal should follow as a separate slice, with a likely static CSS migration unless they explicitly want to adopt a frontend build pipeline.
