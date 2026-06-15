# Tasks: Prepare Deployment

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 220-320 |
| 400-line budget risk | Medium |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 docs/tests → PR 2 verification/archive |
| Delivery strategy | force-chained |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Add deployment docs, `.env.example`, README link, and doc guards | PR 1 | Base = feature/tracker branch; complete with pytest validation. |
| 2 | Run verification, OpenSpec validation, and archive readiness checks | PR 2 | Base = PR 1 branch; no runtime/deploy changes. |

## Phase 1: RED Documentation Guards

- [x] 1.1 Create `tests/test_deployment_docs.py` asserting `.env.example` exists, includes required HYDRO keys, and uses placeholder-only values.
- [x] 1.2 Add tests rejecting real-looking secrets, private hostnames/IPs, tokens, passwords, and references to `specs/DEPLOY_INFO.md` in docs/examples.
- [x] 1.3 Add tests requiring `docs/deployment.md` content for TLS/reverse proxy, secure cookies, firewall, non-root service user, SQLite ownership, backup/rollback, and destructive `scripts/init_db.py` warning.
- [x] 1.4 Add tests requiring `README.md` links to `docs/deployment.md` and `.env.example` and states this is not deploy automation.

## Phase 2: GREEN Deployment Artifacts

- [x] 2.1 Create `.env.example` with placeholders for `HYDRO_SESSION_SECRET`, `HYDRO_DATABASE_PATH`, `HYDRO_SESSION_COOKIE_SECURE`, bootstrap admin values, and dev-only fallback warning.
- [x] 2.2 Create `docs/deployment.md` as a manual readiness runbook covering scope boundaries, secret handling, runtime env, process-manager command, reverse proxy/TLS, firewall, and non-root operation.
- [x] 2.3 Document SQLite production path ownership, pre-release backup, restore/rollback expectations, and explicit destructive-init acceptance for `scripts/init_db.py`.
- [x] 2.4 Update `README.md` with Deployment Readiness links and a no-automation/no-secrets-in-Git note.

## Phase 3: REFACTOR and Validation

- [x] 3.1 Run `python -m pytest tests/test_deployment_docs.py`; refine tests/docs until the doc guard passes.
- [x] 3.2 Run full `python -m pytest` to prove existing FastAPI/SQLite behavior remains unchanged.
- [x] 3.3 Attempt `openspec validate prepare-deployment --strict`; document local OpenSpec CLI unavailability as an accepted tooling warning without claiming successful validation.

## Phase 4: Chain and Archive Readiness

- [x] 4.1 Keep PR 1 focused on docs/examples/tests under the 400-line budget with tests committed in the same work unit.
- [x] 4.2 Prepare PR 2 for verification evidence and archive readiness after PR 1; confirm no server, CI deploy, provisioning, or secret files changed.
- [x] 4.3 Confirm archive remains intentionally blocked until OpenSpec CLI validation can run and pass; do not fake archive readiness.
