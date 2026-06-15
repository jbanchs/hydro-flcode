# Proposal: Local OpenSpec Validation

## Intent

Make HYDRO's local OpenSpec validation expectations explicit and testable. Current archives mention `openspec validate <change> --strict`, but the CLI is not available locally; recent workflow uses `gentle-ai sdd-status`, which must not be presented as strict OpenSpec CLI validation.

## Scope

### In Scope
- Document the local validation ladder: `openspec validate <change> --strict` when an installed CLI exists, otherwise `gentle-ai sdd-status <change>` as a non-strict native status/archive-readiness signal.
- Add pytest guard coverage for OpenSpec config/archive expectations and validation wording.
- Preserve no-secrets, no-production, no-deployment, and no-new-CLI-dependency boundaries.

### Out of Scope
- Installing, pinning, or globally requiring an unverified OpenSpec CLI package.
- Claiming `gentle-ai sdd-status` performs strict OpenSpec schema validation.
- CI billing fixes, deployment automation, production config, secrets, or runtime app changes.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `deployment-readiness`: add requirements for local OpenSpec validation documentation and pytest guards while preserving documentation-only/no-secrets operational boundaries.

## Approach

Use the smallest documentation-plus-guard slice from exploration: update developer-facing/OpenSpec guidance, then add a focused pytest check using the existing `py -m pytest` runner. Tests should assert required repo-local OpenSpec structure/config expectations and prevent wording that equates `gentle-ai sdd-status` with strict CLI validation.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `README.md` | Modified | Document local OpenSpec validation commands and fallback boundary. |
| `openspec/config.yaml` | Modified | Make validation-tooling expectations explicit if needed. |
| `openspec/specs/deployment-readiness/spec.md` | Modified | Add spec requirement for local validation guidance/guards. |
| `tests/test_deployment_docs.py` | Modified | Add static pytest guard for OpenSpec config/archive guidance. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Fallback wording creates false confidence | Med | Explicitly state `gentle-ai sdd-status` is not strict OpenSpec CLI validation. |
| Tests become brittle against archives | Med | Check stable structure and current guidance, not broad archive text. |
| Scope creep into tooling/deployment | Low | Keep CLI installation, CI, secrets, and production changes out of scope. |

## Rollback Plan

Revert the proposal's docs/spec/test changes. No runtime, dependency, secret, CI, or deployment state is changed.

## Dependencies

- Existing pytest runner: `py -m pytest`.
- Existing local `gentle-ai` command availability.

## Success Criteria

- [ ] README/OpenSpec guidance distinguishes strict CLI validation from `gentle-ai sdd-status` fallback.
- [ ] `py -m pytest` includes a guard for local OpenSpec validation/config/archive expectations.
- [ ] No new CLI dependency, deployment automation, production config, or secrets are introduced.
