## Exploration: sanitize-deploy-info-references

### Current State
HYDRO uses OpenSpec as the SDD artifact store. The active deployment-readiness spec and current deployment documentation already use generic secret-handling language and tests guard committed deployment docs/templates from referencing the sensitive deploy-note path. However, one archived OpenSpec exploration artifact still contains the historical sensitive filename/path reference. The sensitive ignored local file was not read, opened, copied, or summarized during this exploration.

### Affected Areas
- `openspec/changes/archive/2026-06-15-prepare-deployment/exploration.md` — contains the historical sensitive filename/path reference and should be sanitized to generic wording.
- `openspec/changes/archive/2026-06-15-prepare-deployment/*` — adjacent archived artifacts already use generic wording or guard language; review scope should stay limited to confirmed references.
- `openspec/changes/archive/2026-06-15-production-deploy-plan/*` — already uses generic wording such as local ignored deployment secret note; no cleanup needed from the safe search results.
- `tests/test_deployment_docs.py` — existing guard covers deployment docs/templates and README, but not archived OpenSpec artifacts.

### Approaches
1. **Small archive-sanitization slice** — Replace only confirmed historical filename/path references in tracked OpenSpec archive artifacts with generic wording such as "ignored local deployment secret note" and add a focused guard for archived OpenSpec markdown.
   - Pros: smallest safe cleanup; avoids reading the ignored file; keeps review under the 400-line budget; preserves artifact meaning while removing sensitive path disclosure.
   - Cons: rewrites an archived audit artifact, so the change must explicitly document why this exception is allowed.
   - Effort: Low

2. **Broad repository rewrite** — Sweep all tracked markdown/docs/spec files and rewrite every mention related to deployment secrets into a single sanitized phrase.
   - Pros: maximizes consistency across historical artifacts.
   - Cons: higher audit-trail churn; risks unnecessary semantic changes; more review noise for little security gain.
   - Effort: Medium

### Recommendation
Proceed with Approach 1. Although OpenSpec convention says archived changes are an audit trail and normally should not be modified, this is a security sanitation exception: rewriting already-committed archive text is acceptable when the edit only removes disclosure of a sensitive local filename/path and preserves the artifact's operational meaning. The implementation should not read the ignored file, should not name its exact path in new artifacts, and should replace the confirmed historical reference with generic wording only.

Add or extend tests/guards so `python -m pytest` fails when tracked OpenSpec archive markdown contains the sensitive deploy-info filename/path pattern. Keep the guard pattern literal/structural enough to catch the known historical reference without printing or embedding secret contents; the sensitive file itself must remain unread.

### Risks
- Archive artifacts are normally immutable audit history; this requires an explicit documented security exception.
- New artifacts must avoid reintroducing the exact sensitive path while describing the cleanup.
- A too-broad guard may flag harmless generic wording or make future deployment documentation hard to write.
- Git history before this change may still contain the old reference; this cleanup addresses current tracked files, not full history rewriting.

### Ready for Proposal
Yes — propose a narrow security sanitation change that rewrites only tracked OpenSpec/archive references to the sensitive deploy-note filename/path and adds a pytest guard over archived markdown. Tell the user archive artifacts may be rewritten only for this security-redaction exception, with no secret-file reads and no secret/path disclosure.
