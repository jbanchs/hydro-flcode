# Proposal: Sanitize Deploy Info References

## Intent

Remove tracked references to a sensitive ignored local deployment secret note from OpenSpec archive artifacts, while preserving audit meaning. This is a narrow security-redaction exception to the normal archive immutability rule.

## Scope

### In Scope
- Sanitize confirmed tracked archive references to generic wording.
- Add or strengthen pytest coverage so tracked archived OpenSpec markdown cannot reintroduce the sensitive local note filename/path pattern.
- Document that current tracked files are cleaned without reading the ignored local note.

### Out of Scope
- Git history rewrite or purge of prior commits.
- Reading, opening, copying, or summarizing the ignored local note.
- Server, deployment, CI/CD, provisioning, or runtime configuration changes.
- Broad rewrite of unrelated deployment documentation.

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `deployment-readiness`: Strengthen secret-handling guardrails so deployment readiness artifacts and tests reject tracked references to sensitive local deployment-note filenames/paths.

## Approach

Follow the exploration recommendation: replace only confirmed tracked archive disclosure with generic wording such as "ignored local deployment secret note," then extend `tests/test_deployment_docs.py` to scan archived OpenSpec markdown for the prohibited sensitive-reference pattern. Keep the guard focused enough to catch the known disclosure without blocking generic secret-handling language.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/changes/archive/2026-06-15-prepare-deployment/exploration.md` | Modified | Replace sensitive local note filename/path wording with generic language. |
| `tests/test_deployment_docs.py` | Modified | Add archive markdown guard against reintroducing the sensitive local note reference pattern. |
| `openspec/changes/sanitize-deploy-info-references/*` | New | SDD artifacts for the sanitation exception. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Archive audit trail is modified | Med | Limit edit to security redaction and preserve meaning. |
| New artifacts disclose the sensitive reference | Low | Use generic wording only. |
| Guard is too broad | Low | Target the known filename/path shape, not generic secret terms. |
| Old Git history still contains reference | Med | Explicitly state no history rewrite is included. |

## Rollback Plan

Revert the archive wording change, test update, and this active change folder. No deployment or runtime state is affected.

## Dependencies

- Existing pytest runner: `python -m pytest`.
- Existing deployment-readiness spec and deployment docs guard tests.

## Success Criteria

- [ ] Current tracked files no longer expose the sensitive local note filename/path.
- [ ] `python -m pytest` fails if archived OpenSpec markdown reintroduces the prohibited reference pattern.
- [ ] No ignored local note is read or copied.
- [ ] No server, deploy, or runtime behavior changes are introduced.
