import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PolicyType(str, enum.Enum):
    """Come l'azienda definisce la presenza richiesta in ufficio."""

    PERCENT = "PERCENT"  # es. "60% dei giorni lavorativi in ufficio"
    FIXED_DAYS = "FIXED_DAYS"  # es. "3 giorni in ufficio a settimana"


class Company(Base):
    """Azienda configurata al primo accesso di un utente."""

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    headquarters: Mapped[str | None] = mapped_column(String(500), nullable=True)

    policy_type: Mapped[PolicyType] = mapped_column(
        Enum(PolicyType), nullable=False, default=PolicyType.PERCENT
    )

    # Usato solo se policy_type == PERCENT: percentuale di smart working (0-100).
    smart_working_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Usato solo se policy_type == FIXED_DAYS: giorni richiesti in ufficio a settimana.
    office_days_per_week: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Giorni lavorativi settimanali della persona (tipicamente 5), usato per calcolare
    # il totale dei giorni lavorativi nell'anno indipendentemente dalla policy.
    work_days_per_week: Mapped[int] = mapped_column(Integer, nullable=False, default=5)

    # Data da cui l'utente vuole iniziare a monitorare la policy (es. iniziato a
    # metà anno): i giorni richiesti/anno si calcolano solo da questa data in poi,
    # non dal 1° gennaio. None = nessuna restrizione (comportamento storico,
    # equivalente a partire dal 1° gennaio dell'anno).
    monitoring_start_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sessions: Mapped[list["UserSession"]] = relationship(back_populates="company")

    @property
    def office_percentage(self) -> float | None:
        """Percentuale di presenza richiesta in ufficio, se la policy è a percentuale."""
        if self.policy_type != PolicyType.PERCENT or self.smart_working_percentage is None:
            return None
        return 100 - self.smart_working_percentage
