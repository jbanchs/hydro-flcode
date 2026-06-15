# Tasks: Local Browser Smoke

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 180-320 |
| 400-line budget risk | Medium |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 tests/fixtures → PR 2 docs/checklist |
| Delivery strategy | force-chained |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Local pytest smoke coverage | PR 1 | Base = feature/tracker branch; includes fixtures, RED/GREEN tests, `py -m pytest`. |
| 2 | Manual browser checklist docs | PR 2 | Base = PR 1 branch; updates `README.md` and `docs/deployment.md`; verify docs stay local-only. |

## Phase 1: Test Foundation

- [x] 1.1 RED: Create `tests/test_local_browser_smoke.py` with failing tests for `/healthz`, `/login`, authenticated `/`, security headers, and static assets.
- [x] 1.2 Move shared auth support into `tests/conftest.py`: `client`, `csrf_token_from`, and `login_client` fixtures/helpers using `TestClient(app, follow_redirects=False)`.
- [x] 1.3 Update `tests/test_api.py` to use shared fixtures and remove duplicated login/CSRF helpers without changing existing assertions.

## Phase 2: Smoke Coverage GREEN

- [x] 2.1 Make smoke tests pass for `/healthz` liveness-only JSON and required security headers.
- [x] 2.2 Make `/login` and authenticated `/` tests assert stable DOM hooks/text, local CSS/JS references, and `303 -> /` auth flow.
- [x] 2.3 Add static checks for `/static/css/styles.css` and `/static/js/app.js`: `200`, non-empty body, app-owned content types, and no forbidden external script/style sources.
- [x] 2.4 Run `py -m pytest tests/test_local_browser_smoke.py tests/test_api.py` and refactor fragile markup assertions to stable hooks only.

## Phase 3: Documentation Checklist

- [x] 3.1 Update `README.md` with local smoke command and concise manual browser checklist for `/healthz`, `/login`, authenticated `/`, search, and Ask HYDRO states.
- [x] 3.2 Update `docs/deployment.md` to frame smoke checks as local pre-deploy confidence while Actions billing is blocked, not CI/deploy automation.
- [x] 3.3 Document Playwright/screenshots/browser automation as deferred and ensure docs use placeholders only, with no real secrets or ignored deployment notes.

## Phase 4: Verification and Archive Prep

- [x] 4.1 Run `py -m pytest` and record pass/fail evidence for SDD verify.
- [x] 4.2 Run `openspec validate local-browser-smoke --strict` if OpenSpec CLI is available; otherwise record the missing-tool blocker. Evidence: `openspec --version` failed because the `openspec` term is not recognized, so CLI validation is blocked by missing local tooling.
- [x] 4.3 Prepare archive notes confirming `/healthz` remains liveness-only and no dependencies, CI, deployment, or secret-handling changes were added. Evidence: archive notes are recorded in `apply-progress.md`.
