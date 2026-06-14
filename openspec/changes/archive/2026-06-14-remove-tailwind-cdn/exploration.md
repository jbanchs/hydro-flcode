## Exploration: remove-tailwind-cdn

### Current State
HYDRO is a FastAPI/Jinja2 app with two rendered templates and app-owned static assets. `app/templates/login.html` and `app/templates/index.html` both load `https://cdn.tailwindcss.com`, while `index.html` also loads `/static/css/styles.css` and `/static/js/app.js`. CSP is enforced in `app/core/security_headers.py` as `script-src 'self' https://cdn.tailwindcss.com` and `style-src 'self' 'unsafe-inline'`; tests in `tests/test_api.py` intentionally assert those interim allowances. There is no application bundler or app package configuration; `.opencode/package.json` is tooling-only, not part of HYDRO delivery.

### Affected Areas
- `app/templates/login.html` — removes Tailwind CDN script and either replaces utility-class dependency with local CSS classes or points to a local generated stylesheet.
- `app/templates/index.html` — same Tailwind dependency plus existing `/static/css/styles.css`; dynamic table/UI classes must remain styled after CDN removal.
- `app/static/css/styles.css` — likely home for hand-written static CSS if using the smallest safe slice; currently only defines `.input`.
- `app/static/js/app.js` — creates elements with Tailwind utility class strings; these must map to CSS classes or remain valid if vendored/generated CSS includes them.
- `app/core/security_headers.py` — tightens CSP to remove Tailwind from `script-src` and, if no inline styles remain, change `style-src` to `'self'` only.
- `tests/test_api.py` — update CSP assertions and asset-reference tests to require no third-party frontend scripts and no `style-src 'unsafe-inline'`; pytest remains the available CI verification.
- `README.md` — update browser security notes to remove Tailwind interim-debt language and document the chosen local asset strategy.
- `openspec/specs/browser-security-policy/spec.md` — current source spec still permits Tailwind CDN as interim debt; proposal/spec phases should modify it.

### Approaches
1. **Replace Tailwind utilities with static CSS** — Remove the CDN script and convert the small set of utility-driven layouts/colors/spacing into app-owned CSS classes/selectors in `/static/css/styles.css`.
   - Pros: smallest dependency footprint; no app build pipeline; enables `script-src 'self'` and likely `style-src 'self'`; aligns with current static FastAPI app.
   - Cons: visual regression risk from translating many utility classes; manual CSS maintenance; responsive variants like `lg:`/`xl:` and arbitrary grid values need careful mapping.
   - Effort: Medium

2. **Introduce a Tailwind build pipeline** — Add real app package config, Tailwind CLI/PostCSS input, generated CSS output, and CI/build steps.
   - Pros: preserves Tailwind class authoring model; generated CSS can satisfy strict CSP with no CDN script or unsafe inline styles.
   - Cons: adds Node/toolchain complexity to an otherwise Python/static app; CI/deployment must install/build frontend assets; larger scope than needed for two templates.
   - Effort: High

3. **Vendor generated Tailwind CSS artifact** — Generate the needed Tailwind CSS once and commit it under `/static/css`, keeping utility classes in templates/JS.
   - Pros: avoids runtime CDN and avoids introducing mandatory CI build; low template churn; CSP can become self-only for scripts/styles.
   - Cons: generated artifact provenance/update process must be documented; risk of stale CSS when utility classes change, especially JS-created classes; CSS file may be larger than hand-written equivalent.
   - Effort: Medium

4. **Self-host Tailwind CDN script locally** — Download/serve the browser Tailwind script from `/static`.
   - Pros: minimal template churn; removes third-party script origin.
   - Cons: keeps runtime style injection and likely preserves `style-src 'unsafe-inline'`; still uses CDN-oriented prototyping mode; weakest CSP outcome.
   - Effort: Low

### Recommendation
Use **Replace Tailwind utilities with static CSS** as the smallest safe production-hardening slice. The UI surface is small enough to translate manually, and this avoids adding a Node/Tailwind build system to a Python/FastAPI app just to support two templates. The implementation should be test-first: update CSP/asset-reference tests to fail on Tailwind CDN and `unsafe-inline`, then remove the script tags, add local CSS coverage for template and JS-generated classes, and tighten CSP to `script-src 'self'` and `style-src 'self'`. Because there is no browser E2E or visual regression tooling, require manual before/after browser screenshots for `/login` and authenticated `/` during verification.

### Risks
- Manual utility-to-CSS translation can subtly change spacing, breakpoints, colors, shadows, focus rings, and table overflow behavior.
- Existing automated tests can prove CSP/header and string-level asset constraints, but cannot prove visual parity without browser/E2E or screenshot tooling.
- `app/static/js/app.js` assigns Tailwind-like class strings dynamically; missing CSS mappings would only appear after search/ask interactions.
- Adding a Tailwind build pipeline would exceed the smallest safe slice and may push the change beyond the 400-line review budget.

### Ready for Proposal
Yes — propose a focused frontend hardening change that removes Tailwind CDN by replacing current utility usage with local static CSS, tightens CSP to self-only scripts and styles if validation confirms no inline styles are needed, updates pytest CSP/static-reference tests, documents manual visual checks, and defers any Tailwind build pipeline unless future UI growth justifies it.
