# Delta for Deployment Readiness

## ADDED Requirements

### Requirement: Repo-Local Staging Handoff Checklist

Deployment documentation MUST provide a repo-local staging handoff checklist for first MVP validation. The checklist MUST state that staging uses `HYDRO_ENV=production` with staging-specific secret values supplied outside Git, and MUST NOT introduce `HYDRO_ENV=staging`, real deployment execution, server access, secret reads, env-file reads, database access, scripts, CI gates, or readiness semantics for `/healthz`.

#### Scenario: Maintainer reviews staging handoff

- GIVEN a maintainer opens the staging handoff checklist
- WHEN they inspect staging configuration guidance
- THEN `HYDRO_ENV=production` MUST be identified as the staging runtime mode
- AND staging secrets MUST be described as operator-supplied outside Git.

#### Scenario: Staging scope expansion is rejected

- GIVEN staging docs propose `HYDRO_ENV=staging`, server access, real secrets, deploy scripts, CI gates, or database reads
- WHEN deployment-readiness review runs
- THEN the change MUST be considered non-compliant until those items are removed.

### Requirement: Staging Dry-Run Checklist

Deployment documentation MUST provide a local dry-run checklist using existing local validation only. The checklist MUST include the runtime-template validator and pytest runner, and MUST remain placeholder-only, non-deploying, and repo-local.

#### Scenario: Maintainer performs dry run locally

- GIVEN the repository is checked out without real staging secrets
- WHEN the maintainer follows the dry-run checklist
- THEN they MUST be directed to run existing local validation such as `py scripts/validate_runtime_config.py` and `py -m pytest`
- AND no real env, secret, server, deployment target, or `hydro.db` access MUST be required.

#### Scenario: Dry run remains documentation-only

- GIVEN a dry-run checklist update is reviewed
- WHEN it adds scripts, deploy automation, CI gate changes, server probes, or real config reads
- THEN deployment-readiness review MUST reject it for this slice.

### Requirement: Manual Staging Validation Runbook

Deployment documentation MUST provide an operator-owned manual staging validation runbook for after an out-of-band staging deployment. The runbook MUST cover `/healthz` liveness, `/login`, authenticated `/`, Ask HYDRO citation behavior, logs, rollback, and backup confirmation without performing or automating deployment.

#### Scenario: Operator validates out-of-band staging

- GIVEN staging has already been deployed outside this repository slice
- WHEN the operator follows the manual staging runbook
- THEN they MUST validate `/healthz`, `/login`, authenticated `/`, citation-backed Ask HYDRO behavior, logs, rollback readiness, and backup confirmation.

#### Scenario: Healthz remains liveness-only

- GIVEN the runbook references `/healthz`
- WHEN reviewers inspect the staging validation steps
- THEN `/healthz` MUST be described as liveness-only
- AND it MUST NOT be treated as readiness, database, dependency, or authenticated workflow validation.

### Requirement: Pytest Guards for Staging Boundaries

The test suite MUST include local pytest static guards for staging readiness wording and boundaries. Guards MUST assert required concepts rather than brittle exact prose, including production-like staging with `HYDRO_ENV=production`, placeholder-only values, no `HYDRO_ENV=staging`, no real deployment/server/secrets/env/db access, no scripts or CI gate changes, and `/healthz` liveness-only wording.

#### Scenario: Required staging concepts are guarded

- GIVEN staging readiness documentation is changed
- WHEN `py -m pytest` runs locally
- THEN guards MUST fail if required staging handoff, dry-run, manual validation, placeholder-only, or liveness-only concepts are missing.

#### Scenario: Prohibited staging concepts are guarded

- GIVEN docs or tests introduce `HYDRO_ENV=staging`, real secret/env/db/server access, deploy automation, scripts, or CI gate changes
- WHEN `py -m pytest` runs locally
- THEN the relevant static guard MUST fail before implementation proceeds.

## MODIFIED Requirements

None.

## REMOVED Requirements

None.

## RENAMED Requirements

None.
