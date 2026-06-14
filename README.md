# HYDRO — Water Regulatory Intelligence Platform

HYDRO is a minimal white-first regulatory webapp for water compliance. It transforms drinking water regulations into searchable, structured, and citation-driven compliance knowledge powered by 40 CFR Part 141, FAC 62-550, and jurisdiction-specific requirements.

It uses structured regulation tables plus a citation-first agent that answers only from verified regulatory sources.

## Stack

- FastAPI
- Jinja2
- SQLite
- HTML / CSS / JavaScript
- Tailwind CSS via CDN for fast prototyping
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

## Browser Security Headers

HYDRO sets browser security headers on rendered pages and API responses through FastAPI middleware:

- `Content-Security-Policy`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()`

The current CSP allows same-origin templates and static assets plus Tailwind from `https://cdn.tailwindcss.com`. Tailwind CDN is the remaining interim prototyping tradeoff; CDNJS/GSAP has been removed from the app and from `script-src`. Production hardening should replace Tailwind CDN with a local build so third-party script sources and `style-src 'unsafe-inline'` can be removed.

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
