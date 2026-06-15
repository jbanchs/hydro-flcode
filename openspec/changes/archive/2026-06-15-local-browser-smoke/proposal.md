# Proposal: Local Browser Smoke

## Intent

Add a local confidence path for HYDRO's server-rendered UI while GitHub Actions is blocked by account billing. The change should catch broken HTML/static asset wiring and document manual browser checks without adding browser automation cost.

## Scope

### In Scope
- Add pytest smoke coverage for `/healthz`, `/login`, authenticated `/`, rendered DOM hooks/text, security headers, and local `/static` CSS/JS responses.
- Document a short manual browser checklist for visual readability and JavaScript interactions.
- Preserve `/healthz` as liveness-only and keep validation local/non-deploy.

### Out of Scope
- Playwright, Selenium, Cypress, screenshot comparison, or browser installs.
- GitHub Actions billing fixes, CI/CD deployment, or deploy automation.
- Secret handling changes or access to ignored local deployment notes.

## Capabilities

### New Capabilities
None

### Modified Capabilities
- `browser-security-policy`: Extend test/documentation expectations for local HTML, static asset, DOM-hook, and manual visual smoke coverage.
- `deployment-readiness`: Clarify local smoke usefulness while Actions is billing-blocked and preserve `/healthz` liveness-only boundaries.

## Approach

Use the cost/maintenance-minimized hybrid from exploration: pytest `TestClient` assertions for server-rendered HTML and static assets, plus README/deployment docs checklist for browser-only behavior. Do not introduce new runtime/test dependencies.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `tests/` | New | Local smoke tests for rendered pages, static assets, and DOM hooks. |
| `README.md` | Modified | Manual browser smoke checklist and local command guidance. |
| `docs/deployment.md` | Modified | Billing-blocked Actions context and `/healthz` boundary. |
| `pytest.ini` | Modified | Only if needed to include smoke markers/config. |
| `.github/workflows/ci.yml` | Unchanged | CI remains out of scope while billing blocks Actions. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| False confidence: pytest cannot execute JS or render CSS | Med | Document manual browser checklist and defer automation explicitly. |
| Smoke tests over-specify fragile markup | Med | Assert stable IDs/text/hooks tied to user workflows only. |
| `/healthz` gets treated as readiness | Low | Keep docs/tests explicit that it is liveness-only. |

## Rollback Plan

Revert the smoke test module and documentation checklist. No data, dependency, CI, or runtime behavior changes should need rollback.

## Dependencies

- Existing pytest/FastAPI `TestClient` stack only.
- GitHub Actions remains blocked by billing; local smoke is a workaround, not a CI fix.

## Success Criteria

- [ ] `py -m pytest` includes local HTML/static smoke coverage without new browser dependencies.
- [ ] Docs provide a concise manual browser checklist for `/healthz`, `/login`, authenticated `/`, search, and Ask HYDRO states.
- [ ] Playwright/screenshots/browser automation remain documented as deferred.
