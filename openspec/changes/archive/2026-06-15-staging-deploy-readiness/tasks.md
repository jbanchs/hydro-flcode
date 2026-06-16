# Tasks: Staging Deploy Readiness

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 160-260 |
| 400-line budget risk | Low |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 docs+static guards |
| Delivery strategy | force-chained |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: stacked-to-main
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Add staging handoff docs with RED pytest guards | PR 1 | Single docs+tests slice; tests stay with guarded docs. |

## Phase 1: RED Static Guards

- [x] 1.1 Add failing staging concept guards to `tests/test_deployment_docs.py` for `docs/deployment.md`: `HYDRO_ENV=production`, staging secrets outside Git, placeholder-only dry run, `/healthz` liveness-only, `/login`, authenticated `/`, Ask HYDRO, logs, rollback, backups.
- [x] 1.2 Add failing forbidden-boundary guards to `tests/test_deployment_docs.py` rejecting `HYDRO_ENV=staging`, deploy automation, SSH/SCP, server probes, real env/secret/db reads, `hydro.db`, script additions, and CI gate changes.
- [x] 1.3 Run `py -m pytest tests/test_deployment_docs.py` and capture the expected RED failures for missing staging docs.

## Phase 2: GREEN Documentation

- [x] 2.1 Update `docs/deployment.md` with a repo-local staging handoff checklist using `HYDRO_ENV=production` and operator-supplied staging secrets outside Git.
- [x] 2.2 Add a local dry-run checklist to `docs/deployment.md` using only `py scripts/validate_runtime_config.py` and `py -m pytest`, with no real secrets, env files, servers, deployment targets, or `hydro.db`.
- [x] 2.3 Add an operator-owned post-deploy runbook to `docs/deployment.md` covering `/healthz` liveness, `/login`, authenticated `/`, search, citation-backed Ask HYDRO behavior, logs, rollback, and backup confirmation.
- [x] 2.4 Update `deploy/README.md` to link staging readiness into the runtime artifact order while preserving placeholder-only, non-deploying scope.
- [x] 2.5 Modify `README.md` only if existing deployment-readiness discovery does not expose `docs/deployment.md` clearly.

## Phase 3: REFACTOR Guards

- [x] 3.1 Refactor `tests/test_deployment_docs.py` guard helpers into compact concept groups and regex checks without asserting long exact prose.
- [x] 3.2 Run `py -m pytest tests/test_deployment_docs.py` and verify GREEN for required staging scenarios and prohibited scope expansion.

## Phase 4: Verification and Archive Prep

- [x] 4.1 Run full local validation with `py -m pytest`; if available, run `openspec validate staging-deploy-readiness --strict` or record the configured fallback.
- [x] 4.2 Confirm no runtime, server, script, CI, database, secret, or real env-file changes were made outside `docs/deployment.md`, `deploy/README.md`, optional `README.md`, and `tests/test_deployment_docs.py`.
- [x] 4.3 Prepare archive notes mapping tasks to deployment-readiness requirements and note rollback as reverting docs, tests, and OpenSpec artifacts only.
