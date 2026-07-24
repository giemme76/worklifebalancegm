# Smart Working Manager — Frontend

*[English version](README.en.md)*

App React (Vite + Tailwind) fedele al design "Smart Working Manager": onboarding in 3 step
(nome/nickname, azienda con ricerca Google Places, policy e data di inizio
monitoraggio, riepilogo con codice di recupero), poi Dashboard / Calendario /
Simulazione, collegata alle API del backend.

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
  components/onboarding/  wizard 3 step (nome/azienda, policy + data di inizio
                           monitoraggio, riepilogo) + schermata post-creazione col
                           codice di recupero
  components/app/         shell con tab bar, Dashboard, Calendario, Simulazione, bottom
                           sheet, pannello sessione (codice + eliminazione dati),
                           pannello impostazioni (policy + data di inizio monitoraggio)
  components/BrandWordmark.jsx  scritta colorata "Smart Working Manager" usata negli
                           header al posto di un logo grafico
  components/Footer.jsx   credito "Realizzato da Giemme76" + link all'ultimo commit
                           GitHub (hash iniettato in build da vite.config.js),
                           visibile in ogni schermata
  img/                    logo (usato come base per public/og-image.png, generato in
                           fase di sviluppo — vedi commenti in vite.config.js)
```

## Palette e stati

Colori e tipografia (Manrope) riprendono il design originale, col verde
principale ripreso dal logo originale (`src/img/`); le 6 tipologie di
presenza (Ufficio, Smart working, Ferie, Permesso, Malattia, Trasferta) e il
semaforo di andamento (verde/arancio/rosso) sono definiti una sola volta in
`tailwind.config.js` e `src/lib/statusDefs.js`.

## Sessione: recupero ed eliminazione

Ogni sessione ha un codice univoco (`SW-XXXX-XXXX`) mostrato una sola volta
subito dopo l'onboarding: è l'unico modo per recuperare i dati se il cookie
scade o si cambia dispositivo/browser ("Ho già un codice" nello step 1). Il
recupero funziona anche se il codice viene incollato da una tabella con
trattini "intelligenti" diversi dall'ASCII: il backend normalizza il
confronto (vedi `../backend/README.md`).
Cliccando sul badge col nickname nell'header dell'app si riapre lo stesso
codice, con un pulsante per eliminare definitivamente la sessione e tutti i
dati collegati. L'icona a ingranaggio accanto permette di modificare policy e
data di inizio monitoraggio in qualsiasi momento.
