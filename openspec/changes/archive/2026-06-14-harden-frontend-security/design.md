# Design: Harden Frontend Security

## Technical Approach

Add response-level security headers through a small Starlette/FastAPI middleware registered in `app/main.py`, backed by constants in `app/core/config.py`. The first policy is enforceable, pragmatic, and compatible with current Jinja2 templates: Tailwind CDN on login/home, CDNJS GSAP on home, local `/static/css/styles.css`, and `/static/js/app.js`. No service, router, or database behavior changes are needed.

## Architecture Decisions

| Option | Tradeoff | Decision |
|--------|----------|----------|
| Inline middleware in `app/main.py` | Fast, but grows startup file and makes header policy harder to unit-test. | Create `app/core/security_headers.py` with middleware and policy constants; register it in `app/main.py`. |
| Enforced CSP vs report-only | Enforced protects immediately; report-only is safer for unknown browser behavior. | Use enforced `Content-Security-Policy`; keep a config toggle for report-only only if tests/manual validation expose breakage. |
| Allow CDNs narrowly vs broad `https:` | Narrow allowlist can break CDN changes; broad `https:` weakens protection. | Allow only `https://cdn.tailwindcss.com` and `https://cdnjs.cloudflare.com` for scripts; document as interim. |
| CSP nonce/hash plumbing | Stronger for inline code but adds template plumbing. | Do not add nonce/hash now because templates load external scripts and no inline scripts are present. |

## Data Flow

```text
Browser ──→ FastAPI app ──→ routers/templates/static
Browser ←── SecurityHeadersMiddleware adds headers to every response
```

The middleware wraps the existing app stack after `SessionMiddleware` registration. Rendered pages, redirects, API JSON, and static responses receive the same browser security headers unless implementation deliberately limits scope; tests focus on `/login` and authenticated `/` per proposal.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `app/core/security_headers.py` | Create | Define CSP/header constants and middleware that sets headers with `setdefault` to avoid overriding explicit future responses. |
| `app/main.py` | Modify | Import and register `SecurityHeadersMiddleware` near existing `SessionMiddleware`. |
| `app/core/config.py` | Modify | Add optional CSP report-only/enforce setting only if needed; default enforce. |
| `tests/test_api.py` | Modify | Add integration assertions for `/login` and authenticated `/`; preserve existing XSS static guard tests. |
| `README.md` | Modify | Document current security headers, CDN exception rationale, rollback, and self-hosting follow-up. |

## Interfaces / Contracts

Expected response headers:

```text
Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.tailwindcss.com https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
```

`style-src 'unsafe-inline'` is intentionally temporary because Tailwind CDN injects runtime styles and current templates use utility classes. `connect-src 'self'` supports existing `fetch('/api/...')` calls in `app/static/js/app.js`.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Header map / CSP string contains exact directives. | Optional focused pytest if middleware helper is factored into pure function. |
| Integration | `/login` and authenticated `/` include CSP and companion headers. | Extend `tests/test_api.py` with `TestClient`; login helper already exists. |
| E2E | Browser runtime compatibility for Tailwind/GSAP. | Not available in repo; document manual validation and risk. |

Run `py -m pytest` locally. CI remains configured for `python -m pytest`.

## Migration / Rollout

No data migration required. Roll out as one reviewable work unit: middleware/config + tests + README. Rollback is reverting that unit, which immediately restores previous response headers. Follow-up: replace Tailwind CDN with a local build and vendor/self-host GSAP so CSP can remove third-party script origins and `style-src 'unsafe-inline'`.

## Open Questions

- [ ] None blocking. Manual browser validation should confirm Tailwind CDN style injection under the proposed `style-src` before merging.
