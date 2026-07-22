from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserSession(Base):
    """Sessione utente login-free, identificata da un codice univoco (es. SW-8F2K-7LQ9)."""

    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)

    # Nome/nickname della persona che usa questo codice (una sessione = una
    # persona, non l'intera azienda): opzionale, usato per personalizzare i
    # saluti nell'app.
    nickname: Mapped[str | None] = mapped_column(String(120), nullable=True)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_accessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    company: Mapped["Company"] = relationship(back_populates="sessions")
    attendance_entries: Mapped[list["AttendanceEntry"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
