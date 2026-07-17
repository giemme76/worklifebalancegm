from pydantic import BaseModel, Field, model_validator

from app.models.company import PolicyType


class CompanyLookupResponse(BaseModel):
    """Risultato (best-effort) della ricerca automatica di sito e sede principale."""

    website: str | None = None
    suggested_headquarters: str | None = None


class CompanyOut(BaseModel):
    id: int
    name: str
    website: str | None = None
    headquarters: str | None = None
    policy_type: PolicyType
    smart_working_percentage: float | None = None
    office_days_per_week: int | None = None
    work_days_per_week: int

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

    @model_validator(mode="after")
    def _check_policy_fields(self) -> "CompanySetup":
        if self.policy_type == PolicyType.PERCENT:
            if self.smart_working_percentage is None:
                raise ValueError(
                    "smart_working_percentage è richiesto quando policy_type è PERCENT"
                )
        elif self.policy_type == PolicyType.FIXED_DAYS:
            if self.office_days_per_week is None:
                raise ValueError(
                    "office_days_per_week è richiesto quando policy_type è FIXED_DAYS"
                )
            if self.office_days_per_week > self.work_days_per_week:
                raise ValueError(
                    "office_days_per_week non può superare work_days_per_week"
                )
        return self
