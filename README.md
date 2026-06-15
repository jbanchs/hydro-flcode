# HYDRO — Water Regulatory Intelligence Platform

HYDRO is a minimal white-first regulatory webapp for water compliance. It transforms drinking water regulations into searchable, structured, and citation-driven compliance knowledge powered by 40 CFR Part 141, FAC 62-550, and jurisdiction-specific requirements.

It uses structured regulation tables plus a citation-first agent that answers only from verified regulatory sources.

## Stack

- FastAPI
- Jinja2
- SQLite
- HTML / CSS / JavaScript
- App-owned static CSS served from `/static/css/styles.css`
- Pytest for TDD

## Core Concept

HYDRO is not a free-form chatbot. HYDRO is a retrieval-first regulatory engineer.

1. Search regulation database.
2. Identify applicable jurisdiction.
3. Determine frequency using the Frequency Engine.
4. Respond with citation.
5. If citation is missing, say that the answer cannot be confirmed.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
HYDRO_SESSION_SECRET="replace-with-a-long-random-secret"
HYDRO_BOOTSTRAP_ADMIN_PASSWORD="replace-with-a-local-admin-password"
python scripts/init_db.py
uvicorn app.main:app --reload
```

On Windows PowerShell, set the environment variables before running HYDRO:

```powershell
$env:HYDRO_SESSION_SECRET = "replace-with-a-long-random-secret"
$env:HYDRO_BOOTSTRAP_ADMIN_PASSWORD = "replace-with-a-local-admin-password"
python scripts/init_db.py
uvicorn app.main:app --reload
```

The bootstrap user defaults to username `admin`. Passwords are stored as Argon2 hashes, never plaintext. `HYDRO_SESSION_SECRET` is required; `HYDRO_ALLOW_DEV_SECRET=1` enables a clearly marked local-only fallback for development only. Session cookies are HTTP-only, SameSite=Lax, and can be marked Secure with `HYDRO_SESSION_COOKIE_SECURE=1` behind HTTPS.

Open:

```text
http://127.0.0.1:8000
```

## Run tests

```bash
py -m pytest
```

## Local OpenSpec validation

For active SDD/OpenSpec changes, use the strict OpenSpec CLI only when a verified OpenSpec CLI is already installed locally:

```bash
openspec validate local-openspec-validation --strict
```

If that CLI is not available, use HYDRO's native SDD status command as a local status/archive-readiness signal:

```bash
gentle-ai sdd-status local-openspec-validation
```

`gentle-ai sdd-status` is not strict OpenSpec CLI schema validation. It is a fallback status/readiness check, not a replacement for `openspec validate <change> --strict`.

Keep local verification on Windows aligned with the repo test runner:

```bash
py -m pytest
```

## Local browser smoke checklist

Use this checklist for local confidence while GitHub Actions is blocked by billing. It is not deploy automation, not a CI fix, and does not require Playwright, Selenium, Cypress, screenshots, remote services, or real secrets.

1. Start HYDRO locally with safe placeholder development values, then run `py -m pytest`.
2. Open `http://127.0.0.1:8000/healthz` and confirm it returns the liveness JSON only; do not treat it as database, auth, dependency, or readiness validation.
3. Open `http://127.0.0.1:8000/login` and confirm the page is readable, styled by `/static/css/styles.css`, and operable.
4. Sign in with the local test/development admin account and confirm authenticated `/` renders the regulation search workflow and Ask HYDRO panel.
5. Search from the regulation table and confirm results refresh without a full page failure, with readable rows, badges, and empty-result feedback.
6. Ask HYDRO a question that has source-backed information and confirm the answer is readable and citation-first.
7. Ask a question with missing or unsupported information and confirm HYDRO clearly states that the answer cannot be confirmed from available sources.
8. In browser developer tools, confirm CSS and JavaScript load from same-origin `/static/...` paths and that no CDN script/style request is required.

## Deployment Readiness

Deployment preparation is documented in [`docs/deployment.md`](docs/deployment.md), with placeholder-only environment examples in [`.env.example`](.env.example) and the runtime artifact index at [`deploy/README.md`](deploy/README.md). Runtime examples include `deploy/systemd/hydro.service.example`, `deploy/env/hydro.env.example`, and `deploy/caddy/Caddyfile.example`. This readiness slice does not add deployment automation, server provisioning, CI/CD deploy jobs, or executable infrastructure.

Real secrets must stay outside Git and must be supplied through the target environment or secret manager. Rotate any exposed credentials before production use.

## Browser Security Headers

HYDRO sets browser security headers on rendered pages and API responses through FastAPI middleware:

- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()`

The current CSP allows only same-origin templates and static frontend assets for scripts and styles. Tailwind CDN has been removed; HYDRO now uses app-owned static CSS from `/static/css/styles.css` for the login page, authenticated app shell, regulation table, and Ask HYDRO dynamic states. CDNJS/GSAP is not required by the frontend or allowed by `script-src`.

Manual visual smoke checks are required after CSS changes because this project has no browser E2E tooling. Use the local browser smoke checklist above to validate that `/healthz` stays liveness-only, `/login` remains readable and operable, authenticated `/` remains readable, search refresh preserves distinguishable regulation rows and badges, Ask HYDRO answer and missing-information states are legible, and CSS/JS load from local `/static` assets without CDN dependencies.

Rollback is limited to reverting the frontend asset removal and `app/core/security_headers.py`; this restores the previous response header and cosmetic animation behavior without changing auth, CSRF, API, database, or frequency logic.

## Project Structure

```text
hydro_sdd_tdd/
├── app/
│   ├── main.py
│   ├── core/config.py
│   ├── db/database.py
│   ├── routers/
│   │   ├── api.py
│   │   └── web.py
│   ├── services/
│   │   ├── frequency_engine.py
│   │   ├── hydro_agent.py
│   │   └── regulation_service.py
│   ├── templates/
│   └── static/
├── specs/
│   ├── SDD.md
│   ├── TDD.md
│   ├── AGENT_SPEC.md
│   ├── DATA_MODEL.md
│   └── FREQUENCY_ENGINE_SPEC.md
├── tests/
├── scripts/init_db.py
└── .opencode/instructions.md
```

## First Build Goal

Build HYDRO around three workflows:

1. Search regulations in a table.
2. Filter by jurisdiction, regulation, category, and frequency type.
3. Ask HYDRO a case-based question and receive a cited answer.
