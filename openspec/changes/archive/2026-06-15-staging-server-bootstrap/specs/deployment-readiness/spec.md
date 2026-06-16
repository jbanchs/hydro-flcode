# Delta for Deployment Readiness

## ADDED Requirements

### Requirement: Manual Staging Server Bootstrap Checklist

Deployment documentation MUST record the audited staging host facts and provide a manual prerequisite checklist only. The checklist MUST include Ubuntu 22.04, `apt`, `systemctl`, passworded `sudo`, Python 3.10, missing `git`, missing Caddy, missing `sqlite3`, 20G disk, and 2GiB RAM. It MUST require operator-installed prerequisites for `git`, `python3-venv`, and `sqlite3`, recommend key-based SSH for later approved access, and warn that Python 3.10 is an audit fact, not compatibility approval for HYDRO's Python 3.13 baseline.

#### Scenario: Operator reviews audit facts

- GIVEN an operator opens the staging bootstrap checklist
- WHEN they inspect target facts and prerequisites
- THEN all audited facts and required manual packages MUST be present
- AND Python 3.10 MUST be labeled as a compatibility caution, not approval.

#### Scenario: Missing prerequisite is visible

- GIVEN `git`, `python3-venv`, or `sqlite3` is absent on the staging host
- WHEN the operator follows the checklist
- THEN the documentation MUST identify the missing package as a manual prerequisite
- AND it MUST NOT install or automate the package from the repository.

### Requirement: Manual Bootstrap Verification Commands

Deployment documentation MUST provide operator-run verification commands for Python, virtual environment support, `git`, `sqlite3`, `systemctl`, `apt`, `sudo`, disk, and memory. Commands MUST be documentation-only, local to the operator's approved shell session, and MUST NOT be wrapped in scripts, CI, deployment automation, SSH/SCP examples, or server probes from this repository.

#### Scenario: Operator verifies prerequisites manually

- GIVEN an operator has authorized shell access outside this repository slice
- WHEN they run the documented verification commands manually
- THEN they can confirm Python, venv, git, sqlite3, systemd, apt, sudo, disk, and memory readiness.

#### Scenario: Verification remains non-automated

- GIVEN a change proposes scripts, CI jobs, SSH commands, SCP, or repository-driven server probes
- WHEN deployment-readiness review runs
- THEN the change MUST be rejected as outside the bootstrap checklist scope.

### Requirement: Bootstrap Security and Scope Boundary

The bootstrap checklist MUST state that passworded `sudo` requires interactive operator entry and MUST NOT record, request, echo, store, or commit passwords. This slice MUST NOT access servers, deploy HYDRO, change Caddy configuration, change systemd configuration, alter secrets, read real env files, read real databases, modify CI, or add deployment scripts.

#### Scenario: Passworded sudo boundary is clear

- GIVEN the checklist references sudo usage
- WHEN an operator reads the guidance
- THEN it MUST state that sudo is passworded and entered interactively
- AND no password value or capture instruction MUST appear.

#### Scenario: Scope creep is rejected

- GIVEN docs or tests add server access, deployment, scripts, Caddy/systemd config, secrets, env/db reads, or CI changes
- WHEN deployment-readiness review runs
- THEN the change MUST be considered non-compliant until removed.

### Requirement: Pytest Guards for Bootstrap Boundaries

The test suite MUST include local pytest static guards requiring the audited facts, manual prerequisite checklist, verification command coverage, sudo boundary, SSH key recommendation, and Python 3.10 caution. Guards MUST fail on server access, deployment scripts, Caddy/systemd configuration, secrets, real env/db reads, or CI changes.

#### Scenario: Required bootstrap wording is guarded

- GIVEN deployment documentation changes
- WHEN `py -m pytest` runs locally
- THEN guards MUST fail if audit facts, prerequisites, verification commands, sudo boundary, SSH key recommendation, or Python caution are missing.

#### Scenario: Prohibited bootstrap scope is guarded

- GIVEN tracked artifacts introduce prohibited server, deployment, secret, env, db, Caddy, systemd, script, or CI scope
- WHEN `py -m pytest` runs locally
- THEN the relevant static guard MUST fail.
