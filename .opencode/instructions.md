# OpenCode Instructions — HYDRO

You are working on HYDRO, a Spec Driven Design and Test Driven Development project.

## Non-negotiable behavior

- Do not invent regulatory answers.
- Every regulatory answer must include exact citation.
- If no citation exists in the local database or approved source, respond with insufficient regulatory basis.
- Keep the UI minimal, white-first, professional, and table-centered.
- HYDRO is an engineer, not a superhero.

## Development workflow

1. Read `specs/SDD.md` before coding.
2. Read `specs/TDD.md` before writing or changing logic.
3. Add or update tests first.
4. Implement the smallest code change that passes the test.
5. Keep services separated:
   - regulation_service.py for data access
   - frequency_engine.py for rule decisions
   - hydro_agent.py for response composition

## UI rules

- 80% white / light neutral background.
- Tables are the primary information architecture.
- Hydro chat is a side panel, not the main app.
- Use Tailwind utility classes first.
- Use custom CSS only for brand polish.
- Use GSAP only for subtle entrance and hover animations.
