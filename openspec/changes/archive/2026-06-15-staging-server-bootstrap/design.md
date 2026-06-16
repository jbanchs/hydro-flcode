# Design: Staging Server Bootstrap

## Technical Approach

Add a documentation-only bootstrap checklist to the existing deployment-readiness materials and extend static pytest guards. The design preserves the current boundary pattern: repo-local docs, placeholder wording, no scripts, no server access, no deploy automation, and verification through `py -m pytest` only.

## Architecture Decisions

| Option | Tradeoff | Decision |
|--------|----------|----------|
| Add checklist to `docs/deployment.md` | Keeps operator guidance near existing staging handoff; document grows longer | Chosen: add a compact "Manual staging server bootstrap prerequisites" section with audit facts, package prerequisites, and verification checklist. |
| Create executable install helper | Faster operator execution, but violates no-automation/no-server boundary | Rejected: apt/systemctl guidance remains manual operator-run wording only. |
| Install/configure Caddy now | Closer to ingress readiness, but implies public exposure/TLS scope | Rejected: document Caddy as deferred; if later approved, package-only and unconfigured, with no Caddyfile/systemd/firewall work in this slice. |
| Add static pytest concepts to existing `tests/test_deployment_docs.py` | Simple and matches current guard style; regex exceptions must avoid false positives | Chosen: extend constants/tests rather than adding a new test module. |

## Data Flow

    Proposal/spec intent
        └─→ docs/deployment.md checklist
              ├─→ deploy/README.md index pointer
              ├─→ OpenSpec delta requirement
              └─→ tests/test_deployment_docs.py static guards
                         └─→ py -m pytest

No runtime app, database, CI, SSH, SCP, apt execution, or server state participates in this flow.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `docs/deployment.md` | Modify | Add manual bootstrap prerequisite checklist for Ubuntu 22.04, apt, systemctl, passworded sudo, Python 3.10 audit fact, missing `git`/Caddy/`sqlite3`, 20G disk, 2GiB RAM, minimal package prerequisites, and verification. |
| `deploy/README.md` | Modify | Link/index the bootstrap checklist and state it remains docs-only and operator-run. |
| `tests/test_deployment_docs.py` | Modify | Add static guards for required audit facts, package checklist wording, apt/manual boundary, Caddy deferral, Python 3.10 compatibility caution, sudo password handling, and prohibited automation. |
| `openspec/changes/staging-server-bootstrap/specs/deployment-readiness/spec.md` | Create | Delta requirement for manual staging server bootstrap checklist and static guard coverage. |
| `openspec/changes/staging-server-bootstrap/design.md` | Create | This design artifact. |

## Interfaces / Contracts

Documentation contract:
- apt examples MUST be framed as "manual operator-run on the server" or equivalent, not scripts, not remote commands, and not automation.
- Use placeholders for operator-specific values and avoid real hostnames, IPs, paths, credentials, or private note references.
- Minimal package prerequisites are `git`, `python3-venv`, and `sqlite3` only.
- Caddy MUST be documented as deferred; later approval may be package-only and unconfigured, not Caddy/systemd/firewall/TLS configuration.
- Python 3.10 MUST be described as an audited server fact, not proof of HYDRO runtime compatibility with the repo's Python 3.13 context.
- Passworded sudo MUST say the operator enters the password interactively and never records it in Git, docs, logs, or prompts.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit/static | Docs contain required bootstrap facts and checklist concepts | Extend `tests/test_deployment_docs.py` phrase/regex guards. |
| Boundary/static | No SSH/SCP/server probes/scripts/CI/deploy automation/secrets/env/db reads | Reuse and extend existing forbidden automation patterns, with explicit allowed manual boundary wording where needed. |
| Integration/E2E | Not applicable | No runtime behavior, server access, or browser automation in scope. |

Verification command: run `py -m pytest` from the repository root.

## Migration / Rollout

No migration required. This is a repo-local docs/spec/test guard change. Rollback is reverting the docs, static tests, and OpenSpec change folder.

## Open Questions

None.
