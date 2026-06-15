# Apply Progress: Local Browser Smoke

## Status

- Change: `local-browser-smoke`
- Mode: Strict TDD for prior test implementation; apply-prep-only finalization for this update.
- Delivery strategy: feature-branch-chain.
- Current boundary: finalize OpenSpec apply evidence only; no product code changes.

## Completed Tasks

### PR 1: Tests and Fixtures

- [x] 1.1 Created `tests/test_local_browser_smoke.py` with RED smoke coverage for `/healthz`, `/login`, authenticated `/`, security headers, and static assets.
- [x] 1.2 Moved shared auth support into `tests/conftest.py`: `client`, `csrf_token_from`, and `login_client` fixtures/helpers using `TestClient(app, follow_redirects=False)`.
- [x] 1.3 Updated `tests/test_api.py` to use shared fixtures and remove duplicated login/CSRF helpers without changing existing assertions.
- [x] 2.1 Made smoke tests pass for `/healthz` liveness-only JSON and required security headers.
- [x] 2.2 Made `/login` and authenticated `/` tests assert stable DOM hooks/text, local CSS/JS references, and `303 -> /` auth flow.
- [x] 2.3 Added static checks for `/static/css/styles.css` and `/static/js/app.js`: `200`, non-empty body, app-owned content types, and no forbidden external script/style sources.
- [x] 2.4 Ran focused pytest evidence for `tests/test_local_browser_smoke.py` and `tests/test_api.py` during the PR 1 slice.

### PR 2: Docs and Checklist

- [x] 3.1 Updated `README.md` with local smoke command and concise manual browser checklist for `/healthz`, `/login`, authenticated `/`, search, and Ask HYDRO states.
- [x] 3.2 Updated `docs/deployment.md` to frame smoke checks as local pre-deploy confidence while Actions billing is blocked, not CI/deploy automation.
- [x] 3.3 Documented Playwright/screenshots/browser automation as deferred and ensured docs use placeholders only, with no real secrets or ignored deployment notes.

### Verification and Archive Prep

- [x] 4.1 Full pytest evidence: `py -m pytest` passed with `51 passed`.
- [x] 4.2 OpenSpec CLI validation blocker recorded: `openspec --version` failed because the `openspec` term is not recognized. `openspec validate local-browser-smoke --strict` cannot run until the CLI is installed or otherwise made available locally.
- [x] 4.3 Archive notes prepared below.

## TDD Cycle Evidence

| Task | RED | GREEN | REFACTOR |
|------|-----|-------|----------|
| 1.1 | Smoke test module was introduced before implementation fixes. | Smoke expectations were later satisfied by existing app behavior and focused fixes. | Assertions kept to stable hooks/text to avoid brittle markup coupling. |
| 1.2 | Shared fixture need was exposed by duplicated auth/CSRF setup. | `tests/conftest.py` fixtures/helpers supported smoke and API tests. | API tests were updated to consume shared helpers. |
| 1.3 | Existing duplicated helpers were replaced after shared fixture extraction. | Existing API assertions remained passing. | Helper duplication was removed from API tests. |
| 2.1 | `/healthz` and header smoke expectations covered liveness-only behavior. | Smoke checks passed without turning `/healthz` into readiness. | Boundary wording remains explicit in docs. |
| 2.2 | Login/authenticated-home smoke expectations covered DOM hooks and auth flow. | `303 -> /` auth flow and local references passed. | Markup assertions were kept stable. |
| 2.3 | Static asset checks covered missing files, empty bodies, content types, and forbidden external sources. | Local CSS/JS asset checks passed. | External browser automation remained out of scope. |
| 2.4 | Focused smoke/API run validated the slice. | Focused pytest evidence was recorded during PR 1. | Fragile assertions were avoided. |

Tasks 3.1-4.3 are documentation/apply-prep tasks and did not require new RED/GREEN product-code cycles.

## Tests Run

- `py -m pytest` → `51 passed`.
- OpenSpec CLI check attempted by orchestrator context: `openspec --version` → failed because `openspec` is not recognized.

## OpenSpec CLI Blocker

OpenSpec archive/strict validation cannot be completed locally because the `openspec` executable is unavailable on PATH. This blocks `openspec validate local-browser-smoke --strict` until the CLI is installed or the project provides a runnable wrapper.

## Archive Prep Notes

- `/healthz` remains liveness-only. It is not documented or tested as readiness, database, auth, dependency, or deployment validation.
- No new runtime dependencies, browser automation dependencies, Playwright/Selenium/Cypress tooling, screenshots, or browser downloads were added.
- No GitHub Actions, CI billing, deployment automation, or remote validation changes were added.
- No secret-handling behavior changed; docs use safe placeholder/test configuration only and do not require inspecting ignored deployment notes or real secrets.
- Manual browser smoke remains local-only pre-deploy confidence while GitHub Actions is billing-blocked.

## Remaining Work

- Install or expose the OpenSpec CLI, then run `openspec validate local-browser-smoke --strict` before archival if strict OpenSpec validation is required by the maintainer.
