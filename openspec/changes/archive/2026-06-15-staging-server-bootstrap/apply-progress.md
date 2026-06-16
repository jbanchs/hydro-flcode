# Apply Progress: Staging Server Bootstrap

## Status

- Mode: Strict TDD
- Work unit: docs+static-guards
- Delivery strategy: force-chained
- Chain strategy: feature-branch-chain
- Result: complete

## Completed Tasks

- [x] 1.1 Extend `tests/test_deployment_docs.py` to fail until `docs/deployment.md` contains all audited host facts and required packages.
- [x] 1.2 Add forbidden-scope guards in `tests/test_deployment_docs.py` for SSH/SCP, scripts, CI, deploy automation, secrets, env/db reads, and Caddy/systemd config.
- [x] 1.3 Run `py -m pytest tests/test_deployment_docs.py` and confirm the new guards fail before docs updates.
- [x] 2.1 Add `docs/deployment.md` manual bootstrap section with Ubuntu 22.04, `apt`, `systemctl`, passworded `sudo`, Python 3.10, missing `git`/Caddy/`sqlite3`, 20G disk, and 2GiB RAM.
- [x] 2.2 Add operator-run prerequisite and verification checklist in `docs/deployment.md` for `git`, `python3-venv`, `sqlite3`, Python, venv, systemd, apt, sudo, disk, and memory.
- [x] 2.3 State in `docs/deployment.md` that Caddy is deferred, Python 3.10 is not Python 3.13 compatibility approval, and sudo passwords are entered interactively only.
- [x] 2.4 Update `deploy/README.md` with a docs-only pointer to the bootstrap checklist and no automation promise.
- [x] 3.1 Refactor `tests/test_deployment_docs.py` constants/regex helpers to keep manual apt wording allowed while prohibited automation still fails.
- [x] 3.2 Run `py -m pytest` from repo root and verify all bootstrap guard scenarios pass.
- [x] 3.3 Review `docs/deployment.md` and `deploy/README.md` for placeholders only; remove real hosts, credentials, private paths, or deployment instructions.
- [x] 4.1 Confirm `openspec/changes/staging-server-bootstrap/specs/deployment-readiness/spec.md` matches implemented docs and guards.
- [x] 4.2 Prepare verification notes for archive: changed files, `py -m pytest` result, and out-of-scope boundaries preserved.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1-1.3 | `tests/test_deployment_docs.py` | Unit/static | ✅ 26/26 baseline | ✅ Added required fact/package/command guards first | ✅ Focused guard run failed as expected before docs: 3 failed, 26 passed | ✅ Guard set covers facts, packages, commands, and boundaries | ✅ Constants added for readable guard maintenance |
| 2.1-2.4 | `tests/test_deployment_docs.py` | Unit/static | ✅ RED already captured | ✅ Existing RED guards drove docs changes | ✅ Focused run reached green after docs/refactor: 29 passed | ✅ Multiple checks cover docs and deploy index | ✅ Wording adjusted to avoid false positives while preserving scope |
| 3.1-3.3 | `tests/test_deployment_docs.py` | Unit/static | ✅ 29/29 focused green before full suite | ✅ Boundary regex failures exposed allowed documentation wording | ✅ Full suite passed: 91 passed | ✅ Allowed-language exceptions stay explicit and narrow | ✅ No additional refactor needed after full green |
| 4.1-4.2 | `tests/test_deployment_docs.py` | Unit/static | ✅ 91/91 full suite | ✅ Completion verified against spec and tasks | ✅ Tasks and apply-progress updated after green | ➖ Documentation/archive prep only | ➖ None needed |

## Test Summary

- Total tests written: 3
- Total tests passing: 91
- Layers used: Unit/static (3 new guards)
- Approval tests: None — no refactoring tasks beyond guard cleanup
- Pure functions created: 0

## Tests Run

- `py -m pytest tests/test_deployment_docs.py` baseline: 26 passed
- `py -m pytest tests/test_deployment_docs.py` RED: 3 failed, 26 passed
- `py -m pytest tests/test_deployment_docs.py` GREEN: 29 passed
- `py -m pytest`: 91 passed

## Files Changed

- `tests/test_deployment_docs.py` — added static guards for staging bootstrap facts, package prerequisites, verification commands, and prohibited scope.
- `docs/deployment.md` — added manual staging server bootstrap prerequisite checklist and operator-run verification checklist.
- `deploy/README.md` — added docs-only pointer to the bootstrap checklist and preserved no-automation boundary.
- `openspec/changes/staging-server-bootstrap/tasks.md` — marked all tasks complete.
- `openspec/changes/staging-server-bootstrap/apply-progress.md` — recorded strict TDD evidence and verification notes.

## Boundary Notes

- No server access, SSH/SCP command examples, deployment automation, scripts, Caddy/systemd configuration, CI changes, secrets, real env files, or real databases were added.
- Caddy remains deferred; later approval is described only as package-only and unconfigured.
- Python 3.10 is documented as an audited host fact, not compatibility approval for HYDRO's Python 3.13 baseline.
