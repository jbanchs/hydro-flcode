# SDD — HYDRO

## Product Vision

HYDRO is a water regulatory intelligence platform that organizes drinking water regulations into searchable tables and provides a citation-first regulatory engineer assistant.

The first regulatory guides are:

- 40 CFR Part 141
- FAC 62-550

The system may later include county-level requirements such as Palm Beach County procedures when official sources are loaded.

## Design Principles

1. Structured first, agent second.
2. Every requirement must be traceable to a citation.
3. The app must identify missing information before giving a case-specific frequency.
4. HYDRO must never improvise.
5. The UI must be minimal and professional.

## User Roles

### Compliance Officer
Needs fast lookup of requirements, due dates, and citations.

### Laboratory Professional
Needs sample frequency, reporting, methods, and monitoring triggers.

### Utility Operator
Needs action-oriented interpretation for monitoring, repeat samples, and reporting.

### Inspector / Reviewer
Needs citations and regulatory basis.

## Core Features

### Regulation Table
Users can search and filter regulatory requirements.

Fields:

- Category
- Topic
- Regulation
- Section
- Requirement / Description
- Frequency Summary
- Frequency Type
- Jurisdiction
- Citation

### Frequency Engine
HYDRO determines frequency based on case input.

Inputs:

- jurisdiction
- system_type
- source_type
- population_served
- parameter
- sample_type
- result
- previous_results
- waiver_status
- compliance_history

Outputs:

- required frequency
- triggered action
- missing information
- citation
- confidence

### HYDRO Agent
HYDRO composes a response using retrieved regulation data and frequency engine output.

Required answer format:

```text
Answer:

Case Factors Used:

Required Frequency / Action:

Regulatory Basis:

HYDRO Interpretation:

Missing Information:

Confidence:
```

## Initial Pages

- `/` Dashboard / Regulations table
- `/api/regulations` JSON search/filter endpoint
- `/api/ask` case-based HYDRO endpoint

## Style

- 80% white
- navy text
- soft blue accent
- light gray borders
- large searchable tables
- clean right-side HYDRO consult panel
