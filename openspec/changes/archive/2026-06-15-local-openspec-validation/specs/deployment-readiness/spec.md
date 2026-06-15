# Delta for Deployment Readiness

## ADDED Requirements

### Requirement: Local OpenSpec Validation Guidance

Developer-facing SDD/OpenSpec guidance MUST document the local validation ladder for active changes: use `openspec validate <change> --strict` only when a verified OpenSpec CLI is already installed, otherwise use `gentle-ai sdd-status <change>` as a native status and archive-readiness signal. The guidance MUST state that `gentle-ai sdd-status` is not strict OpenSpec CLI schema validation.

#### Scenario: Strict CLI is available

- GIVEN a developer has a verified local OpenSpec CLI available
- WHEN they validate `local-openspec-validation`
- THEN guidance MUST direct them to run `openspec validate local-openspec-validation --strict`
- AND the result MAY be described as strict OpenSpec CLI validation.

#### Scenario: Native fallback is used

- GIVEN no verified local OpenSpec CLI is available
- WHEN a developer checks `local-openspec-validation`
- THEN guidance MUST direct them to `gentle-ai sdd-status local-openspec-validation`
- AND it MUST NOT describe that command as strict OpenSpec CLI schema validation.

### Requirement: No Unverified CLI or Deployment Scope Expansion

This change MUST NOT install, pin, globally require, or recommend an unverified OpenSpec CLI package. It MUST NOT introduce secrets, deployment automation, production config changes, CI billing fixes, runtime app changes, or remote-service dependencies.

#### Scenario: CLI installation is proposed

- GIVEN a change adds installation or pinning for an unverified OpenSpec CLI
- WHEN deployment-readiness review runs
- THEN the change MUST be rejected as out of scope.

#### Scenario: Operational boundaries are preserved

- GIVEN validation documentation or guards are updated
- WHEN reviewers inspect the change
- THEN no secrets, deployment automation, production config, CI billing fix, or runtime app behavior MUST be added.

### Requirement: Pytest Guards for Validation Wording and Artifacts

The test suite MUST include local pytest guard coverage for OpenSpec validation wording and stable artifact expectations. The guard MUST prevent wording that equates `gentle-ai sdd-status` with strict OpenSpec CLI validation and SHOULD verify repo-local OpenSpec config/archive expectations without depending on broad archive rewrites.

#### Scenario: Misleading fallback wording is detected

- GIVEN tracked documentation claims `gentle-ai sdd-status` performs strict OpenSpec CLI validation
- WHEN `py -m pytest` runs locally
- THEN the relevant guard MUST fail.

#### Scenario: Required OpenSpec expectations remain present

- GIVEN tracked OpenSpec config or documentation removes required local validation guidance
- WHEN `py -m pytest` runs locally
- THEN the relevant guard MUST fail.
