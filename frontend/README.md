# OfficePresence — Frontend

App React (Vite + Tailwind) fedele al design "WorkLife": onboarding in 3 step,
poi Dashboard / Calendario / Simulazione, collegata alle API del backend.

## Setup locale

```bash
cd frontend
npm install
cp .env.example .env   # punta VITE_API_BASE_URL al backend (default http://localhost:8000)
npm run dev
```

App su `http://localhost:5173`. Il backend deve girare in parallelo (vedi
`../backend/README.md`) con CORS che include questa origin (già di default
in `backend/.env.example`).

La sessione è gestita dal backend tramite cookie httponly: il browser la
mantiene automaticamente, non serve alcun login.

## Build di produzione

```bash
cp .env.example .env.production
# imposta VITE_API_BASE_URL=https://tuodominio.tld/api (path del backend su cPanel)
npm run build
```

Genera `dist/`: carica **il contenuto** di quella cartella (non la cartella
stessa) nella document root del dominio su cPanel — di solito `public_html/`,
o la sua root se il backend è pubblicato su un path dedicato come `/api`
tramite Setup Python App (vedi `../backend/README.md`).

Non essendoci routing lato client (un'unica pagina, stati mostrati
condizionalmente), non serve alcuna regola di riscrittura URL: un hosting
statico semplice basta.

## Struttura

```
src/
  api/client.js          wrapper fetch verso il backend (cookie di sessione incluso)
  context/                stato sessione + cache dashboard/calendario per anno
  lib/                    utility pure: date, stati presenza, palette, anteprima onboarding
  components/onboarding/  wizard 3 step (azienda, policy, riepilogo)
  components/app/         shell con tab bar, Dashboard, Calendario, Simulazione, bottom sheet
```

## Palette e stati

Colori e tipografia (Manrope) riprendono il design originale; le 6
tipologie di presenza (Ufficio, Smart working, Ferie, Permesso, Malattia,
Trasferta) e il semaforo di andamento (verde/arancio/rosso) sono definiti
una sola volta in `tailwind.config.js` e `src/lib/statusDefs.js`.

## Nota sull'ambiente di sviluppo di questa sessione

Il codice è stato scritto e rivisto manualmente, ma in questo sandbox
`npm run build` non è stato eseguibile fino in fondo (il binario nativo di
esbuild va in segmentation fault nell'ambiente isolato usato qui — un
limite dell'infrastruttura, non del codice). Prima di considerare il
frontend pronto, esegui in locale:

```bash
npm install
npm run build
```

e segnala eventuali errori: si risolvono rapidamente avendo un ambiente che
esegue esbuild normalmente.
