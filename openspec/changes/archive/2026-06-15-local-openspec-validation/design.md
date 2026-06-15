# Design: Local OpenSpec Validation

## Technical Approach

Add a documentation-plus-static-guard slice that clarifies HYDRO's local OpenSpec validation ladder without introducing tooling. The design updates README/OpenSpec guidance and the deployment-readiness spec, then extends the existing `tests/test_deployment_docs.py` pytest guard to enforce wording boundaries and repo-local OpenSpec structure/config expectations. No app runtime, production, deployment, CI billing, dependency, or secret-bearing files are changed.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Validation boundary | Document `openspec validate <change> --strict` only when an OpenSpec CLI is installed; document `gentle-ai sdd-status <change>` as native non-strict status/archive-readiness fallback. | Treat `gentle-ai sdd-status` as strict validation; install/pin a CLI. | The proposal explicitly rejects false equivalence and new CLI dependency. |
| Guard location | Extend `tests/test_deployment_docs.py`. | Create a new test module. | Existing deployment-readiness guards already centralize docs/archive/config wording checks. |
| Config scope | Add explicit local validation expectations to `openspec/config.yaml` only as SDD metadata/rules. | Add executable config, production config, or CI workflow changes. | Keeps validation expectations discoverable while preserving no-deploy/no-runtime boundaries. |
| Review slicing | Keep as one small docs+test work unit. | Split docs, spec, and tests into separate PRs. | Expected diff is below 400 lines; tests stay with docs they validate. |

## Data Flow

Developer local validation path:

```text
README / OpenSpec guidance
        │
        ├─ if OpenSpec CLI exists ──→ openspec validate <change> --strict
        │
        └─ fallback ────────────────→ gentle-ai sdd-status <change>
                                      (native status/readiness, not strict schema validation)

py -m pytest ──→ tests/test_deployment_docs.py ──→ README/config/spec/archive wording guards
```

## File Changes

| File | Action | Description |
|---|---|---|
| `README.md` | Modify | Add local OpenSpec validation section with strict CLI vs `gentle-ai sdd-status` fallback language and `py -m pytest` verification. |
| `openspec/config.yaml` | Modify | Record validation-tooling expectations in local SDD rules/context without adding executable dependency. |
| `openspec/specs/deployment-readiness/spec.md` | Modify | Add requirement/scenarios for local OpenSpec validation guidance, fallback boundary, pytest guard, and no production/deploy/secrets scope. |
| `tests/test_deployment_docs.py` | Modify | Add static assertions for OpenSpec config/archive structure, README wording, forbidden strict-validation equivalence, and local pytest command. |
| `openspec/changes/local-openspec-validation/design.md` | Create | This design artifact. |

## Interfaces / Contracts

No production APIs or runtime interfaces change. The documentation contract is:

```text
Strict validation: openspec validate <change> --strict, only when an OpenSpec CLI is installed locally.
Fallback: gentle-ai sdd-status <change>, native SDD status/archive-readiness signal, not strict OpenSpec CLI/schema validation.
Verification: py -m pytest.
```

Forbidden wording must not claim or imply that `gentle-ai sdd-status` performs strict OpenSpec CLI validation.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit/static | README/config/spec wording and OpenSpec archive/config expectations | Add pytest checks in `tests/test_deployment_docs.py` using `Path.read_text()` and regex/string assertions. |
| Integration | Full local project guard suite | Run `py -m pytest`. |
| E2E | Not applicable | No browser/runtime behavior changes. |

## Migration / Rollout

No migration required. Rollout is local documentation/spec/test only. Revert the docs/spec/test changes to roll back.

## Open Questions

None.
