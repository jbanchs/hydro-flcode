# Apply Progress: Remove Tailwind CDN

## Current Slice

- PR slice: PR 3 JS/docs/smoke
- Delivery strategy: force-chained
- Chain strategy: feature-branch-chain
- Boundary: Convert remaining dynamic JavaScript Tailwind-style utility strings to local semantic CSS classes, update README hardening guidance, and record deterministic smoke/verification evidence without committing.

## Completed Tasks

- [x] 1.1 RED: Updated `tests/test_api.py` CSP assertions for `/login` and authenticated `/` to require `script-src 'self'`, `style-src 'self'`, and absence of Tailwind CDN, CDNJS, wildcard, HTTPS broad allow, and `unsafe-inline`.
- [x] 1.2 RED/PENDING: Added a focused rendered/static asset scan in `tests/test_api.py` that documents the PR 2 end state while keeping the suite green until template/CSS conversion removes Tailwind CDN references.
- [x] 1.3 GREEN: Updated `app/core/security_headers.py` to same-origin `script-src`/`style-src` while preserving `object-src 'none'`, `base-uri 'self'`, `frame-ancestors 'none'`, `form-action 'self'`, and existing image/font/connect directives.
- [x] 2.1 GREEN: Expanded `app/static/css/styles.css` with base, login, app shell, cards, forms, table, badge, answer, and responsive classes.
- [x] 2.2 GREEN: Modified `app/templates/login.html` to remove Tailwind CDN and use local `page-login`, `login-card`, `form-field`, and `primary-button` classes.
- [x] 2.3 GREEN: Modified `app/templates/index.html` to remove Tailwind CDN and map layout/sidebar/table/consult panel markup to semantic classes.
- [x] 2.4 REFACTOR: Kept template class names aligned with the design contract and avoided broad Tailwind utility alias recreation.
- [x] 3.1 GREEN: Updated `app/static/js/app.js` table helpers to use `table-cell`, `table-cell--*`, `table-row`, and `badge` classes instead of Tailwind utility strings.
- [x] 3.2 GREEN: Updated `app/static/js/app.js` Ask HYDRO answer and missing-info states to use `answer-line`, `answer-line--lead`, `answer-line--muted`, and `answer-warning` classes.
- [x] 3.3 REFACTOR: Preserved `textContent`/`createElement` safety plus `/api/regulations` and `/api/ask` behavior; existing raw HTML injection and API tests remain green.
- [x] 4.1 Verification: `py -m pytest` passes with security header, asset reference, raw HTML injection, API, CI workflow, and frequency tests green.
- [x] 4.2 Smoke evidence: Browser smoke could not be executed in this environment. Deterministic local evidence covers rendered local assets, absence of Tailwind/CDNJS/GSAP references, semantic JS class usage, README manual smoke guidance, and full pytest results.
- [x] 4.3 Documentation: Updated `README.md` to state Tailwind CDN removal, local static CSS strategy, same-origin CSP, and required `/login` plus authenticated `/` visual checks.
- [x] 4.4 OpenSpec alignment: Updated `tasks.md` checkboxes. `openspec validate remove-tailwind-cdn --strict` was attempted but blocked because the `openspec` CLI is not installed/available on PATH.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/test_api.py` | Integration | ✅ 19/19 baseline passing | ✅ CSP assertions written first; failed against Tailwind/unsafe-inline policy | ✅ Passed after CSP change | ✅ Covered `/login` and authenticated `/` | ➖ None needed |
| 1.2 | `tests/test_api.py` | Static scan | ✅ 19/19 baseline passing | ✅ End-state asset assertions written first; failed on login CSS/Tailwind references | ✅ Converted to explicit pending-state documentation to keep PR 1 green | ✅ Covers login template, index template, and `app.js` | ➖ Full enforcement deferred to PR 2 |
| 1.3 | `tests/test_api.py` | Integration | ✅ 19/19 baseline passing | ✅ Existing new CSP tests failed before production change | ✅ `py -m pytest tests/test_api.py` passed 19/19 | ✅ Same CSP helper exercised by unauthenticated and authenticated pages | ➖ None needed |
| 2.1 | `tests/test_api.py` | Static scan + integration | ✅ 19/19 baseline passing | ✅ Activated local-asset end-state test first; failed because login lacked local CSS and templates referenced Tailwind CDN | ✅ `py -m pytest tests/test_api.py` passed 19/19 after local CSS/template conversion | ✅ Covers login template, index template, and JS source dependency absence | ✅ Consolidated reusable semantic CSS instead of Tailwind aliases |
| 2.2 | `tests/test_api.py` | Static scan + integration | ✅ 19/19 baseline passing | ✅ Same activated asset test failed before login template conversion | ✅ Login renders with local stylesheet and no Tailwind CDN under passing security tests | ✅ Login and authenticated templates both assert local stylesheet presence | ✅ Replaced utility classes with semantic login/form/button contract |
| 2.3 | `tests/test_api.py` | Static scan + integration | ✅ 19/19 baseline passing | ✅ Same activated asset test failed before index template Tailwind removal | ✅ Authenticated home renders with local stylesheet/script and no Tailwind CDN under passing security tests | ✅ Authenticated home plus login coverage verifies both primary rendered pages | ✅ Mapped shell/sidebar/table/consult panel to semantic classes |
| 2.4 | `tests/test_api.py` | Static scan | ✅ 19/19 baseline passing | ✅ Asset absence test constrained refactor to no external CDN dependencies | ✅ `py -m pytest` passed 32/32 after refactor | ✅ CSS/templates preserve named design contracts without broad Tailwind utility aliases | ✅ Class names aligned to design contract |
| 3.1 | `tests/test_api.py` | Static scan | ✅ 19/19 baseline passing | ✅ Added semantic dynamic UI class test first; failed on `px-5`, `py-4`, `hover:bg-slate-50`, `rounded-full`, and related utility strings | ✅ `py -m pytest tests/test_api.py` passed 21/21 after JS/CSS conversion | ✅ Covered default cells, specialized modifier cells, rows, and badges | ✅ Kept helper defaults semantic and CSS-backed |
| 3.2 | `tests/test_api.py` | Static scan | ✅ 19/19 baseline passing | ✅ Same semantic dynamic UI test failed on answer utility strings such as `font-semibold`, `mt-3`, and `text-amber-*` | ✅ `py -m pytest tests/test_api.py` passed 21/21 after answer class conversion | ✅ Covered lead answer, standard lines, muted interpretation, and missing-info warning | ✅ Added focused answer CSS modifiers instead of recreating Tailwind aliases |
| 3.3 | `tests/test_api.py` | Static scan + integration | ✅ 19/19 baseline passing | ✅ Existing raw HTML injection and API tests protected current behavior during JS refactor | ✅ `py -m pytest` passed 34/34 | ✅ `/api/regulations`, `/api/ask`, raw HTML injection, and asset dependency tests all passed together | ✅ Preserved `textContent`/`createElement` DOM construction |
| 4.1 | `tests/test_api.py`, full suite | Integration/static scan | ✅ 19/19 baseline passing | ✅ Verification expectations existed before final implementation | ✅ `py -m pytest` passed 34/34 | ✅ Full suite covers API, security/assets, CI workflow, and frequency engine | ➖ None needed |
| 4.2 | `tests/test_api.py` | Deterministic smoke substitute | ✅ 19/19 baseline passing | ✅ Tests enforce local rendered assets, no external CDN dependencies, and semantic dynamic classes before reporting smoke evidence | ✅ `py -m pytest` passed 34/34 | ✅ Covers login template, authenticated template, search JS table states, Ask HYDRO answer states, and docs guidance | ➖ Browser E2E unavailable; limitation documented |
| 4.3 | `tests/test_api.py` | Documentation scan | ✅ 20/20 API test file passing before README edit | ✅ README documentation test written first; failed because README still described Tailwind CDN interim debt | ✅ `py -m pytest tests/test_api.py` passed 21/21 after README update | ✅ Asserts removal statement, local CSS path, manual `/login`, authenticated `/`, search refresh, and Ask HYDRO checks | ✅ Replaced stale CDN language with current hardening guidance |
| 4.4 | OpenSpec CLI + artifact check | Tooling/artifact | ✅ Tasks artifact read before update | ✅ Validation task remained incomplete until command was attempted and artifact alignment completed | ⚠️ `openspec validate remove-tailwind-cdn --strict` blocked: CLI unavailable on PATH | ✅ `tasks.md` and `apply-progress.md` now show cumulative completion and blocked validation evidence | ➖ No code refactor |

## Test Summary

- Total tests written/updated: 5 focused security/asset/docs tests across the change; PR 3 added semantic dynamic JS class coverage and README hardening guidance coverage.
- Total tests passing: 34/34 full suite.
- Layers used: Integration, static scan, documentation scan, deterministic smoke substitute.
- Approval tests: Existing raw HTML injection and API tests served as behavior-preservation checks during JS refactor.
- Pure functions created: 0.

## Manual / Smoke Evidence

- Browser E2E/manual visual smoke was not executed in this environment.
- Deterministic local verification performed instead:
  - Rendered templates/static sources contain `/static/css/styles.css` and no Tailwind CDN, CDNJS, GSAP, or `window.gsap` dependency.
  - JS dynamic UI source contains semantic `table-cell`, `table-row`, `badge`, `answer-line`, and `answer-warning` classes and no targeted Tailwind utility strings.
  - Raw HTML injection scan remains green, preserving safe `textContent`/`createElement` DOM construction.
  - README documents required manual checks for `/login`, authenticated `/`, search refresh, and Ask HYDRO answer/missing-information states.

## Risks

- Visual parity still needs real browser review before merge because no Playwright/Cypress/Selenium-style E2E tooling exists.
- `openspec` CLI validation could not run locally because the command is unavailable on PATH.

## Verification

- `py -m pytest tests/test_api.py` — 19 passed baseline before PR 3 edits.
- `py -m pytest tests/test_api.py` — failed as expected after RED semantic JS test.
- `py -m pytest tests/test_api.py` — 21 passed after JS/CSS/README implementation.
- `py -m pytest` — 34 passed.
- `openspec validate remove-tailwind-cdn --strict` — blocked: `openspec` command not recognized.
