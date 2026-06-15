# Design: Local Browser Smoke

## Technical Approach

Add a lightweight local smoke layer aligned with the proposal: stay inside the existing pytest/FastAPI `TestClient` stack, assert rendered HTML/static/security-header behavior locally, and document browser-only checks separately. This preserves `/healthz` as liveness-only, avoids new runtime/test dependencies, and treats the local smoke path as a workaround while GitHub Actions is billing-blocked—not as a CI/deploy fix.

## Architecture Decisions

| Option | Tradeoff | Decision |
|--------|----------|----------|
| Pytest `TestClient` smoke tests | Fast, dependency-free, matches `tests/test_api.py`; cannot execute JS or render CSS. | Use for local automated smoke coverage. |
| Playwright browser smoke | Real browser confidence; adds browser install, slower runs, and review noise. | Defer; document why and what would trigger adoption. |
| Reuse login helper from `tests/test_api.py` | Existing helper works but cross-test imports couple modules. | Move shared auth helpers into `tests/conftest.py` fixtures. |
| Manual checklist in docs | Human-dependent but covers visual/JS gaps. | Add concise README/deployment guidance for visual readability, search, and Ask HYDRO states. |

## Data Flow

```text
pytest smoke test ──→ TestClient(app) ──→ FastAPI middleware/routers
       │                    │                    │
       │                    ├── GET /healthz     ├── static JSON + headers
       │                    ├── GET/POST /login  ├── session + CSRF auth
       │                    ├── GET /            ├── Jinja2 app shell
       │                    └── GET /static/...  └── app-owned CSS/JS
       └── docs checklist ──→ local browser manual visual/JS validation
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `tests/conftest.py` | Modify | Add shared `client`, `csrf_token_from`, and `login_client` fixtures/helpers while preserving isolated test DB setup. |
| `tests/test_local_browser_smoke.py` | Create | Add smoke assertions for `/healthz`, unauthenticated redirect, login page, authenticated home DOM hooks/text, local CSS/JS responses, and security headers. |
| `tests/test_api.py` | Modify | Remove or stop relying on local auth helper duplication if moved to `conftest.py`; keep behavior tests intact. |
| `README.md` | Modify | Add local smoke command and reference the manual checklist; state this is not deploy automation or a CI billing fix. |
| `docs/deployment.md` | Modify | Add/point to the manual checklist only as local pre-deploy confidence; preserve `/healthz` as liveness-only and avoid secret-bearing deployment notes. |

## Interfaces / Contracts

No application API changes. Test contracts:

- `py -m pytest` MUST include the local smoke checks without browser tooling or new dependencies.
- Smoke tests MUST use `TestClient(app, follow_redirects=False)`.
- Auth setup MUST fetch `/login`, parse `csrf_token`, post `admin` with `TEST_ADMIN_PASSWORD`, then assert `303 -> /`.
- Static checks MUST request `/static/css/styles.css` and `/static/js/app.js`, assert `200`, non-empty body, and expected content types.
- `/healthz` MUST remain unauthenticated static JSON and not be treated as database/auth readiness.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Shared CSRF parsing helper | Simple HTML fixture/assertion if helper becomes non-trivial; otherwise covered through smoke flow. |
| Integration | FastAPI rendered pages, auth, headers, static assets, `/healthz` | `TestClient` smoke module using the initialized test SQLite DB. |
| E2E | Real JS execution, visual rendering, browser network panel | Manual checklist only; Playwright explicitly deferred. |

## Migration / Rollout

No migration required. Rollback is reverting the new smoke test module, helper extraction if needed, and README/deployment docs. Because no runtime code changes are planned, rollback does not affect auth, API, database, static assets, CI, or deployment behavior.

## Work Unit / Chained PR Plan

Keep implementation under the 400-line review budget as one small chain-ready slice: test fixtures + smoke tests + docs. If it grows, split docs/checklist into a second chained PR after the pytest smoke slice.

## Open Questions

- [ ] None.
