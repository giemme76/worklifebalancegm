from sqlalchemy.orm import Session

from app.models.session import UserSession
from app.repositories.company_repository import CompanyRepository
from app.repositories.session_repository import SessionRepository
from app.schemas.session import SessionCreateRequest
from app.services.company_lookup_service import lookup_company
from app.utils.code_generator import generate_session_code

_MAX_CODE_ATTEMPTS = 10


def _generate_unique_code(session_repo: SessionRepository) -> str:
    for _ in range(_MAX_CODE_ATTEMPTS):
        code = generate_session_code()
        if not session_repo.code_exists(code):
            return code
    raise RuntimeError("Impossibile generare un codice sessione univoco, riprovare.")


def create_session(db: Session, data: SessionCreateRequest) -> UserSession:
    """Configura l'azienda e crea una nuova sessione login-free (primo accesso)."""
    company_repo = CompanyRepository(db)
    session_repo = SessionRepository(db)

    website = data.website
    if not website:
        lookup = lookup_company(data.name)
        website = lookup.website

    company = company_repo.create(data, website=website)
    code = _generate_unique_code(session_repo)
    nickname = data.nickname.strip() if data.nickname and data.nickname.strip() else None
    session = session_repo.create(code=code, company_id=company.id, nickname=nickname)

    db.commit()
    db.refresh(session)
    return session


def get_session_by_code(db: Session, code: str) -> UserSession | None:
    """Recupera una sessione tramite codice univoco (usato anche per il cookie)."""
    session_repo = SessionRepository(db)
    session = session_repo.get_by_code(code)
    if session is None:
        return None
    session_repo.touch(session)
    db.commit()
    return session
