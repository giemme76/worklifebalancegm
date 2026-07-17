from datetime import date

from sqlalchemy.orm import Session

from app.models.attendance import AttendanceEntry
from app.models.session import UserSession
from app.repositories.attendance_repository import AttendanceRepository
from app.schemas.attendance import AttendanceCreate
from app.schemas.calendar import CalendarOut
from app.schemas.dashboard import DashboardOut
from app.schemas.simulation import SimulationOut, SimulationRequest
from app.services import calculation_service


def record_attendance(
    db: Session, session: UserSession, data: AttendanceCreate
) -> AttendanceEntry:
    """Registra (o aggiorna) la presenza di un giorno per la sessione."""
    repo = AttendanceRepository(db)
    entry = repo.upsert(
        session_id=session.id, date=data.date, type=data.type, is_simulated=data.is_simulated
    )
    db.commit()
    db.refresh(entry)
    return entry


def get_dashboard(db: Session, session: UserSession, year: int) -> DashboardOut:
    repo = AttendanceRepository(db)
    entries = repo.list_for_year(session.id, year, include_simulated=False)
    types = [e.type for e in entries]
    return calculation_service.build_dashboard(session.company, year, types)


def get_calendar(db: Session, session: UserSession, year: int) -> CalendarOut:
    repo = AttendanceRepository(db)
    entries = repo.list_for_year(session.id, year, include_simulated=False)
    counts = calculation_service.build_calendar_counts(e.type for e in entries)
    return CalendarOut(year=year, entries=list(entries), counts=counts)


def simulate(
    db: Session, session: UserSession, request: SimulationRequest, year: int | None = None
) -> SimulationOut:
    """Simula l'aggiunta di presenze future senza persisterle."""
    repo = AttendanceRepository(db)

    hypothetical_by_year: dict[int, list] = {}
    for item in request.hypothetical_entries:
        hypothetical_by_year.setdefault(item.date.year, []).append(item.type)

    target_year = year or (next(iter(hypothetical_by_year), date.today().year))

    real_entries = repo.list_for_year(session.id, target_year, include_simulated=False)
    real_types = [e.type for e in real_entries]
    hypothetical_types = hypothetical_by_year.get(target_year, [])

    return calculation_service.simulate(session.company, target_year, real_types, hypothetical_types)
