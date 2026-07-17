from datetime import datetime

from pydantic import BaseModel

from app.schemas.company import CompanyOut, CompanySetup


class SessionCreateRequest(CompanySetup):
    """Dati inseriti al primo accesso per creare azienda + sessione."""


class SessionOut(BaseModel):
    code: str
    company: CompanyOut
    created_at: datetime

    model_config = {"from_attributes": True}
