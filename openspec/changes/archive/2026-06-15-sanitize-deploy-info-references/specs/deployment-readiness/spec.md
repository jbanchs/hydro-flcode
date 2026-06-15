# Delta for Deployment Readiness

## ADDED Requirements

### Requirement: Tracked Artifact Sensitive Reference Guard

Tracked deployment-readiness artifacts MUST NOT include the sensitive local deployment-note filename or path pattern. Generic wording MAY describe an ignored local deployment secret note without naming or locating it.

#### Scenario: Tracked artifacts use generic wording

- GIVEN tracked deployment-readiness documentation or OpenSpec artifacts are reviewed
- WHEN they refer to the local deployment secret note
- THEN the reference MUST use generic wording only
- AND it MUST NOT disclose the sensitive filename or path pattern.

#### Scenario: Prohibited reference is rejected

- GIVEN a tracked artifact includes the sensitive local note filename or path pattern
- WHEN deployment-readiness checks run
- THEN the change MUST be considered non-compliant until the reference is removed or generalized.

### Requirement: Archive Redaction Exception

Archived OpenSpec artifacts SHOULD remain immutable, except a narrow security-redaction change MAY replace sensitive local deployment-note references with generic wording while preserving audit meaning.

#### Scenario: Security redaction preserves audit meaning

- GIVEN an archived OpenSpec artifact exposes the sensitive local note reference pattern
- WHEN a security-redaction exception is applied
- THEN only the sensitive reference MUST be generalized
- AND the surrounding audit meaning MUST remain intact.

#### Scenario: Unrelated archive rewrite is rejected

- GIVEN an archive edit changes scope, decisions, or unrelated deployment text
- WHEN it is reviewed as part of this redaction exception
- THEN the change MUST be rejected as outside the allowed exception.

### Requirement: Guard Coverage for Archived Markdown

The test suite MUST guard tracked archived OpenSpec markdown against reintroducing the sensitive local deployment-note filename or path pattern.

#### Scenario: Archive guard detects reintroduction

- GIVEN archived OpenSpec markdown contains the prohibited sensitive reference pattern
- WHEN `python -m pytest` runs
- THEN the relevant test MUST fail.

#### Scenario: Generic secret language remains allowed

- GIVEN archived OpenSpec markdown uses generic wording for ignored local deployment secret notes
- WHEN `python -m pytest` runs
- THEN the guard MUST allow the artifact.

### Requirement: No History Rewrite or Sensitive File Access

This change MUST NOT rewrite Git history and MUST NOT read, open, copy, summarize, or otherwise access the ignored local deployment secret note.

#### Scenario: Current tracked files are sanitized only

- GIVEN the sensitive reference exists in current tracked artifacts
- WHEN the sanitation change is applied
- THEN only current tracked content and tests MUST be changed
- AND Git history MUST NOT be rewritten.

#### Scenario: Ignored local note remains untouched

- GIVEN the ignored local deployment secret note exists outside tracked artifacts
- WHEN the sanitation work is performed
- THEN the note MUST NOT be read, copied, summarized, or named in artifacts.
