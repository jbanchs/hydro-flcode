# TDD — HYDRO

## Test-First Rules

Every new regulatory behavior needs a test before implementation.

## Initial Test Cases

### Regulation Search
- Search `nitrate` returns 40 CFR 141.62 and FAC 62-550.310/320 seed records.
- Filter by jurisdiction `Federal` returns federal records only.
- Filter by regulation `FAC 62-550` returns Florida records only.

### Frequency Engine
- Monthly microbiological monitoring case returns monthly when the seed rule has base monthly frequency.
- Annual CCR case returns annual.
- Triggered RTCR case with positive total coliform returns triggered repeat/assessment action.
- Missing population for population-based rule returns missing information instead of guessing.

### HYDRO Agent
- Agent response includes citation when answer is found.
- Agent refuses to confirm if no citation is found.
- Agent lists missing information when frequency cannot be determined.
