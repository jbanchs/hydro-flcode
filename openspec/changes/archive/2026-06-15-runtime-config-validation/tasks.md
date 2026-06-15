# Tasks: Runtime Config Validation

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 220-340 |
| 400-line budget risk | Medium |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 only unless budget drifts; keep tests, validator, docs together |
| Delivery strategy | force-chained |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Add local template validator with RED/GREEN tests and docs | PR 1 | Base = feature/tracker branch; keep under 400 lines |

## Phase 1: RED Tests / Contracts

- [x] 1.1 Add failing tests in `tests/test_deployment_docs.py` for parser errors, key parity, missing/extra keys, and malformed `KEY=VALUE` lines.
- [x] 1.2 Add failing tests in `tests/test_deployment_docs.py` rejecting real-looking secrets, hostnames/IPs, private paths, and `HYDRO_ALLOW_DEV_SECRET=1`.
- [x] 1.3 Add failing tests proving validator only reads `.env.example` and `deploy/env/hydro.env.example`, never `.env`, `os.environ`, `app.main`, servers, or deploy tools.

## Phase 2: GREEN Validator

- [x] 2.1 Create `scripts/validate_runtime_config.py` with pure parsing helpers, required-key contract, and repo-relative template paths.
- [x] 2.2 Implement validation for exact key parity, angle-bracket placeholders, `HYDRO_SESSION_COOKIE_SECURE=1`, and non-zero failure output.
- [x] 2.3 Align `.env.example` and `deploy/env/hydro.env.example` only if required by the validator contract.

## Phase 3: Docs / Checklist

- [x] 3.1 Update `docs/deployment.md` with `py scripts/validate_runtime_config.py` as local template preflight only, not production readiness.
- [x] 3.2 Update `deploy/README.md` manual checklist with the validator command and explicit no server/secret/deploy automation wording.
- [x] 3.3 Update `openspec/specs/deployment-readiness/spec.md` if archived baseline needs the local validator requirement wording.

## Phase 4: Verification / Archive Prep

- [x] 4.1 Run `py -m pytest` and confirm validator behavior, docs wording, and boundary guards pass.
- [x] 4.2 Verify no new startup fail-closed checks, secret reads, server probes, deploy jobs, or production-readiness claims were added.
- [x] 4.3 Prepare archive notes mapping implementation to deployment-readiness scenarios and rollback scope.
