from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Company(Base):
    """Azienda configurata al primo accesso di un utente."""

    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    headquarters: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Percentuale di smart working prevista dalla policy aziendale (0-100).
    smart_working_percentage: Mapped[float] = mapped_column(Float, nullable=False)

    # Giorni lavorativi settimanali (tipicamente 5).
    work_days_per_week: Mapped[int] = mapped_column(Integer, nullable=False, default=5)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    sessions: Mapped[list["UserSession"]] = relationship(back_populates="company")

    @property
    def office_percentage(self) -> float:
        return 100 - self.smart_working_percentage
