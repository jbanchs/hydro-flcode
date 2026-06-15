# Apply Progress: Production Deploy Plan

## Status

- **Change**: `production-deploy-plan`
- **Mode**: Strict TDD
- **Artifact store**: OpenSpec file artifact restored from prior apply-progress evidence
- **Local test runner override**: `py -m pytest`
- **Workload / PR boundary**: Chained PR slices using `feature-branch-chain`
- **Current action**: Recover missing OpenSpec `apply-progress.md` only; no runtime code changed

## Task Completion Summary

- [x] 1.1 Extended `tests/test_deployment_docs.py` to scan `.env.example`, `docs/deployment.md`, and `deploy/**/*` for forbidden deployment data.
- [x] 1.2 Added runtime artifact/doc contract assertions for required paths and operations guidance.
- [x] 1.3 Added assertions rejecting server access and deployment automation patterns.
- [x] 2.1 Created `deploy/README.md` with example-only scope, placeholder rules, validation order, and no-secrets/no-automation boundaries.
- [x] 2.2 Created `deploy/systemd/hydro.service.example` with non-root `hydro`, `/etc/hydro/hydro.env`, placeholder working directory, direct `uvicorn app.main:app`, restart policy, and journald output.
- [x] 2.3 Created `deploy/env/hydro.env.example` aligned with required HYDRO env keys and placeholder-only values.
- [x] 2.4 Created `deploy/caddy/Caddyfile.example` with placeholder domain and private bind target; TLS remains proxy-managed.
- [x] 2.5 Updated `docs/deployment.md` with env placement, service shape, logs, firewall/TLS checks, SQLite backup/restore, rollback, and manual-only validation.
- [x] 3.1 Ran deployment-document guards and adjusted docs/templates until all deployment-readiness guards passed.
- [x] 3.2 Ran the full pytest suite to verify documentation guards did not regress app tests.
- [x] 3.3 Refactored `tests/test_deployment_docs.py` helpers so forbidden-token scanning is readable and uniform.
- [x] 4.1 Verified deployment-readiness spec scenarios map to passing pytest guards and docs/template content.
- [x] 4.2 Prepared verify evidence for `sdd-verify`: changed files, test commands, and confirmation that real secrets, deploy automation, and server access instructions were not added.
- [x] 4.3 Prepared archive readiness using OpenSpec artifacts; archive was not run.

## TDD Cycle Evidence

| Task / PR Slice | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|---|---|---|---|---|---|---|---|
| PR 1: validation guards (tasks 1.1-1.3) | `tests/test_deployment_docs.py` | Static/unit | Baseline guards preserved | Tests written first for forbidden deployment data, required runtime guidance, and automation rejection | `py -m pytest tests/test_deployment_docs.py` -> 4 passed, 2 skipped | Full suite confirmed existing behavior: `py -m pytest` -> 38 passed, 2 skipped | Guard structure prepared for later runtime artifacts |
| PR 2: runtime templates/docs (tasks 2.1-2.5, 3.1-3.2) | `tests/test_deployment_docs.py` | Static/unit + full suite | PR 1 state: 4 passed, 2 skipped | After unskipping PR 2 guards: 2 failed, 4 passed until templates/docs existed | Deployment docs: `py -m pytest tests/test_deployment_docs.py` -> 6 passed; full suite: `py -m pytest` -> 40 passed | Required artifacts, placeholder-only values, service/env/proxy shape, logs, firewall/TLS, SQLite backup/restore, rollback, and manual validation all covered | Documentation wording and examples adjusted to satisfy guards without real deployment data |
| PR 3: verification/archive readiness (tasks 3.3, 4.1-4.3) | `tests/test_deployment_docs.py` + OpenSpec artifacts | Static verification | PR 2 state: deployment docs 6 passed, full suite 40 passed | Existing guards and OpenSpec scenarios defined verification evidence before helper refactor/archive readiness | Deployment docs: `py -m pytest tests/test_deployment_docs.py` -> 6 passed; full suite: `py -m pytest` -> 40 passed | Spec scenarios mapped to guards for runtime templates, real-data exclusion, operator checklist, and automation rejection | Helper extraction/readability completed; no archive mutation performed |
| Recovery artifact: file apply-progress | `openspec/changes/production-deploy-plan/apply-progress.md` | Documentation/evidence | Prior Engram apply-progress and completed `tasks.md` read | Verification failure identified missing OpenSpec file artifact with TDD evidence table | This file restores cumulative TDD evidence; validation run required after creation | Evidence includes all completed PR slices and test outcomes | No runtime code changed |

## Files Changed Summary

| File | Action | What Was Done |
|---|---|---|
| `tests/test_deployment_docs.py` | Modified in prior PR slices | Added and refactored static deployment-readiness guards for placeholders, forbidden deployment data, runtime guidance, and no automation. |
| `deploy/README.md` | Created in prior PR slices | Documented example-only runtime artifact scope, validation order, and no-secrets/no-automation boundaries. |
| `deploy/systemd/hydro.service.example` | Created in prior PR slices | Added placeholder systemd service using non-root `hydro`, `/etc/hydro/hydro.env`, direct `uvicorn app.main:app`, restart policy, and journald output. |
| `deploy/env/hydro.env.example` | Created in prior PR slices | Added placeholder-only production env template aligned with HYDRO config keys. |
| `deploy/caddy/Caddyfile.example` | Created in prior PR slices | Added placeholder Caddy reverse proxy/TLS example forwarding to a private app bind target. |
| `docs/deployment.md` | Modified in prior PR slices | Added runtime artifact links, env placement, service install shape, logs, firewall/TLS checks, SQLite backup/restore, rollback, and manual validation guidance. |
| `openspec/changes/production-deploy-plan/tasks.md` | Modified in prior PR slices | Marked all apply tasks complete. |
| `openspec/changes/production-deploy-plan/apply-progress.md` | Created in this recovery slice | Restored cumulative Strict TDD evidence required by `sdd-verify`. |

## Sensitive-File Handling

- The local ignored deployment secret note was not read, opened, copied, summarized, or referenced by name/path in committed OpenSpec artifacts.
- This change keeps deployment artifacts placeholder-only and does not include real secrets, hostnames, IPs, private paths, SSH targets, or copied deployment values.
- No server access, provisioning, CI/CD deploy job, backup script, one-shot deploy automation, or runtime code change was added in this recovery slice.

## OpenSpec CLI Warning

- OpenSpec CLI availability is not assumed for this environment.
- Verification should use the restored file artifact plus `py -m pytest`; if OpenSpec CLI is unavailable, treat CLI validation as skipped with this warning rather than as implementation evidence.

## Tests Recorded From Prior PR Slices

- PR 1 validation guards: `py -m pytest tests/test_deployment_docs.py` -> 4 passed, 2 skipped; full suite `py -m pytest` -> 38 passed, 2 skipped.
- PR 2 runtime templates/docs: RED after unskipping PR 2 guards -> 2 failed, 4 passed; GREEN deployment docs -> 6 passed; full suite -> 40 passed.
- PR 3 verification/archive readiness: deployment docs -> 6 passed; full suite -> 40 passed.

## Remaining Tasks

None. Apply tasks are complete. Next recommended phase: `sdd-verify production-deploy-plan`.
