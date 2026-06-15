## Exploration: local-openspec-validation

### Current State
HYDRO stores SDD/OpenSpec artifacts repo-locally under `openspec/`. `openspec/config.yaml` declares project `HYDRO`, persistence `openspec`, strict TDD, local test command `py -m pytest`, and CI command `python -m pytest`. The repository has main specs for `browser-security-policy` and `deployment-readiness`, plus archived changes that repeatedly record `openspec validate <change> --strict` as unavailable because `openspec` is not on PATH. Later archives also record `gentle-ai sdd-status` as the available native SDD status/archival dispatcher.

Local command probing confirmed `gentle-ai.exe` is available, while `openspec` is not discoverable. Runtime dependencies are Python-only in `requirements.txt`; there is no package file or declared OpenSpec CLI dependency. Existing tests already guard CI shape, deployment docs, local browser smoke, and archived sensitive-reference redaction, but they do not verify the OpenSpec artifact structure or validation-tooling documentation.

### Affected Areas
- `openspec/config.yaml` — current source for project SDD settings, local/CI test commands, and phase rules; may need explicit validation-tooling guidance.
- `openspec/specs/deployment-readiness/spec.md` — best existing domain for local validation boundaries, no-secrets rules, and documentation-only operational readiness.
- `README.md` — current public developer entry point for local run/test guidance; could document OpenSpec validation commands and the missing CLI fallback.
- `tests/test_deployment_docs.py` — existing docs/static guard pattern suitable for asserting validation guidance without touching runtime behavior.
- `requirements.txt` — Python dependency list does not include OpenSpec CLI tooling; adding a CLI here is only appropriate if the CLI is Python-distributed and intentionally project-pinned.
- `openspec/changes/archive/*/verify-report.md` and `apply-progress.md` — historical evidence of missing OpenSpec CLI and evolving reliance on `gentle-ai sdd-status`.

### Approaches
1. **Install/use OpenSpec CLI directly** — Pin or document the official CLI and require `openspec validate <change> --strict` locally.
   - Pros: restores strict validation semantics; matches existing archived command wording.
   - Cons: no CLI dependency is currently declared; package/source is not evident in repo; may add toolchain ambiguity or global-install assumptions.
   - Effort: Medium

2. **Rely on `gentle-ai sdd-status` as explicit local gate** — Document that `gentle-ai sdd-status <change>` is the available native repo-local dispatcher when `openspec` CLI is absent.
   - Pros: matches verified environment and recent archive precedent; no new dependencies or secrets; keeps validation truthful.
   - Cons: does not provide strict OpenSpec schema validation; must avoid claiming it is equivalent to `openspec validate --strict`.
   - Effort: Low

3. **Add a script wrapper** — Provide a local command that tries `openspec validate <change> --strict` when available, otherwise runs `gentle-ai sdd-status <change>` and reports the limitation.
   - Pros: one actionable command for maintainers; makes fallback behavior consistent.
   - Cons: needs careful naming/output so fallback is not misrepresented as strict validation; adds maintenance surface.
   - Effort: Medium

4. **Add docs only** — Update README/OpenSpec guidance to explain command availability, expected local commands, and what to do when the CLI is missing.
   - Pros: smallest safe slice; no runtime, dependency, deployment, or secret impact.
   - Cons: easy to drift; no automated guard ensures future docs keep the boundary explicit.
   - Effort: Low

5. **Add pytest artifact-structure tests** — Add tests that assert required OpenSpec config/spec/change archive artifacts exist and validation guidance remains explicit.
   - Pros: uses existing `py -m pytest` local runner; protects actionable documentation and artifact presence without needing the missing CLI.
   - Cons: still not a substitute for strict OpenSpec CLI validation; tests must avoid overfitting archived artifact content.
   - Effort: Low/Medium

### Recommendation
Proceed with a narrow documentation-plus-guard slice: explicitly document the local validation ladder (`openspec validate <change> --strict` when CLI is installed; otherwise `gentle-ai sdd-status <change>` as the available native status/archive-readiness signal), and add lightweight pytest coverage that the repo-local OpenSpec structure and validation guidance exist. Do not add production deployment changes, real env files, secrets, GitHub Actions changes, or browser/deployment automation. Defer CLI installation/pinning until the exact official OpenSpec CLI distribution is chosen; if later chosen, make it a separate work unit.

### Risks
- `gentle-ai sdd-status` can report artifact completeness and archive readiness, but it must not be described as strict OpenSpec schema validation.
- Adding a wrapper without clear wording could hide the missing CLI and create false confidence.
- Installing a CLI globally or through an unverified package path could make local validation less reproducible, not more.
- Tests that scan archived artifacts too broadly may become brittle because archives are an audit trail.

### Ready for Proposal
Yes — propose a focused `local-openspec-validation` change that documents the validation-tooling story and adds local pytest guards for required OpenSpec artifacts/guidance, while explicitly preserving the no-secrets, no-production-deployment, and no-CI-billing-fix boundaries.
