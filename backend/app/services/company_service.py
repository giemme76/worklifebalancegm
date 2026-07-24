from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.session import UserSession
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanySettingsUpdate


def update_company_settings(
    db: Session, session: UserSession, data: CompanySettingsUpdate
) -> Company:
    """Aggiorna policy e data di inizio monitoraggio dalla sezione impostazioni.

    Modifica l'azienda collegata alla sessione corrente: oggi ogni onboarding
    crea un'azienda dedicata, quindi non impatta altre sessioni.
    """
    repo = CompanyRepository(db)
    company = repo.update(session.company, data)
    db.commit()
    db.refresh(company)
    return company
