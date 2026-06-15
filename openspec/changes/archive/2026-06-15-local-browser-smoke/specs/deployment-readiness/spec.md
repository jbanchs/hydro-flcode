# Delta for Browser Security Policy and Deployment Readiness

## Capability Mapping

- `browser-security-policy`: Local HTML/static asset smoke coverage for rendered pages, DOM hooks/text, and security headers.
- `deployment-readiness`: Local smoke usefulness while GitHub Actions is billing-blocked, with `/healthz` preserved as liveness-only.

## ADDED Requirements

### Requirement: Local HTML and Static Asset Smoke Coverage

The system MUST provide local pytest smoke coverage for server-rendered HTML, DOM hooks/text, security headers, and app-owned static CSS/JavaScript references using the existing pytest/FastAPI `TestClient` stack only, without new browser automation dependencies, remote CI, deployment, or secrets.

#### Scenario: Local smoke validates rendered pages

- GIVEN a developer has installed project test dependencies
- WHEN they run `py -m pytest` locally
- THEN smoke coverage MUST verify `/healthz`, `/login`, and authenticated `/` return expected responses and security headers
- AND rendered pages MUST expose required local CSS, JavaScript, stable DOM hooks, and key text.

#### Scenario: Static reference regression is detected

- GIVEN a rendered page references a missing local static asset or forbidden external script/style source
- WHEN local pytest smoke coverage runs
- THEN the test suite MUST fail before any deployment or browser automation is required.

### Requirement: Manual Browser Checklist

README/deployment documentation MUST provide a concise manual local browser checklist for visual readability and JavaScript behavior that pytest cannot execute. The checklist MUST remain local-only and MUST NOT require Playwright, Selenium, Cypress, screenshots, remote CI, deployment, or secrets.

#### Scenario: Maintainer performs local browser smoke

- GIVEN the app is running locally with safe development/test configuration
- WHEN a maintainer follows the checklist in a browser
- THEN they MUST verify `/healthz`, `/login`, authenticated `/`, local styling, search interaction, and Ask HYDRO states
- AND they MUST record issues without adding real secrets to tracked files.

#### Scenario: Playwright remains deferred

- GIVEN a change proposes Playwright, screenshots, browser downloads, or CI browser jobs for this slice
- WHEN it is reviewed against local-browser-smoke scope
- THEN the change MUST be rejected or moved to a follow-up proposal.

### Requirement: Local Validation Boundary

The smoke path MUST provide local confidence while GitHub Actions is billing-blocked and MUST preserve existing deployment-readiness boundaries: `/healthz` remains liveness-only, no CI/deployment fix is implied, no remote service is contacted, and no secret-bearing artifact is read, created, copied, or named.

#### Scenario: CI or deployment is unavailable

- GIVEN GitHub Actions is blocked by billing or deployment infrastructure is unavailable
- WHEN a developer needs pre-deployment confidence
- THEN they MUST be able to run the local pytest smoke checks and manual checklist without remote dependencies.

#### Scenario: Secret handling boundary is preserved

- GIVEN local smoke documentation or tests are reviewed
- WHEN they describe configuration needs
- THEN they MUST use placeholder or safe test configuration only
- AND they MUST NOT disclose, require, or inspect real deployment secrets.
