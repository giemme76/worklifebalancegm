# Smart Working Manager — Backend

API FastAPI per il monitoraggio delle presenze ufficio/smart working.

## Setup locale

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

API disponibile su `http://localhost:8000` (docs interattive su `/docs`).
In sviluppo usa SQLite in locale (`officepresence.db`), nessun DB esterno richiesto.

Per la ricerca aziende in onboarding (`GET /company/search`, Google Places
Text Search legacy) serve una `GOOGLE_MAPS_API_KEY` valida nel `.env` locale
(mai committarla: `.env` è già in `.gitignore`, in `.env.example` c'è solo il
placeholder). Senza chiave l'endpoint torna semplicemente risultati vuoti,
l'app resta comunque utilizzabile.

## Test

```bash
pytest
pytest --cov=app --cov-report=term-missing
```

Target di copertura: **> 90%**, con attenzione particolare alla logica di
calcolo in `app/services/calculation_service.py`.

## Struttura

```
app/
    api/            router FastAPI (endpoint HTTP)
    services/       logica di business
    models/         modelli SQLAlchemy
    schemas/        modelli Pydantic (request/response)
    repositories/    accesso al database
    utils/          funzioni di supporto (codice sessione, calcolo date)
tests/              test pytest, stessa struttura di app/
```

## Deploy su hosting cPanel

Setup in uso: repo clonato **fuori** da `public_html`, backend pubblicato con
**Setup Python App** (Passenger) su `smartworkingmanager.com/api` — stesso
dominio del frontend (vedi `../deploy.sh`), così il cookie di sessione resta
same-site invece di cross-site tra due domini diversi. Frontend buildato e
pubblicato come file statici alla radice del dominio da `../deploy.sh`.

Setup iniziale:

1. Clonare il repo sul server, fuori da `public_html`.
2. Su cPanel, sezione **Setup Python App**: creare una nuova app con
   - Application root: la cartella `backend/` del repo clonato
   - Application URL: `smartworkingmanager.com/api` (Passenger instrada le
     richieste su quel path all'app, che risponde comunque sulle sue rotte "a
     radice", es. `/session`, `/dashboard` — non serve modificare il codice)
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`
3. Nel virtualenv creato da cPanel (il pannello mostra il comando `source
   .../bin/activate`): `pip install -r requirements.txt`.
4. Variabili d'ambiente (tab **Environment variables** della Python App):
   - `DATABASE_URL=mysql+pymysql://utente:password@localhost/nome_db`
   - `APP_ENV=production` (attiva il cookie di sessione `Secure` — richiede
     SSL attivo sul dominio, altrimenti il browser scarta il cookie)
   - `CORS_ORIGINS=https://smartworkingmanager.com`
   - `GOOGLE_MAPS_API_KEY=...` (per la ricerca aziende in onboarding)
5. **Restart** dell'app Python da cPanel.

**Nota migrazione dominio:** il backend girava in precedenza su
`giemme76.com/worklifebalancegm/api`, con `CORS_ORIGINS` puntato lì. Se quel
deploy resta online in parallelo (path legacy, non più aggiornato), le due
app Python restano indipendenti: stesso codice, `Setup Python App` e
variabili d'ambiente separate per ciascuna.

Ad ogni aggiornamento: push su GitHub dal locale → `git pull` sul terminale
cPanel, dalla cartella del repo → se sono cambiate le dipendenze Python,
`pip install -r requirements.txt` nel virtualenv → **Restart** app da cPanel.

**Attenzione:** ricreare l'app da "Setup Python App" sovrascrive
`passenger_wsgi.py` con uno stub generico di cPanel. Se succede, ripristinarlo
con `git checkout -- passenger_wsgi.py` (deve contenere l'adattamento ASGI→WSGI
tramite `a2wsgi`, non lo stub).

**Attenzione:** `init_db()` crea solo le tabelle **mancanti** all'avvio, non
altera quelle già esistenti. Ogni volta che si aggiunge una colonna a un
modello (es. `UserSession.nickname`), su un DB di produzione già popolato va
applicata a mano, altrimenti l'endpoint che la usa risponde 500:

```sql
ALTER TABLE nome_tabella ADD COLUMN nome_colonna TIPO NULL;
```

In alternativa, valutare migrazioni esplicite (es. Alembic) prima di
introdurre ulteriori modifiche allo schema.
