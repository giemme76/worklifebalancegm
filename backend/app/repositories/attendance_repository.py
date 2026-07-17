from datetime import date as date_type

from sqlalchemy import extract, select
from sqlalchemy.orm import Session

from app.models.attendance import AttendanceEntry, AttendanceType


class AttendanceRepository:
    def __init__(self, db: Session):
        self.db = db

    def upsert(
        self, session_id: int, date: date_type, type: AttendanceType, is_simulated: bool = False
    ) -> AttendanceEntry:
        """Crea o aggiorna la voce per (session_id, date), mantenendo un'unica voce al giorno."""
        existing = self.get_by_session_and_date(session_id, date)
        if existing is not None:
            existing.type = type
            existing.is_simulated = is_simulated
            self.db.flush()
            return existing

        entry = AttendanceEntry(
            session_id=session_id, date=date, type=type, is_simulated=is_simulated
        )
        self.db.add(entry)
        self.db.flush()
        return entry

    def get_by_session_and_date(self, session_id: int, date: date_type) -> AttendanceEntry | None:
        stmt = select(AttendanceEntry).where(
            AttendanceEntry.session_id == session_id, AttendanceEntry.date == date
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def list_for_year(
        self, session_id: int, year: int, include_simulated: bool = False
    ) -> list[AttendanceEntry]:
        stmt = select(AttendanceEntry).where(
            AttendanceEntry.session_id == session_id,
            extract("year", AttendanceEntry.date) == year,
        )
        if not include_simulated:
            stmt = stmt.where(AttendanceEntry.is_simulated.is_(False))
        stmt = stmt.order_by(AttendanceEntry.date)
        return list(self.db.execute(stmt).scalars().all())

    def delete_simulated(self, session_id: int) -> None:
        entries = self.list_for_year_all_simulated(session_id)
        for entry in entries:
            self.db.delete(entry)
        self.db.flush()

    def list_for_year_all_simulated(self, session_id: int) -> list[AttendanceEntry]:
        stmt = select(AttendanceEntry).where(
            AttendanceEntry.session_id == session_id, AttendanceEntry.is_simulated.is_(True)
        )
        return list(self.db.execute(stmt).scalars().all())
