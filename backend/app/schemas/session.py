from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.company import CompanyOut, CompanySetup


class SessionCreateRequest(CompanySetup):
    """Dati inseriti al primo accesso per creare azienda + sessione."""

    # Stesso limite del campo lato frontend: il badge nell'header ha spazio
    # limitato, non ha senso accettare nickname più lunghi.
    nickname: str | None = Field(default=None, max_length=10)


class SessionOut(BaseModel):
    code: str
    nickname: str | None = None
    company: CompanyOut
    created_at: datetime

    model_config = {"from_attributes": True}
