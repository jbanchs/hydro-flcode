# Tasks: Staging Server Bootstrap

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 160-260 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | One docs+test work unit |
| Delivery strategy | force-chained |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: feature-branch-chain
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Add RED static guards, docs checklist, and verification/archive prep | PR 1 | Base = feature/tracker branch; keep docs and tests together under budget. |

## Phase 1: RED Static Guards

- [x] 1.1 Extend `tests/test_deployment_docs.py` to fail until `docs/deployment.md` contains all audited host facts and required packages.
- [x] 1.2 Add forbidden-scope guards in `tests/test_deployment_docs.py` for SSH/SCP, scripts, CI, deploy automation, secrets, env/db reads, and Caddy/systemd config.
- [x] 1.3 Run `py -m pytest tests/test_deployment_docs.py` and confirm the new guards fail before docs updates.

## Phase 2: GREEN Documentation Checklist

- [x] 2.1 Add `docs/deployment.md` manual bootstrap section with Ubuntu 22.04, `apt`, `systemctl`, passworded `sudo`, Python 3.10, missing `git`/Caddy/`sqlite3`, 20G disk, and 2GiB RAM.
- [x] 2.2 Add operator-run prerequisite and verification checklist in `docs/deployment.md` for `git`, `python3-venv`, `sqlite3`, Python, venv, systemd, apt, sudo, disk, and memory.
- [x] 2.3 State in `docs/deployment.md` that Caddy is deferred, Python 3.10 is not Python 3.13 compatibility approval, and sudo passwords are entered interactively only.
- [x] 2.4 Update `deploy/README.md` with a docs-only pointer to the bootstrap checklist and no automation promise.

## Phase 3: REFACTOR and Verification

- [x] 3.1 Refactor `tests/test_deployment_docs.py` constants/regex helpers to keep manual apt wording allowed while prohibited automation still fails.
- [x] 3.2 Run `py -m pytest` from repo root and verify all bootstrap guard scenarios pass.
- [x] 3.3 Review `docs/deployment.md` and `deploy/README.md` for placeholders only; remove real hosts, credentials, private paths, or deployment instructions.

## Phase 4: Archive Prep

- [x] 4.1 Confirm `openspec/changes/staging-server-bootstrap/specs/deployment-readiness/spec.md` matches implemented docs and guards.
- [x] 4.2 Prepare verification notes for archive: changed files, `py -m pytest` result, and out-of-scope boundaries preserved.
