# Proposal: Self-Host Frontend Assets Slice 1

## Intent

Reduce HYDRO's third-party frontend script surface by removing the non-essential GSAP/CDNJS runtime dependency and tightening CSP without taking on the larger Tailwind migration risk in the same review slice.

## Scope

### In Scope
- Remove the CDNJS GSAP script from the authenticated app template.
- Remove or replace the single GSAP entrance animation with app-owned behavior.
- Drop `https://cdnjs.cloudflare.com` from CSP and update tests/docs/spec deltas for this narrower policy.

### Out of Scope
- Tailwind CDN removal; defer to a follow-up slice/change due to template churn and visual regression risk.
- Introducing npm, Tailwind CLI, bundlers, or vendored minified GSAP.
- Changing auth, regulatory citation behavior, retrieval flows, or API semantics.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `browser-security-policy`: CSP no longer permits CDNJS/GSAP, while Tailwind CDN remains an explicitly documented interim allowance.

## Approach

Follow the exploration recommendation: delete the external GSAP dependency instead of vendoring it. Update `index.html` and `/static/js/app.js` so page load does not require `window.gsap`, then tighten CSP and regression tests to prove CDNJS is absent. Keep Tailwind unchanged for this chained PR slice.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `app/templates/index.html` | Modified | Remove CDNJS GSAP script tag. |
| `app/static/js/app.js` | Modified | Remove/replace `gsap.from(...)` dependency. |
| `app/core/security_headers.py` | Modified | Remove CDNJS from `script-src`; keep Tailwind allowance. |
| `tests/test_api.py` | Modified | Assert CDNJS/GSAP are absent and CSP remains restrictive. |
| `README.md` | Modified | Document Tailwind as remaining interim CDN debt. |
| `openspec/specs/browser-security-policy/spec.md` | Modified | Update policy expectations through a delta spec. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Minor loss of page polish | Low | Treat GSAP animation as non-functional; preserve page content and interactions. |
| CSP blocks needed asset | Low | Parse CSP in tests and manually load login/home. |
| Tailwind debt misunderstood as solved | Med | Explicitly document Tailwind CDN as deferred follow-up. |

## Rollback Plan

Revert this slice to restore the GSAP script, `gsap.from(...)` call, CDNJS CSP allowance, and previous tests/docs. No data migration or regulatory citation behavior is involved.

## Dependencies

- Existing FastAPI/Jinja2 static asset flow.
- Current pytest integration suite (`py -m pytest`).

## Success Criteria

- [ ] Authenticated app renders without loading or referencing CDNJS/GSAP.
- [ ] CSP `script-src` excludes `https://cdnjs.cloudflare.com` while preserving required same-origin and Tailwind behavior.
- [ ] Tests document remaining Tailwind CDN allowance and pass with `py -m pytest`.
