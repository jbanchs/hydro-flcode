## Exploration: production-mode-signal

### Current State
HYDRO currently has no explicit production-mode signal. Runtime config is read directly from process environment in `app/core/config.py`: `HYDRO_SESSION_SECRET` is required unless `HYDRO_ALLOW_DEV_SECRET=1`, `HYDRO_SESSION_COOKIE_SECURE` is true only when set to `"1"`, and `HYDRO_DATABASE_PATH` defaults to repo-local `hydro.db`. `app/main.py` imports config and calls `get_session_secret_key()` while constructing `SessionMiddleware`, so missing session secret already fails at import/app construction time.

Tests are protected by `tests/conftest.py`, which sets test-controlled `HYDRO_DATABASE_PATH`, `HYDRO_SESSION_SECRET`, and bootstrap password before importing `app.main`. The local runtime template validator in `scripts/validate_runtime_config.py` intentionally validates committed templates only, does not import `app.main`, and does not read `os.environ`. `.env.example` and `deploy/env/hydro.env.example` currently document production-oriented keys but do not include a mode variable. Deployment specs explicitly deferred startup fail-closed checks until a reliable production signal exists.

### Affected Areas
- `app/core/config.py` — central place to define the production-mode parser and fail-closed production checks because existing runtime environment reads already live here.
- `app/main.py` — app construction currently triggers session-secret validation; production checks can be invoked here or indirectly from config before middleware setup.
- `tests/conftest.py` — must keep dev/test imports from accidentally entering production mode; production behavior should be tested with isolated env and module reloads or pure helper functions.
- `tests/test_deployment_docs.py` — existing guard suite for env templates and runtime validator should add `HYDRO_ENV` parity and production-template expectations.
- `.env.example` and `deploy/env/hydro.env.example` — should document the explicit production signal with placeholders/safe value shape while preserving no-real-secret constraints.
- `scripts/validate_runtime_config.py` — should include the new key in template parity/validation without reading real env or importing the app.
- `docs/deployment.md` and `deploy/README.md` — should instruct operators to set production mode and explain that fail-closed checks apply only when the signal is active.
- `openspec/specs/deployment-readiness/spec.md` — should add requirements for the production signal and startup fail-closed behavior.

### Approaches
1. **`HYDRO_ENV=production` with exact-match production mode** — Add a string mode variable where only normalized `production` enables production-only fail-closed checks.
   - Pros: Explicit and conventional; extensible to future `development`/`test` wording; avoids boolean ambiguity; tests/dev remain unchanged when unset.
   - Cons: Requires docs/templates/tests update; typos like `prod` need a clear failure policy if present.
   - Effort: Medium

2. **Boolean `HYDRO_PRODUCTION=1` flag** — Add a dedicated boolean-like flag where `1` enables production checks.
   - Pros: Simple parser; mirrors existing `HYDRO_SESSION_COOKIE_SECURE=1` style.
   - Cons: Less descriptive; boolean env flags invite ambiguous values; harder to extend; accidental `0`/unset differences need careful docs.
   - Effort: Low

3. **Infer production from secure-cookie/database/secret values** — Treat secure cookies, absolute database paths, or missing dev-secret permission as production-like.
   - Pros: No new env key.
   - Cons: Unreliable and explicitly conflicts with the deferred-check rationale; can break local tests/dev or fail to protect real deployments.
   - Effort: Low

### Recommendation
Use `HYDRO_ENV=production` as the explicit production-mode signal, with an exact normalized value (`production`) as the only mode that enables production-only fail-closed checks. Keep unset/non-production behavior compatible with current tests and local development. Put the production-mode parser and checks in `app/core/config.py`, and trigger them during app construction before or alongside `SessionMiddleware` setup so production misconfiguration fails before serving requests.

Initial fail-closed checks should stay narrow: in production mode require a non-empty `HYDRO_SESSION_SECRET`, require `HYDRO_SESSION_COOKIE_SECURE=1`, reject `HYDRO_ALLOW_DEV_SECRET=1`, and require an explicit `HYDRO_DATABASE_PATH` rather than defaulting to repo-local `hydro.db`. Avoid checking real file existence, ownership, TLS, server state, secret strength beyond non-empty/present, or deployment automation. Update templates/docs/validator/specs/tests in the same review slice. Rollback is straightforward: remove/disable `HYDRO_ENV=production` in the runtime environment to return to existing startup behavior while reverting the code/docs change if needed.

For chained delivery, this can be split into small reviewable work units if needed: (1) config parser/checks with focused tests, (2) template validator/template/docs/spec updates. Keep tests with each behavior slice.

### Risks
- Adding checks at import/app-construction time can break tests if production mode leaks from the developer shell; tests should control or clear `HYDRO_ENV` around production-check cases.
- If `HYDRO_ENV` accepts aliases like `prod`, behavior becomes less predictable; prefer exact `production` and document unsupported values clearly.
- Runtime checks must not inspect real env files, server state, deployment notes, filesystem ownership, TLS, or secrets beyond process env values already supplied to the app.
- Template validation could be mistaken for validating real production configuration; docs must preserve the local-template-only boundary.

### Ready for Proposal
Yes — propose a narrowly scoped runtime config change that introduces `HYDRO_ENV=production` and production-only fail-closed startup checks, plus pytest coverage and template/docs/spec updates. Tell the orchestrator not to include server/deploy automation, real env-file reads, real secret inspection, CI billing fixes, or readiness claims.
