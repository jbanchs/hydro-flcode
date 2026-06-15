# Tasks: Production Deploy Plan

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 450-650 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 tests → PR 2 runtime templates/docs → PR 3 verification/archive |
| Delivery strategy | force-chained |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | RED validation guards | PR 1 | base = feature/tracker branch; tests fail before docs/templates exist. |
| 2 | Runtime templates and operator docs | PR 2 | base = PR 1 branch; make guards pass with placeholder-only artifacts. |
| 3 | Final verification/archive readiness | PR 3 | base = PR 2 branch; prove no secrets or server automation. |

## Phase 1: RED Static Validation

- [x] 1.1 Extend `tests/test_deployment_docs.py` to scan `.env.example`, `docs/deployment.md`, and `deploy/**/*` for secrets, real hosts/IPs, private paths, SSH targets, and copied deploy values.
- [x] 1.2 Add failing pytest assertions for `/etc/hydro/hydro.env`, `uvicorn app.main:app`, non-root service user, proxy-managed TLS, journald logs, firewall checklist, SQLite backup/restore, rollback, and manual validation.
- [x] 1.3 Add failing assertions rejecting SSH commands, provisioning, CI/CD deploy jobs, backup scripts, one-shot deploy automation, and any reference to server access automation.

## Phase 2: Runtime Templates and Docs

- [x] 2.1 Create `deploy/README.md` describing example-only scope, placeholder rules, validation order, and no-secrets/no-automation boundaries.
- [x] 2.2 Create `deploy/systemd/hydro.service.example` with `User=hydro`, `/etc/hydro/hydro.env`, placeholder working directory, direct `uvicorn app.main:app`, restart policy, and journald output.
- [x] 2.3 Create `deploy/env/hydro.env.example` aligned with config keys and `.env.example`; keep every value placeholder-only.
- [x] 2.4 Create `deploy/caddy/Caddyfile.example` with placeholder domain and private app bind target; TLS remains proxy-managed.
- [x] 2.5 Update `docs/deployment.md` with env placement, service install shape, logs, firewall/TLS checks, SQLite backup/restore, rollback, and explicit manual-only validation.

## Phase 3: GREEN/REFACTOR Validation

- [x] 3.1 Run `python -m pytest tests/test_deployment_docs.py`; adjust templates/docs until all deployment-readiness guards pass.
- [x] 3.2 Run full `python -m pytest` to verify documentation guards do not regress app tests.
- [x] 3.3 Refactor `tests/test_deployment_docs.py` helpers so forbidden-token scanning is readable and applies uniformly across deployment docs/templates.

## Phase 4: Verification and Archive Readiness

- [x] 4.1 Verify `openspec/changes/production-deploy-plan/specs/deployment-readiness/spec.md` scenarios map to passing pytest guards and docs/template content.
- [x] 4.2 Prepare verify evidence for `sdd-verify`: changed files, test commands, and confirmation that no real secrets, deploy automation, or server access instructions were added.
- [x] 4.3 After verification, prepare `sdd-archive` using the OpenSpec change artifacts; do not include real deployment data.
