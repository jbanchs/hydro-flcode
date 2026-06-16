## Exploration: staging-server-bootstrap

### Current State
HYDRO already has deployment/staging readiness documentation and placeholder-only runtime examples for env, systemd, and Caddy. Current OpenSpec requirements strongly reject server access, deploy automation, SSH/SCP commands, real host/IP values, real env/secret reads, and `hydro.db` access for deployment-readiness slices. The user-provided read-only server audit says the Ubuntu 22.04 staging host has Python 3.10, systemd, apt, sudo-with-password, limited disk/memory, and is missing git, Caddy, and sqlite3 CLI. This exploration did not contact the server, read ignored sensitive notes, real env files, or `hydro.db`.

### Affected Areas
- `docs/deployment.md` — existing staging and deployment readiness checklist is the safest place to add a manual server bootstrap checklist with explicit non-deploy boundaries.
- `deploy/README.md` — runtime artifact index can point operators to the bootstrap checklist without adding executable automation.
- `deploy/systemd/hydro.service.example` — already assumes systemd, non-root `hydro` user, `/etc/hydro/hydro.env`, and uvicorn; bootstrap docs should verify prerequisites that make this template adaptable later.
- `deploy/caddy/Caddyfile.example` — already provides placeholder reverse proxy/TLS shape; bootstrap docs should decide whether Caddy is installed now or deferred.
- `tests/test_deployment_docs.py` — current guards reject SSH/SCP, server probes, real hosts/IPs, deploy automation, and sensitive note references; any new checklist likely needs focused static guards or carefully scoped exceptions for generic package verification wording.
- `openspec/specs/deployment-readiness/spec.md` — existing requirements are readiness-only and no-server/no-automation; this change likely needs a delta requirement for operator-run prerequisite bootstrap planning.

### Approaches
1. **Docs/checklist only** — Add a placeholder-only checklist describing required packages, verification commands, sudo expectation, SSH key requirement, and stop-before-deploy boundary.
   - Pros: smallest safe slice; matches existing docs-first pattern; no server access or automation; easy rollback; likely under the 400-line review budget.
   - Cons: does not install anything; operator must execute and adapt commands manually; may need test guard updates to allow generic apt/package wording without real targets.
   - Effort: Low

2. **Apt command runbook for git/python3-venv/sqlite3/caddy** — Document operator-run apt update/install commands and verification commands for all missing prerequisites.
   - Pros: actionable; covers current audit gaps; makes later deployment less ambiguous.
   - Cons: Caddy setup can imply public ingress/TLS before deployment; sudo-with-password handling must avoid recording credentials; exact commands must remain generic and operator-run, not automation.
   - Effort: Medium

3. **Delay Caddy and use local uvicorn first** — Document only minimal app-host prerequisites (`git`, `python3-venv`, `sqlite3`) and verify Python/systemd, leaving Caddy/TLS/firewall for the deployment slice.
   - Pros: smallest operational risk; avoids opening ingress or TLS ownership too early; aligns with “server bootstrap only, not deployment.”
   - Cons: staging cannot be validated through the final reverse-proxy path yet; a later slice must handle Caddy install/configuration.
   - Effort: Low

4. **System package verification commands only** — Document read-only commands like `command -v`, version checks, and `systemctl --version`; do not document package installation yet.
   - Pros: very safe; no sudo package mutation; works as a preflight checklist.
   - Cons: does not resolve missing git/Caddy/sqlite3 CLI; insufficient if the next step expects prerequisites installed.
   - Effort: Low

### Recommendation
Use a docs/checklist-only bootstrap plan that includes generic operator-run apt installation for the minimal prerequisites `git`, `python3-venv`, and `sqlite3`, plus verification commands for Python, venv, git, sqlite3, systemd, disk, memory, and sudo readiness. Defer Caddy installation/configuration to the actual deployment/reverse-proxy slice unless the proposal explicitly frames it as “package installed only, not configured, not exposed.” Require key-based SSH readiness as a human/operator prerequisite, but do not include real SSH targets, keys, passwords, host IPs, hostnames, or remote commands in tracked artifacts. Keep the checklist explicitly stopped before cloning private code, creating real env files, initializing databases, starting HYDRO, opening firewall ports, or configuring Caddy.

### Risks
- Existing static tests reject SSH/SCP, IPs, URLs, server probes, and deploy automation; implementation must phrase key-based SSH and verification guidance generically without real remote commands or targets.
- Apt install wording can be mistaken for deploy automation if not labeled as manual operator-run server bootstrap.
- Installing/configuring Caddy too early could imply public ingress/TLS readiness before HYDRO deployment is authorized.
- Sudo requires a password on the target host; docs must state credentials are operator-entered interactively and must never be recorded in Git, logs, prompts, or artifacts.
- The local app targets Python 3.13 in config, while the audited server has Python 3.10; verify dependency compatibility before assuming the server runtime is acceptable.

### Ready for Proposal
Yes — propose a narrow documentation/spec/test slice for manual staging server bootstrap planning. Tell the orchestrator this should not access the real server, not deploy HYDRO, not create automation, not configure Caddy/TLS/firewall, not read secrets/env/database files, and should keep the review slice under 400 changed lines.
