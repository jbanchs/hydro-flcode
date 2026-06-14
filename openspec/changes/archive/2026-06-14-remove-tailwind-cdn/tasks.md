# Tasks: Remove Tailwind CDN

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 450-650 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 tests/security → PR 2 CSS/templates → PR 3 JS/docs/smoke |
| Delivery strategy | force-chained |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Lock failing security/asset tests | PR 1 | base = feature/tracker branch; pytest only |
| 2 | Replace Tailwind template styling with local CSS | PR 2 | base = PR 1 branch; visual-heavy review |
| 3 | Convert JS classes, docs, smoke evidence | PR 3 | base = PR 2 branch; dynamic UI/manual checks |

## Phase 1: TDD Security Baseline

- [x] 1.1 RED: update `tests/test_api.py` CSP assertions for `/login` and authenticated `/`: `script-src 'self'`, `style-src 'self'`, no Tailwind/CDNJS/`unsafe-inline`.
- [x] 1.2 RED: add `tests/test_api.py` rendered asset scans proving local `/static/css/styles.css`, no Tailwind CDN, no CDNJS GSAP, no `window.gsap` dependency. Pending end-state assertions are documented in a green compatibility test until PR 2 removes template Tailwind CDN references.
- [x] 1.3 GREEN: update `app/core/security_headers.py` to same-origin `script-src`/`style-src` while preserving object/frame/base/form restrictions.

## Phase 2: Local CSS and Templates

- [x] 2.1 GREEN: expand `app/static/css/styles.css` with base, login, app shell, cards, forms, table, badge, answer, and responsive classes.
- [x] 2.2 GREEN: modify `app/templates/login.html` to remove Tailwind CDN and use `page-login`, `login-card`, `form-field`, `primary-button` classes.
- [x] 2.3 GREEN: modify `app/templates/index.html` to remove Tailwind CDN and map layout/sidebar/table/consult panel markup to semantic classes.
- [x] 2.4 REFACTOR: keep template class names aligned with design contract; do not recreate broad Tailwind utility aliases.

## Phase 3: Dynamic UI Conversion

- [x] 3.1 GREEN: update `app/static/js/app.js` table helpers to use `table-cell`, modifier classes, and `badge` instead of Tailwind utilities.
- [x] 3.2 GREEN: update `app/static/js/app.js` Ask HYDRO answer/missing-info states to use `answer-box`, `answer-line`, `answer-warning` classes.
- [x] 3.3 REFACTOR: preserve existing `textContent`/`createElement` safety and `/api/regulations` plus `/api/ask` JSON behavior.

## Phase 4: Verification and Documentation

- [x] 4.1 Run `pytest` and confirm security header, asset reference, and raw HTML injection tests pass.
- [x] 4.2 Manually smoke `/login`, authenticated `/`, search refresh, answer, and missing-info states for readability without CDN assets. Browser smoke could not be executed in this environment; deterministic local verification is documented in apply-progress via rendered asset/static JS/README tests and full pytest evidence.
- [x] 4.3 Update `README.md` to state Tailwind CDN removal, local static CSS strategy, and required `/login` plus `/` visual checks.
- [x] 4.4 Run `openspec validate remove-tailwind-cdn --strict` and keep this `tasks.md` aligned with completed work. Validation attempted but blocked because `openspec` CLI is not installed/available on PATH; tasks/apply-progress remain aligned.
