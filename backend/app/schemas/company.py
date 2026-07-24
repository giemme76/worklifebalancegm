from datetime import date

from pydantic import BaseModel, Field, model_validator

from app.models.company import PolicyType


def _validate_policy_fields(model: "CompanySetup | CompanySettingsUpdate"):
    """Regole condivise tra creazione (onboarding) e aggiornamento (impostazioni)
    della policy aziendale: campo richiesto in base al tipo di policy scelto."""
    if model.policy_type == PolicyType.PERCENT:
        if model.smart_working_percentage is None:
            raise ValueError(
                "smart_working_percentage è richiesto quando policy_type è PERCENT"
            )
    elif model.policy_type == PolicyType.FIXED_DAYS:
        if model.office_days_per_week is None:
            raise ValueError(
                "office_days_per_week è richiesto quando policy_type è FIXED_DAYS"
            )
        if model.office_days_per_week > model.work_days_per_week:
            raise ValueError("office_days_per_week non può superare work_days_per_week")
    return model


class CompanyLookupResponse(BaseModel):
    """Risultato (best-effort) della ricerca automatica di sito e sede principale."""

    website: str | None = None
    suggested_headquarters: str | None = None


class CompanySearchResult(BaseModel):
    """Un candidato restituito da Google Places per un nome azienda."""

    place_id: str
    name: str
    address: str | None = None
    city: str | None = None
    website: str | None = None
    rating: float | None = None
    lat: float | None = None
    lng: float | None = None


class CompanySearchResponse(BaseModel):
    results: list[CompanySearchResult]
    # Presente solo se la chiamata a Google Places è fallita: aiuta a
    # diagnosticare (chiave/API non abilitata, quota, ecc.) senza dover
    # scavare nei log del server. Non contiene mai la chiave API.
    error: str | None = None


class CompanyOut(BaseModel):
    id: int
    name: str
    website: str | None = None
    headquarters: str | None = None
    policy_type: PolicyType
    smart_working_percentage: float | None = None
    office_days_per_week: int | None = None
    work_days_per_week: int
    # None solo per aziende create prima dell'introduzione di questo campo.
    monitoring_start_date: date | None = None

    model_config = {"from_attributes": True}


class CompanySetup(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    website: str | None = None
    headquarters: str | None = None

    policy_type: PolicyType = PolicyType.PERCENT
    # Richiesto se policy_type == PERCENT: percentuale di smart working (0-100).
    smart_working_percentage: float | None = Field(default=None, ge=0, le=100)
    # Richiesto se policy_type == FIXED_DAYS: giorni in ufficio richiesti a settimana.
    office_days_per_week: int | None = Field(default=None, ge=1, le=7)

    work_days_per_week: int = Field(ge=1, le=7, default=5)

    # Data da cui iniziare a monitorare la policy (scelta in onboarding, default oggi).
    monitoring_start_date: date = Field(default_factory=date.today)

    @model_validator(mode="after")
    def _check_policy_fields(self) -> "CompanySetup":
        return _validate_policy_fields(self)


class CompanySettingsUpdate(BaseModel):
    """Aggiornamento della policy e della data di inizio monitoraggio dalla
    sezione impostazioni della dashboard (non tocca nome/sede azienda)."""

    policy_type: PolicyType
    smart_working_percentage: float | None = Field(default=None, ge=0, le=100)
    office_days_per_week: int | None = Field(default=None, ge=1, le=7)
    work_days_per_week: int = Field(ge=1, le=7, default=5)
    monitoring_start_date: date

    @model_validator(mode="after")
    def _check_policy_fields(self) -> "CompanySettingsUpdate":
        return _validate_policy_fields(self)
