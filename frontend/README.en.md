# Smart Working Manager — Frontend

*[Versione italiana](README.md)*

React app (Vite + Tailwind) matching the "Smart Working Manager" design:
3-step onboarding (name/nickname, company with Google Places search, policy
and monitoring start date, summary with recovery code), then
Dashboard / Calendar / Simulation, connected to the backend API.

## Local setup

```bash
cd frontend
npm install
cp .env.example .env   # point VITE_API_BASE_URL to the backend (default http://localhost:8000)
npm run dev
```

App at `http://localhost:5173`. The backend must be running in parallel (see
`../backend/README.en.md`) with CORS including this origin (already the
default in `backend/.env.example`).

The session is managed by the backend via an httponly cookie: the browser
keeps it automatically, no login required.

## Production build

```bash
cp .env.example .env.production
# set VITE_API_BASE_URL=https://yourdomain.tld/api (backend path on cPanel)
npm run build
```

Generates `dist/`: upload **the contents** of that folder (not the folder
itself) to the domain's document root on cPanel — usually `public_html/`, or
its root if the backend is published on a dedicated path like `/api` via
Setup Python App (see `../backend/README.en.md`).

Since there is no client-side routing (a single page, states shown
conditionally), no URL rewrite rule is needed: plain static hosting is
enough.

## Structure

```
src/
  api/client.js          fetch wrapper towards the backend (session cookie included)
  context/                session state + dashboard/calendar cache per year
  lib/                    pure utilities: dates, presence statuses, palette, onboarding preview
  components/onboarding/  3-step wizard (name/company, policy + monitoring start
                           date, summary) + post-creation screen with the
                           recovery code
  components/app/         shell with tab bar, Dashboard, Calendar, Simulation, bottom
                           sheet, session panel (code + data deletion),
                           settings panel (policy + monitoring start date)
  components/BrandWordmark.jsx  colored "Smart Working Manager" wordmark used in
                           headers instead of a graphic logo
  components/Footer.jsx   "Made by Giemme76" credit + link to the latest GitHub
                           commit (hash injected at build time by vite.config.js),
                           visible on every screen
  img/                    logo (used as the base for public/og-image.png, generated
                           during development — see comments in vite.config.js)
```

## Palette and statuses

Colors and typography (Manrope) follow the original design, with the main
green taken from the logo (`src/img/`); the 6 presence types (Office, Smart
working, Vacation, Permit, Sick leave, Travel) and the progress indicator
(green/orange/red) are defined once in `tailwind.config.js` and
`src/lib/statusDefs.js`.

## Session: recovery and deletion

Every session has a unique code (`SW-XXXX-XXXX`) shown once right after
onboarding: it's the only way to recover data if the cookie expires or you
switch device/browser ("I already have a code" in step 1). Recovery also
works if the code is pasted from a table with "smart" dashes different from
plain ASCII: the backend normalizes the comparison (see
`../backend/README.en.md`).
Clicking the nickname badge in the app header reopens the same code, with a
button to permanently delete the session and all its data. The gear icon
next to it lets you edit the policy and monitoring start date at any time.
