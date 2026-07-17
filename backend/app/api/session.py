from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.schemas.session import SessionCreateRequest, SessionOut
from app.services.session_service import create_session, get_session_by_code

router = APIRouter(tags=["session"])
settings = get_settings()


def _set_session_cookie(response: Response, code: str) -> None:
    response.set_cookie(
        key=settings.session_cookie_name,
        value=code,
        max_age=settings.session_cookie_max_age_seconds,
        httponly=True,
        samesite="lax",
        path="/",
    )


@router.post("/session", response_model=SessionOut, status_code=status.HTTP_201_CREATED)
def create_new_session(
    data: SessionCreateRequest, response: Response, db: Session = Depends(get_db)
) -> SessionOut:
    """Primo accesso: configura l'azienda e crea una nuova sessione login-free."""
    session = create_session(db, data)
    _set_session_cookie(response, session.code)
    return session


@router.get("/session/{code}", response_model=SessionOut)
def recover_session(code: str, response: Response, db: Session = Depends(get_db)) -> SessionOut:
    """Recupero sessione tramite codice univoco (ripristina anche il cookie)."""
    session = get_session_by_code(db, code)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Codice non trovato")
    _set_session_cookie(response, session.code)
    return session
