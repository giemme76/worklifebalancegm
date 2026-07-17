"""Entry point per l'hosting cPanel (Passenger).

Passenger si aspetta un'app **WSGI**, mentre FastAPI/Starlette sono **ASGI**.
Qui adattiamo l'app con `a2wsgi`.

Configurazione in cPanel > Setup Python App:
- Application root: la cartella `backend/` di questo repo (dopo il pull da GitHub)
- Application startup file: passenger_wsgi.py
- Application Entry point: application
- Variabili d'ambiente (tab "Environment variables"): DATABASE_URL, APP_ENV=production,
  SESSION_COOKIE_NAME, SESSION_COOKIE_MAX_AGE_DAYS, CORS_ORIGINS (vedi .env.example)

Dopo ogni pull da GitHub: eseguire `pip install -r requirements.txt` nel virtualenv creato
da cPanel e poi "Restart" dall'interfaccia Setup Python App.
"""

import sys
from pathlib import Path

# Garantisce che la cartella backend/ sia nel path, indipendentemente dalla
# working directory da cui Passenger avvia lo script.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from a2wsgi import ASGIMiddleware  # noqa: E402

from app.main import app as _fastapi_app  # noqa: E402

application = ASGIMiddleware(_fastapi_app)
