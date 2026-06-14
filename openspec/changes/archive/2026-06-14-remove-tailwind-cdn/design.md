# Design: Remove Tailwind CDN

## Technical Approach

Replace HYDRO's small Tailwind CDN surface with app-owned CSS in `app/static/css/styles.css`, then update Jinja templates and JavaScript-created elements to use local semantic classes. This is a static asset/security hardening slice only: no router, service, database, or regulatory-answer behavior changes. CSP can then move from Tailwind/inline allowances to same-origin frontend assets.

## Architecture Decisions

| Option | Tradeoff | Decision |
|--------|----------|----------|
| Hand-written semantic CSS | Slight manual mapping work, but fits current no-build FastAPI/Jinja app | Use local CSS classes in `styles.css` |
| Tailwind CLI/PostCSS/Node | Better long-term utility workflow, but adds package/build/CI surface outside scope | Reject for this slice |
| Preserve utility strings in JS | Fast but requires recreating many Tailwind names as global CSS utilities | Replace JS class strings with semantic row/cell/badge/answer classes |
| Tighten CSP first | Proves security target but breaks pages before CSS/template conversion | Update tests first, then CSS/templates/JS, then CSP |

## Data Flow

FastAPI static mount serves local assets; templates reference only same-origin CSS/JS.

    Browser ──GET /login or /──→ FastAPI/Jinja template
       │                            │
       ├──GET /static/css/styles.css┘
       └──GET /static/js/app.js ──→ DOM rows/answer content using local classes

No application data flow changes: `/api/regulations` and `/api/ask` keep returning the same JSON, and `app.js` still builds DOM with `textContent`/`createElement`.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `app/templates/login.html` | Modify | Remove Tailwind CDN; add `/static/css/styles.css`; replace utility-heavy classes with semantic login/card/form/button classes. |
| `app/templates/index.html` | Modify | Remove Tailwind CDN; map shell/sidebar/header/table/consult-panel markup to local semantic classes. |
| `app/static/css/styles.css` | Modify | Expand from `.input` to full local stylesheet: reset/base, layout, cards, forms, table, badges, answer states, responsive rules. |
| `app/static/js/app.js` | Modify | Replace generated Tailwind strings (`px-5 py-4`, `hover:bg-slate-50`, text color utilities) with CSS-backed semantic classes. |
| `app/core/security_headers.py` | Modify | Set `script-src 'self'` and `style-src 'self'`; keep current image/font/connect/object/base/frame/form directives. |
| `tests/test_api.py` | Modify | Assert no Tailwind CDN references in templates/JS and assert tightened CSP disallows third-party scripts and `unsafe-inline`. |
| `README.md` | Modify | Document local static CSS strategy and required manual visual checks for `/login` and authenticated `/`. |

## Interfaces / Contracts

CSS class names become the local template/JS contract. Prefer component-like names over Tailwind aliases:

```text
page-login, login-card, brand-mark, form-field, primary-button
app-shell, sidebar, nav-link, content-card, search-panel
reg-table, table-row, table-cell, table-cell--muted, badge
consult-panel, answer-box, answer-line, answer-warning
```

`app.js` helper defaults should shift from Tailwind utility strings to semantic defaults, e.g. `cell(text, "table-cell")`; specialized cells use modifiers such as `table-cell--mono`, `table-cell--muted`, and `table-cell--accent`.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | CSP parsing/security assertions | Update existing pytest helper expectations to exact self-only `script-src`/`style-src`. |
| Integration | `/login` and authenticated `/` rendered HTML | FastAPI `TestClient` asserts local stylesheet/script are present and `cdn.tailwindcss.com`, `unsafe-inline`, wildcard, and third-party script sources are absent. |
| Static scan | JS-generated class coverage and XSS safety | Extend file-content assertions around `app.js`/templates; keep existing raw HTML injection scan. |
| Manual | Visual preservation | Capture/check `/login`, `/`, search results refresh, and Ask HYDRO answer/missing-info states. No browser E2E tooling exists. |

## Migration / Rollout

No data migration required. Roll out as reviewable chained slices if needed: tests/security expectation, local CSS/template conversion, JS-generated class conversion, docs/manual checks. Rollback is a clean revert restoring Tailwind script tags, old CSP allowances, tests, and README notes.

## Open Questions

None.
