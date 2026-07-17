from pydantic import BaseModel, Field


class CompanyLookupResponse(BaseModel):
    """Risultato (best-effort) della ricerca automatica di sito e sede principale."""

    website: str | None = None
    suggested_headquarters: str | None = None


class CompanyOut(BaseModel):
    id: int
    name: str
    website: str | None = None
    headquarters: str | None = None
    smart_working_percentage: float
    work_days_per_week: int

    model_config = {"from_attributes": True}


class CompanySetup(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    website: str | None = None
    headquarters: str | None = None
    smart_working_percentage: float = Field(ge=0, le=100)
    work_days_per_week: int = Field(ge=1, le=7, default=5)
