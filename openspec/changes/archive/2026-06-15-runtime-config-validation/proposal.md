# Proposal: Runtime Config Validation

## Intent

Add a local, non-deploying validator for committed runtime/env templates so maintainers can catch drift between HYDRO's documented production placeholders and app expectations before deployment work. This slice improves pre-deploy confidence without reading real env files, touching servers, handling secrets, or claiming production readiness.

## Scope

### In Scope
- Add `scripts/validate_runtime_config.py` to validate committed placeholder templates only.
- Add pytest coverage for template parity, validator behavior, docs wording, and boundary protections.
- Update deployment docs and OpenSpec requirements to advertise the local validator accurately.

### Out of Scope
- Reading `.env`, `/etc/hydro/hydro.env`, secret managers, or any real deployment environment.
- Server access, deployment automation, CI billing fixes, infrastructure changes, or production readiness claims.
- App startup fail-closed behavior beyond the existing session-secret guard; defer until a reliable production-mode signal exists.

## Capabilities

### New Capabilities
None

### Modified Capabilities
- `deployment-readiness`: add requirements for local runtime/env template validation while preserving no-secrets, no-server, no-automation boundaries.

## Approach

Implement a small script that parses `.env.example` and `deploy/env/hydro.env.example`, verifies required key parity, placeholder-only sensitive/deployment-specific values, expected secure-cookie production template value, and no dev-secret production bypass. Keep validation pure/local and avoid importing `app.main`; reuse constants/helpers only if they have no import-time side effects.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `scripts/validate_runtime_config.py` | New | Local template validator command. |
| `tests/test_deployment_docs.py` | Modified | Guards validator behavior, template parity, and wording. |
| `.env.example` | Modified | Align placeholder expectations if needed. |
| `deploy/env/hydro.env.example` | Modified | Align deploy template shape if needed. |
| `docs/deployment.md`, `deploy/README.md` | Modified | Document validator as local template preflight only. |
| `openspec/specs/deployment-readiness/spec.md` | Modified | Delta requirements for this capability. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Validator is mistaken for production readiness proof | Med | Docs/spec must say template-only, local-only, non-deploying. |
| Import-time config guard breaks tests | Low | Avoid importing `app.main`; isolate pure parsing. |
| Secret/host guards flag placeholders | Med | Test allowed placeholder patterns explicitly. |

## Rollback Plan

Revert the validator script, related pytest/docs changes, and deployment-readiness spec delta. Existing runtime behavior and deployment docs remain usable because this slice does not change app startup or deployment automation.

## Dependencies

- Existing pytest runner: `py -m pytest`.
- Existing deployment-readiness spec and committed env templates.

## Success Criteria

- [ ] `py -m pytest` validates template parity and local validator behavior.
- [ ] Docs describe the command as local template/preflight validation only.
- [ ] No real env files, secrets, servers, deploy automation, or startup fail-closed expansion are introduced.
