# Design: Staging Deploy Readiness

## Technical Approach

Implement this as a documentation-and-static-guard slice only. Extend the existing deployment readiness runbook and runtime artifact index with staging validation guidance that remains repo-local, placeholder-only, and operator-executed after out-of-band deployment. Add pytest guards to `tests/test_deployment_docs.py` that assert required staging concepts and prohibited boundaries without matching long exact prose.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Staging mode | Document staging as production-like validation using `HYDRO_ENV=production` with staging-specific secret values supplied outside Git. | Add `HYDRO_ENV=staging` or app config changes. | Existing production-mode checks already define the safety model; a staging runtime mode would expand runtime behavior and violate scope. |
| Guard style | Add concept-level pytest assertions using small required term sets and forbidden regexes. | Assert complete paragraphs or snapshots. | Existing `test_deployment_docs.py` uses static guard patterns; concept checks reduce brittleness while still catching scope regressions. |
| Documentation location | Put detailed staging checklist in `docs/deployment.md`; link/order it from `deploy/README.md`; update `README.md` only if discoverability needs it. | Create new docs or deploy scripts. | Existing docs already centralize deployment readiness; adding files would increase review surface without new capability. |
| Delivery slice | One docs+tests work unit, suitable for a chained PR slice if needed. | Split docs and tests separately. | Tests verify the docs behavior and should stay with the documentation they guard. |

## Data Flow

```text
Maintainer updates docs/checklist
        │
        ├── docs/deployment.md: detailed staging preflight + post-deploy checklist
        ├── deploy/README.md: artifact order and pointer to staging checklist
        └── tests/test_deployment_docs.py: static guards
                         │
                         └── py -m pytest validates wording boundaries locally
```

No server, app, script, CI, database, or secret flow changes are introduced.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `docs/deployment.md` | Modify | Add staging preflight/dry-run section and manual post-deploy validation checklist covering login, `/healthz` liveness-only, authenticated home, search, Ask HYDRO, backup readiness, logs, rollback, and production-mode safety. |
| `deploy/README.md` | Modify | Link staging readiness into the manual validation order and preserve runtime artifact scope boundaries. |
| `tests/test_deployment_docs.py` | Modify | Add static guards for staging concepts, forbidden `HYDRO_ENV=staging`, no deploy automation/server access/real secret reads, and required checklist coverage. |
| `README.md` | Maybe modify | Only add/adjust a short pointer if the existing Deployment Readiness section does not sufficiently expose the staging checklist. |
| `openspec/changes/staging-deploy-readiness/specs/deployment-readiness/spec.md` | Future phase | Delta spec should add requirements for staging readiness docs and static guards. |

## Interfaces / Contracts

No runtime interfaces change. The test contract should remain static and concept-oriented:

```python
REQUIRED_STAGING_VALIDATION_CONCEPTS = [
    "staging", "HYDRO_ENV=production", "staging-specific secret values",
    "/healthz", "liveness-only", "/login", "authenticated /",
    "search", "Ask HYDRO", "backup", "rollback",
]
FORBIDDEN_STAGING_PATTERN = re.compile(
    r"HYDRO_ENV\s*=\s*staging|ssh\s+|scp\s+|deploy\.sh|hydro\.db",
    re.IGNORECASE,
)
```

Prefer asserting compact concept groups over exact sections. If checking prose, assert headings or short phrases only.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit/static | Staging docs include required checklist concepts and production-mode safety wording. | Extend `tests/test_deployment_docs.py` with required concept arrays over `docs/deployment.md` and `deploy/README.md`. |
| Boundary/static | No `HYDRO_ENV=staging`, deploy automation, server access, real env/secret reads, live `hydro.db`, scripts, app code, or CI changes are implied. | Add/extend regex guards; reuse existing `assert_no_forbidden_pattern` style. |
| Integration/E2E | None. | Out of scope; no real server access or browser automation. |

## Migration / Rollout

No migration required. Rollout is reverting docs, tests, and OpenSpec artifacts only.

## Open Questions

- None.
