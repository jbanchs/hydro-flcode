# Design: Sanitize Deploy Info References

## Technical Approach

Make a documentation-and-test-only security sanitation change. The implementation will replace confirmed tracked archive wording that identifies a sensitive ignored local deployment note with generic wording, without opening or relying on the ignored local note. A focused pytest guard will scan committed OpenSpec archive markdown and fail on the prohibited sensitive-reference shape while allowing generic secret-handling language. This maps to `deployment-readiness` by strengthening tracked documentation guardrails without changing runtime behavior.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Redaction scope | Edit only confirmed tracked archive disclosure and preserve audit meaning. | Rewrite the whole archived exploration or delete archive content. | Archive artifacts are normally immutable audit records; a narrow security redaction is the least destructive exception. |
| Search strategy | Search committed text for the known sensitive-reference shape using generic regex terms; do not read ignored local files. | Open the ignored note to compare content, or broad-scan outside tracked docs. | The risk is tracked filename/path disclosure, not note content. Avoiding sensitive file access prevents expanding exposure. |
| Test guard | Extend `tests/test_deployment_docs.py` with an OpenSpec archive markdown scanner. | Add a separate test file or block all “secret” wording. | Existing deployment docs tests already centralize secret/private deployment guardrails; a targeted guard avoids false positives. |
| Git history | Clean current tracked files only; do not rewrite history. | Rewrite or purge prior commits. | History rewrite is disruptive, coordination-heavy, and explicitly out of scope for this change. |

## Data Flow

    tracked OpenSpec archive markdown
        └── pytest archive scanner
              ├── prohibited sensitive-reference pattern => fail
              └── generic secret wording only => pass

Implementation data flow is static text validation only. No server, deployment, CI/CD, database, router, service, or runtime path participates.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `openspec/changes/archive/2026-06-15-prepare-deployment/exploration.md` | Modify | Replace sensitive local note filename/path wording with generic language while preserving the finding and audit rationale. |
| `tests/test_deployment_docs.py` | Modify | Add helper(s) to read committed OpenSpec archive markdown and a pytest case rejecting the prohibited sensitive-reference pattern. |
| `openspec/changes/sanitize-deploy-info-references/design.md` | Create | Record this technical design. |

## Interfaces / Contracts

No product API or runtime contract changes.

Test contract:

```python
ARCHIVED_OPENSPEC_MARKDOWN = PROJECT_ROOT / "openspec" / "changes" / "archive"

def archived_openspec_markdown_paths() -> list[Path]:
    return sorted(ARCHIVED_OPENSPEC_MARKDOWN.rglob("*.md"))
```

The new assertion MUST report the relative tracked file path if the prohibited pattern appears, but the generated artifact and assertion label should use generic wording only.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Archive markdown scanner rejects prohibited sensitive-reference shape. | Add pytest coverage in `tests/test_deployment_docs.py` using the existing `PROJECT_ROOT` and `Path` patterns. |
| Integration | Full deployment documentation guard suite remains green. | Run `python -m pytest tests/test_deployment_docs.py`, then `python -m pytest`. |
| E2E | Not applicable. | No browser/runtime behavior changes. |

## Migration / Rollout

No migration required. This is a tracked documentation redaction plus test guard. Rollout is normal review/merge. Do not rewrite Git history; if historical exposure must be remediated later, handle it as a separate coordinated security procedure.

## Open Questions

None.
