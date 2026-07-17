"""Dependency FastAPI condivise dai router: DB session e sessione utente corrente."""

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.models.session import UserSession
from app.services.session_service import get_session_by_code

settings = get_settings()


def get_current_session(request: Request, db: Session = Depends(get_db)) -> UserSession:
    """Risolve la sessione corrente dal cookie del browser.

    Solleva 401 se il cookie manca o se il codice non corrisponde a nessuna sessione
    (es. cookie scaduto/non valido).
    """
    code = request.cookies.get(settings.session_cookie_name)
    if not code:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessione mancante")

    session = get_session_by_code(db, code)
    if session is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessione non valida")

    return session
