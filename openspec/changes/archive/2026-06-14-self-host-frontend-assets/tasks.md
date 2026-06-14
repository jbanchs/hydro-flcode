# Tasks: Self-Host Frontend Assets Slice 1

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 120-220 |
| 400-line budget risk | Low |
| Chained PRs recommended | Yes |
| Suggested split | PR 1: remove GSAP/CDNJS, tighten CSP, tests/docs; later PR: self-host/build Tailwind |
| Delivery strategy | force-chained |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: Low

Boundary: This slice is intentionally under 400 lines but remains PR 1 in the forced chain because the larger frontend asset hardening effort continues with Tailwind self-host/build migration later.

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Remove GSAP/CDNJS and preserve current UI behavior | PR 1 | Base = feature/tracker branch; include tests/docs in this slice. |
| 2 | Self-host or build remaining Tailwind assets | PR 2 | Base = PR 1 branch; out of scope for this tasks file. |

## Phase 1: RED Tests

- [x] 1.1 Update `tests/test_api.py` CSP assertions for `/login` and authenticated `/` to require Tailwind CDN and reject CDNJS in `script-src`.
- [x] 1.2 Add `tests/test_api.py` assertions that `app/templates/index.html` and `app/static/js/app.js` contain no CDNJS GSAP or `window.gsap` dependency.

## Phase 2: Frontend Removal

- [x] 2.1 Remove the CDNJS GSAP `<script>` tag from `app/templates/index.html`; keep Tailwind CDN and `/static/js/app.js`.
- [x] 2.2 Delete the top-level `gsap.from(...)` animation from `app/static/js/app.js` without replacing cosmetic motion.

## Phase 3: CSP Tightening

- [x] 3.1 Remove `https://cdnjs.cloudflare.com` from `CONTENT_SECURITY_POLICY` `script-src` in `app/core/security_headers.py`.
- [x] 3.2 Keep `script-src 'self' https://cdn.tailwindcss.com` and existing object/frame restrictions in `app/core/security_headers.py`.

## Phase 4: Documentation and Verification

- [x] 4.1 Update `README.md` to remove GSAP/CDNJS from current dependencies and call Tailwind CDN remaining interim debt.
- [x] 4.2 Run `py -m pytest` and confirm security header, frontend asset, auth, and API regression tests pass.
