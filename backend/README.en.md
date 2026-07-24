# Smart Working Manager — Backend

*[Versione italiana](README.md)*

FastAPI API for tracking office/smart-working attendance.

## Local setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

API available at `http://localhost:8000` (interactive docs at `/docs`).
In development it uses local SQLite (`officepresence.db`), no external DB
required.

Company search in onboarding (`GET /company/search`, legacy Google Places
Text Search) requires a valid `GOOGLE_MAPS_API_KEY` in the local `.env`
(never commit it: `.env` is already in `.gitignore`, `.env.example` only has
a placeholder). Without a key the endpoint simply returns empty results, the
app otherwise remains usable.

## Tests

```bash
pytest
pytest --cov=app --cov-report=term-missing
```

Coverage target: **> 90%**, with particular attention to the calculation
logic in `app/services/calculation_service.py`.

## Structure

```
app/
    api/            FastAPI routers (HTTP endpoints)
    services/       business logic
    models/         SQLAlchemy models
    schemas/        Pydantic models (request/response)
    repositories/    database access
    utils/          helper functions (session code, date calculations)
tests/              pytest tests, mirroring app/'s structure
```

## Main endpoints

- `POST /session`, `GET /session`, `GET /session/{code}`, `DELETE /session` —
  creation, cookie bootstrap, recovery by code, deletion
- `GET /company/search` — company search (Google Places)
- `GET /company`, `PATCH /company` — read and update policy, working days
  and monitoring start date (settings section)
- `GET /dashboard`, `GET /calendar`, `POST /attendance`,
  `DELETE /attendance/{date}`, `POST /simulation`

The annual target calculation (`app/services/calculation_service.py`) takes
`Company.monitoring_start_date` into account: if set, required days/year are
counted from that date onward instead of January 1st (useful for someone who
starts monitoring mid-year); if the date is in the future relative to the
requested year, the target is zero.

Session recovery (`GET /session/{code}`) normalizes the submitted code
(`app/utils/code_generator.normalize_code`) before comparing it against the
DB: it tolerates upper/lowercase, whitespace, and the Unicode dash variants
that editor/spreadsheet autocorrect (Word, Notion, Google Sheets, iOS/macOS
"smart dashes") often substitutes for a plain `-` when copy-pasting.

## Deploy on cPanel hosting

Current setup: repo cloned **outside** `public_html`, backend served via
**Setup Python App** (Passenger) at `smartworkingmanager.com/api` — same
domain as the frontend (see `../deploy.sh`), so the session cookie stays
same-site instead of cross-site between two different domains. The frontend
is built and published as static files at the domain root by `../deploy.sh`.

Initial setup:

1. Clone the repo on the server, outside `public_html`.
2. On cPanel, **Setup Python App** section: create a new app with
   - Application root: the `backend/` folder of the cloned repo
   - Application URL: `smartworkingmanager.com/api` (Passenger routes
     requests under that path to the app, which still responds on its
     "root" routes, e.g. `/session`, `/dashboard` — no code changes needed)
   - Application startup file: `passenger_wsgi.py`
   - Application entry point: `application`
3. In the virtualenv created by cPanel (the panel shows the `source
   .../bin/activate` command): `pip install -r requirements.txt`.
4. Environment variables (**Environment variables** tab of the Python App):
   - `DATABASE_URL=mysql+pymysql://user:password@localhost/db_name`
   - `APP_ENV=production` (enables the `Secure` session cookie — requires
     SSL to be active on the domain, otherwise the browser discards the
     cookie)
   - `CORS_ORIGINS=https://smartworkingmanager.com`
   - `GOOGLE_MAPS_API_KEY=...` (for company search in onboarding)
5. **Restart** the Python app from cPanel.

**Domain migration note:** the backend previously ran on
`giemme76.com/worklifebalancegm/api`, with `CORS_ORIGINS` pointing there. If
that deployment stays online in parallel (legacy path, no longer updated),
the two Python apps remain independent: same code, separate `Setup Python
App` entries and environment variables for each.

On every update: push to GitHub locally → `git pull` on the cPanel terminal,
from the repo folder → if Python dependencies changed, `pip install -r
requirements.txt` in the virtualenv → **Restart** the app from cPanel.

**Warning:** recreating the app from "Setup Python App" overwrites
`passenger_wsgi.py` with a generic cPanel stub. If that happens, restore it
with `git checkout -- passenger_wsgi.py` (it must contain the ASGI→WSGI
adaptation via `a2wsgi`, not the stub).

**Warning:** `init_db()` only creates **missing** tables at startup, it does
not alter existing ones. Every time a column is added to a model (e.g.
`UserSession.nickname`, `Company.monitoring_start_date`), it must be applied
by hand on an already-populated production DB, otherwise the endpoint that
uses it returns 500:

```sql
ALTER TABLE table_name ADD COLUMN column_name TYPE NULL;
-- For the monitoring start date (company settings):
ALTER TABLE companies ADD COLUMN monitoring_start_date DATE NULL;
```

Alternatively, consider explicit migrations (e.g. Alembic) before
introducing further schema changes.
