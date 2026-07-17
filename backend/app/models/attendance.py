import enum
from datetime import date as date_type
from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AttendanceType(str, enum.Enum):
    OFFICE = "OFFICE"
    SMART_WORKING = "SMART_WORKING"
    VACATION = "VACATION"
    PERMIT = "PERMIT"
    SICK = "SICK"


class AttendanceEntry(Base):
    """Singola voce del calendario presenze per una sessione, un giorno per voce."""

    __tablename__ = "attendance_entries"
    __table_args__ = (UniqueConstraint("session_id", "date", name="uq_session_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("user_sessions.id"), nullable=False)

    date: Mapped[date_type] = mapped_column(Date, nullable=False)
    type: Mapped[AttendanceType] = mapped_column(Enum(AttendanceType), nullable=False)

    # True per i giorni futuri ipotizzati dal simulatore: non contano nei conteggi reali
    # a meno che non venga richiesto esplicitamente (include_simulated=True).
    is_simulated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["UserSession"] = relationship(back_populates="attendance_entries")
