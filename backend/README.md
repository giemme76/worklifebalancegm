# OfficePresence — Backend

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

Il flusso previsto: push su GitHub dal proprio ambiente locale, poi pull
dell'hosting cPanel tramite "Git Version Control" (o SSH), e servizio
dell'app Python tramite **Setup Python App** (Passenger).

Passi:

1. Su cPanel, sezione **Git Version Control**: aggiungere il repository e
   fare pull/deploy della branch desiderata.
2. Su cPanel, sezione **Setup Python App**: creare una nuova app con
   - Application root: la cartella `backend/` del repo clonato
   - Application URL: se frontend e backend condividono lo stesso dominio,
     assegna al backend un path dedicato, es. `tuodominio.tld/api` (cPanel/
     Passenger si occupa di instradare le richieste su quel path all'app,
     che risponde comunque sulle sue rotte "a radice", es. `/session`,
     `/dashboard` — non serve modificare il codice)
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`
3. Nel virtualenv creato da cPanel (il pannello mostra il comando `source
   .../bin/activate`):
   ```bash
   pip install -r requirements.txt
   ```
4. Impostare le variabili d'ambiente (tab **Environment variables** della
   Python App), in particolare:
   - `DATABASE_URL=mysql+pymysql://utente:password@localhost/nome_db` (DB
     MySQL creato da cPanel > MySQL Databases)
   - `APP_ENV=production` (attiva anche il cookie di sessione `Secure`,
     necessario perché il sito gira in HTTPS)
   - `CORS_ORIGINS=https://tuodominio.tld` — se frontend e backend sono
     sullo **stesso dominio** (stesso path base, es. `/api`), le richieste
     sono same-origin e il browser non applica CORS: questa variabile serve
     comunque da rete di sicurezza e per eventuali test da altre origin.
5. **Restart** dell'app Python da cPanel.

Ad ogni aggiornamento: push su GitHub → pull su cPanel (Git Version Control
può farlo automaticamente o manualmente) → se sono cambiate le dipendenze,
`pip install -r requirements.txt` → **Restart** app.

`passenger_wsgi.py` adatta l'app ASGI di FastAPI al modello WSGI richiesto
da Passenger, tramite la libreria `a2wsgi`.

Nota: `init_db()` crea le tabelle mancanti all'avvio (comodo in sviluppo).
In produzione, su un DB già popolato, valutare migrazioni esplicite (es.
Alembic) prima di introdurre modifiche allo schema.
