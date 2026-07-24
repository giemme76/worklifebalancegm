# Smart Working Manager

*[Versione italiana](README.md)*

Login-free web app to track compliance with an office / smart-working
presence policy: 3-step onboarding, dashboard with an annual target and a
progress indicator, calendar, simulation of future scenarios.

Live: https://smartworkingmanager.com/ (previously at
https://giemme76.com/worklifebalancegm/, still online but no longer updated)

See [docs/OfficePresence.md](docs/OfficePresence.md) for the original concept
(some details are superseded by the actual implementation, which follows the
real design: percentage- or fixed-days-per-week policy, 6 presence types
including "Travel", green/orange/red progress indicator).

## Main features

- Registration-free onboarding: name/nickname, real company search (Google
  Places) with auto-detected headquarters, choice of policy, monitoring
  start date (defaults to today, useful when starting mid-year)
- Unique recovery code (`SW-XXXX-XXXX`) shown once at the end of onboarding,
  with a recovery form for another device or after the cookie expires
  (tolerant of copy/paste from tables: normalizes Unicode dashes,
  upper/lowercase and whitespace)
- Dashboard with required/completed days for the year and progress
- Annual calendar with 6 presence types
- Simulation of future scenarios against the annual target
- Settings: edit policy and monitoring start date at any time from the gear
  icon in the app header
- Deletion of the session and its data on user request

## Repo structure

```
backend/    FastAPI API (Python)
frontend/   React + Tailwind app (Vite)
docs/       Original spec and documentation
```

## Backend

See [backend/README.en.md](backend/README.en.md) for local setup and cPanel
deployment.

## Frontend

See [frontend/README.en.md](frontend/README.en.md) for local setup
(`npm install && npm run dev`).

## Deploy

Current flow: push to GitHub from your local environment → `git pull` on the
cPanel terminal in the repo folder (outside `public_html`) → `./deploy.sh`
(builds the frontend for smartworkingmanager.com, at the domain root, and
publishes only the static assets, without touching Passenger's `/api`
routing) → if Python dependencies changed, `pip install -r requirements.txt`
in the backend virtualenv → **Restart** the Python app from cPanel.

On this hosting, the Document Root of `smartworkingmanager.com` coincides
with `public_html/worklifebalancegm` (the same folder previously used for
`giemme76.com/worklifebalancegm/`): `deploy.sh` assumes this as the default
`PUBLIC_TARGET`. The two base paths are not compatible in the same folder, so
publishing the new build here means `giemme76.com/worklifebalancegm/` stops
working correctly — an accepted trade-off in favor of the new domain. If the
Document Root changes, override `PUBLIC_TARGET` (see the comments at the top
of `deploy.sh`).
