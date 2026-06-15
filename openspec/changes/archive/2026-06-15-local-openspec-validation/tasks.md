# Tasks: Local OpenSpec Validation

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 120-220 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single focused docs+guard PR |
| Delivery strategy | force-chained |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: stacked-to-main
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Add pytest guards, docs/config wording, and archive-ready spec sync | PR 1 | Base = main; keep tests with docs/config changes. |

## Phase 1: RED Guards

- [x] 1.1 Add failing assertions in `tests/test_deployment_docs.py` for README validation ladder wording and `py -m pytest` verification.
- [x] 1.2 Add failing assertions in `tests/test_deployment_docs.py` rejecting claims that `gentle-ai sdd-status` is strict OpenSpec CLI/schema validation.
- [x] 1.3 Add failing assertions in `tests/test_deployment_docs.py` for stable `openspec/config.yaml` local validation expectations.

## Phase 2: GREEN Docs and Config

- [x] 2.1 Update `README.md` with `openspec validate local-openspec-validation --strict` only when a verified CLI exists.
- [x] 2.2 Update `README.md` to describe `gentle-ai sdd-status local-openspec-validation` as native status/archive-readiness, not strict schema validation.
- [x] 2.3 Update `openspec/config.yaml` rules/context with local validation ladder expectations; do not add executable CLI dependency.

## Phase 3: Spec and Archive Prep

- [x] 3.1 Sync `openspec/specs/deployment-readiness/spec.md` with the accepted local validation guidance and no-deploy/no-secrets boundaries.
- [x] 3.2 Prepare archive readiness by ensuring `openspec/changes/local-openspec-validation/` contains proposal, spec, design, and this `tasks.md`.

## Phase 4: Verification and Refactor

- [x] 4.1 Run `py -m pytest tests/test_deployment_docs.py` and fix only guard/docs issues.
- [x] 4.2 Run `py -m pytest` for full local verification.
- [x] 4.3 Refactor brittle string checks in `tests/test_deployment_docs.py` into small helpers only if needed.
