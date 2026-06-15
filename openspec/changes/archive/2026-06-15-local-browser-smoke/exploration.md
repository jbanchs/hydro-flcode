## Exploration: local-browser-smoke

### Current State
HYDRO is a FastAPI/Jinja2 app with server-rendered `/login` and authenticated `/`, app-owned static CSS/JS under `/static`, strict same-origin CSP/security headers, session/CSRF auth, API endpoints for regulation search and Ask HYDRO, and a public `/healthz` liveness endpoint. Current pytest coverage uses FastAPI `TestClient` for auth, API, headers, CSP, local asset references, XSS-pattern guards, deployment docs, and CI workflow shape. OpenSpec records that browser E2E tooling is unavailable, README already calls out manual visual smoke checks after CSS changes, and GitHub Actions is currently blocked by account billing rather than code failure.

### Affected Areas
- `requirements.txt` — would need any added smoke dependency such as Playwright; current dependencies are Python-only pytest/httpx/FastAPI tooling.
- `pytest.ini` / `tests/` — natural home for local smoke tests that can run with `py -m pytest` without GitHub Actions.
- `app/main.py` — mounts `/static`, includes routers, and is the app entry point a local smoke path would exercise.
- `app/routers/web.py` — login, logout, CSRF, authenticated home rendering, and local session flow are central to UI readiness.
- `app/routers/health.py` — `/healthz` is liveness-only and should remain distinct from browser/authenticated readiness.
- `app/core/security_headers.py` — CSP and browser security headers must remain compatible with any local browser smoke path.
- `app/templates/login.html` and `app/templates/index.html` — rendered pages that need smoke validation for local CSS/JS references and basic UI structure.
- `app/static/css/styles.css` and `app/static/js/app.js` — browser-facing assets; JavaScript interactions are only truly exercised by a browser runner.
- `README.md` and `docs/deployment.md` — likely places to document the local smoke command/checklist while keeping deploy automation out of scope.
- `.github/workflows/ci.yml` — should not be treated as the immediate validation path while billing blocks Actions; optional later integration only.

### Approaches
1. **Playwright local browser smoke** — add a small Playwright-based smoke test that boots the FastAPI app locally, logs in with test credentials, checks `/healthz`, `/login`, authenticated `/`, local CSS/JS loading, search refresh, and Ask HYDRO output/missing-info states.
   - Pros: validates real browser behavior, CSP/static asset compatibility, DOM updates from `app.js`, and the UI/deploy readiness gap that TestClient cannot cover.
   - Cons: adds dependency weight, browser install step, slower local runs, and higher maintenance than the current pytest-only stack.
   - Effort: Medium

2. **FastAPI TestClient HTML/static smoke only** — extend pytest with server-side assertions for rendered HTML, static asset responses, headers, login flow, and known text/element IDs.
   - Pros: smallest dependency footprint, fast, works fully offline after Python dependencies are installed, fits current test patterns, no secrets or deploy needed.
   - Cons: cannot execute JavaScript, cannot prove CSS actually renders, and cannot catch browser-only CSP/static loading failures.
   - Effort: Low

3. **Manual checklist script/doc** — document and/or provide a non-deploy local checklist around `py -m pytest`, `uvicorn app.main:app`, `/healthz`, `/login`, authenticated `/`, search refresh, and Ask HYDRO states.
   - Pros: near-zero tooling cost, works while GitHub Actions is blocked, keeps deploy automation out of scope, and matches README's current manual visual smoke guidance.
   - Cons: human-dependent, easy to skip, weak regression protection, and no machine-readable proof beyond screenshots/notes.
   - Effort: Low

4. **Screenshots/visual smoke** — use browser automation to capture baseline screenshots for `/login`, authenticated `/`, search results, and Ask HYDRO states, optionally comparing snapshots.
   - Pros: directly targets visual readiness and CSS regressions.
   - Cons: highest flake/maintenance cost, screenshot diffs are noisy across OS/font/browser rendering, and it is more process than HYDRO needs right now.
   - Effort: High

5. **Cost/maintenance-minimized hybrid** — add a pytest-only smoke layer now plus a documented manual browser checklist; defer Playwright/screenshots until repeated UI regressions or pre-production readiness justifies the dependency.
   - Pros: smallest safe slice, improves local validation immediately without secrets, real deploy, GitHub Actions, or heavy browsers, and stays under a small review budget.
   - Cons: still leaves JavaScript execution and visual rendering as manual checks.
   - Effort: Low

### Recommendation
Recommend the cost/maintenance-minimized hybrid for now: create a local pytest smoke test module using `TestClient` to verify `/healthz`, `/login`, authenticated `/`, security headers, local CSS/JS asset responses, and key DOM hooks/text required for search and Ask HYDRO, plus update documentation with a short manual browser checklist for the interactions TestClient cannot execute. Do not add Playwright or screenshot comparison in the first slice. That keeps the change small, local, non-secret, non-deploy, and useful while GitHub Actions is blocked by billing. Playwright should remain a follow-up option once the project is closer to production or UI regressions justify browser dependency cost.

### Risks
- TestClient smoke can produce false confidence because it does not execute `app/static/js/app.js` or render CSS.
- Manual visual checks remain dependent on discipline unless later replaced by browser automation.
- Adding Playwright too early may create setup friction and review noise that exceeds the value of this blocked-CI workaround.
- Any docs must preserve the existing boundary that `/healthz` is liveness-only, not authenticated readiness or database validation.
- The ignored local deployment secret note must remain unread, unnamed, and untouched.

### Ready for Proposal
Yes — propose the smallest safe slice: local pytest HTML/static smoke coverage plus a documented manual browser checklist, explicitly deferring Playwright and screenshots. Tell the user this is not a GitHub Actions fix and not deploy automation; it is a local confidence path while Actions is blocked by billing.
