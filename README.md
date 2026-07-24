# Smart Working Manager

App web login-free per monitorare il rispetto della policy di presenza in
ufficio / smart working: onboarding in 3 step, dashboard con obiettivo annuale
e semaforo di andamento, calendario, simulazione di scenari futuri.

Live: https://smartworkingmanager.com/ (in precedenza su
https://giemme76.com/worklifebalancegm/, ancora online ma non più aggiornato)

Vedi [docs/OfficePresence.md](docs/OfficePresence.md) per il concept iniziale
(alcuni dettagli sono superati dall'implementazione reale, allineata al design
effettivo: policy configurabile a percentuale o a giorni fissi/settimana, 6
tipologie di presenza incluso "Trasferta", semaforo verde/arancio/rosso).

## Funzionalità principali

- Onboarding senza registrazione: nome/nickname, ricerca azienda reale
  (Google Places) con sede rilevata automaticamente, policy a scelta
- Codice univoco di recupero (`SW-XXXX-XXXX`) mostrato a fine onboarding, con
  form di recupero sessione da un altro dispositivo o dopo la scadenza del
  cookie
- Dashboard con giorni richiesti/completati nell'anno e andamento
- Calendario annuale con 6 tipologie di presenza
- Simulazione di scenari futuri sull'obiettivo annuale
- Eliminazione sessione e dati collegati su richiesta dell'utente

## Struttura repo

```
backend/    API FastAPI (Python)
frontend/   App React + Tailwind (Vite)
docs/       Specifica iniziale e documentazione
```

## Backend

Vedi [backend/README.md](backend/README.md) per setup locale e deploy su hosting cPanel.

## Frontend

Vedi [frontend/README.md](frontend/README.md) per setup locale (`npm install && npm run dev`).

## Deploy

Flusso in uso: push su GitHub dal proprio ambiente locale → `git pull` sul
terminale cPanel nella cartella del repo (fuori da `public_html`) → `./deploy.sh`
(builda il frontend per smartworkingmanager.com, alla radice del dominio, e
pubblica solo gli asset statici, senza toccare il routing `/api` di Passenger)
→ se sono cambiate le dipendenze Python, `pip install -r requirements.txt` nel
virtualenv del backend → **Restart** dell'app Python da cPanel.

`deploy.sh` verifica `PUBLIC_TARGET` (document root del dominio): controllarla
prima del primo deploy sul nuovo dominio. Per rifare invece un deploy sotto
`giemme76.com/worklifebalancegm/` (il path dedicato usato in precedenza), vedi
i commenti in testa a `deploy.sh`.
