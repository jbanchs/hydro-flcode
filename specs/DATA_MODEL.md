# Data Model

## regulations

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| category | TEXT | Requirement category |
| topic | TEXT | Parameter/topic |
| regulation | TEXT | 40 CFR Part 141, FAC 62-550, etc. |
| section | TEXT | Section number |
| description | TEXT | Plain description |
| frequency_summary | TEXT | Human readable frequency |
| frequency_type | TEXT | monthly, annual, triggered, conditional, population_based, waiver_based |
| jurisdiction | TEXT | Federal, Florida, Palm Beach County |
| citation | TEXT | Exact cite |
| keywords | TEXT | Search keywords |

## frequency_rules

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| regulation_id | INTEGER | FK to regulations |
| parameter | TEXT | nitrate, total coliform, CCR, etc. |
| system_type | TEXT | CWS, NTNCWS, TNCWS, ANY |
| source_type | TEXT | groundwater, surface water, ANY |
| population_min | INTEGER | optional |
| population_max | INTEGER | optional |
| result_condition | TEXT | positive, exceedance, routine, ANY |
| waiver_status | TEXT | active, none, ANY |
| frequency | TEXT | monthly, annual, quarterly, triggered |
| action | TEXT | Required action |
| missing_required_fields | TEXT | comma-separated required fields |
| citation | TEXT | Exact citation |
