# Proposal: Remove Tailwind CDN

## Intent

Remove HYDRO's runtime dependency on `https://cdn.tailwindcss.com` so rendered pages use app-owned static assets and the browser CSP can be tightened for production hardening.

## Scope

### In Scope
- Replace current Tailwind utility-dependent styling in `login.html`, `index.html`, and JS-created UI with local static CSS/custom classes.
- Remove Tailwind CDN script tags from rendered templates.
- Tighten CSP to `script-src 'self'` and `style-src 'self'` if validation confirms no inline styles remain.
- Update pytest assertions, README security notes, and manual visual-check expectations.

### Out of Scope
- Introducing Node, Tailwind CLI, PostCSS, or a frontend build pipeline.
- Redesigning the UI beyond preserving current layout/visual behavior.
- Adding browser E2E or visual regression tooling.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `browser-security-policy`: remove interim Tailwind CDN and unsafe-inline style allowances; require same-origin frontend assets only.

## Approach

Use the exploration recommendation: translate the small current Tailwind surface into app-owned CSS in `/static/css/styles.css`, including classes used dynamically by `/static/js/app.js`. Make security tests fail first for CDN/unsafe-inline allowances, then remove script references, map styles locally, tighten CSP, and document manual screenshots for `/login` and authenticated `/`.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `app/templates/login.html` | Modified | Remove Tailwind CDN and use local CSS classes. |
| `app/templates/index.html` | Modified | Remove Tailwind CDN while preserving page layout. |
| `app/static/css/styles.css` | Modified | Add custom CSS replacing utility usage. |
| `app/static/js/app.js` | Modified | Replace dynamic Tailwind utility strings with local class names. |
| `app/core/security_headers.py` | Modified | Restrict CSP script/style sources to self when feasible. |
| `tests/test_api.py` | Modified | Assert no Tailwind CDN or unsafe-inline CSP dependency. |
| `README.md` | Modified | Document local static asset strategy and visual checks. |
| `openspec/specs/browser-security-policy/spec.md` | Modified | Update source requirements after archive. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Visual regressions from manual CSS translation | Med | Require before/after browser screenshots for `/login` and `/`. |
| Missing styles for JS-created elements | Med | Audit `app.js` class usage and cover representative interactions manually. |
| CSP too strict for current rendering | Low | Tighten only after confirming no inline style dependency remains. |

## Rollback Plan

Revert the proposal's implementation commit(s): restore Tailwind CDN script tags, previous CSP allowances, old tests, and README notes. No data migration or regulatory citation behavior changes are involved.

## Dependencies

- Existing `browser-security-policy` spec.
- `python -m pytest` for automated verification.
- Manual browser screenshot comparison due no E2E/visual tooling.

## Success Criteria

- [ ] Rendered templates and static JS contain no `cdn.tailwindcss.com` reference.
- [ ] CSP no longer allows third-party script sources or `style-src 'unsafe-inline'`, unless infeasible and documented.
- [ ] `/login` and authenticated `/` remain visually usable with local CSS.
- [ ] `python -m pytest` passes.
