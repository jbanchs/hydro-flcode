# Design: Self-Host Frontend Assets Slice 1

## Technical Approach

Remove GSAP as a non-functional runtime dependency rather than vendoring or replacing it. The authenticated app will keep existing HTML, Tailwind CDN styling, and app-owned `/static/js/app.js` behavior, but `app.js` will no longer reference `window.gsap`. CSP will then remove CDNJS from `script-src` while retaining `https://cdn.tailwindcss.com` as explicit deferred debt. This implements the proposal without touching auth, API, database, service, or retrieval flows.

## Architecture Decisions

| Decision | Option | Tradeoff | Rationale |
|---|---|---|---|
| Remove GSAP instead of self-hosting | Delete GSAP script and entrance animation | Loses subtle page-load polish | GSAP is used once for `gsap.from(...)`; self-hosting a library for one cosmetic effect preserves unnecessary attack surface. |
| Preserve UI without JS animation | Do not add replacement JS animation | Less motion, fewer regression paths | Existing Tailwind classes already render acceptable static UI. CSS/JS replacement would add code for non-functional behavior. |
| Tighten CSP narrowly | Remove only `https://cdnjs.cloudflare.com` from `script-src` | Tailwind CDN remains allowed | Keeps slice reviewable and matches chained PR scope; Tailwind migration has higher template/build churn. |
| Test policy and source absence | Update integration/static assertions | Tests do not provide visual validation | Current test suite is pytest/FastAPI only; assertions should catch CDNJS regressions and preserve existing auth/API behavior. |

## Data Flow

No request or domain data flow changes. Only browser asset loading changes:

```text
GET / ──→ Jinja2 index.html ──→ browser loads Tailwind CDN
                         └──→ browser loads /static/js/app.js

Removed: browser ──X──→ cdnjs.cloudflare.com/gsap.min.js
```

Security headers continue to be applied by `SecurityHeadersMiddleware` for all responses before the browser evaluates allowed script sources.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `app/templates/index.html` | Modify | Remove the GSAP CDNJS `<script>` tag; keep Tailwind CDN and `/static/js/app.js`. |
| `app/static/js/app.js` | Modify | Delete the top-level `gsap.from(...)` call so app JS has no dependency on `window.gsap`. |
| `app/core/security_headers.py` | Modify | Remove `https://cdnjs.cloudflare.com` from `CONTENT_SECURITY_POLICY` `script-src`; keep `'self'` and Tailwind CDN. |
| `tests/test_api.py` | Modify | Update CSP allowance expectations; add/assert CDNJS and GSAP are absent from rendered home and static JS. |
| `README.md` | Modify | Remove GSAP from current stack and document Tailwind CDN as the remaining interim frontend asset debt. |
| `openspec/changes/self-host-frontend-assets/specs/browser-security-policy/spec.md` | Create | Delta spec updates CSP requirements to forbid CDNJS/GSAP while documenting Tailwind as deferred. |

## Interfaces / Contracts

No Python API, router, service, database, session, or template context contract changes.

Expected CSP contract after implementation:

```text
script-src 'self' https://cdn.tailwindcss.com
```

The authenticated page contract remains: HTML renders the regulations table, search controls, HYDRO form, logout form, and `/static/js/app.js` script.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit/static | `app/static/js/app.js` contains no `gsap`/CDNJS usage and no unsafe HTML injection | Extend existing frontend static guard patterns in `tests/test_api.py`. |
| Integration | `/login` and authenticated `/` retain security headers; CSP excludes CDNJS and keeps Tailwind | Update `assert_current_frontend_csp_allowances` and page-response assertions. |
| E2E | Basic page render remains usable | No E2E tool exists; rely on FastAPI rendered HTML assertions and recommend manual login/home smoke check. |

Run `py -m pytest` locally.

## Migration / Rollout

No migration required. Roll out as a chained PR slice under 400 changed lines. Rollback is a normal revert restoring the GSAP script tag, `gsap.from(...)`, CDNJS CSP allowance, and previous tests/docs. No data, auth, regulatory citation, or API behavior is involved.

## Open Questions

None.
