from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.database import get_db
from app.models.session import UserSession
from app.schemas.calendar import CalendarOut
from app.services.attendance_service import get_calendar

router = APIRouter(tags=["calendar"])


@router.get("/calendar", response_model=CalendarOut)
def read_calendar(
    year: int | None = None,
    session: UserSession = Depends(get_current_session),
    db: Session = Depends(get_db),
) -> CalendarOut:
    """Calendario annuale delle presenze (ufficio, smart working, ferie, permessi, malattia)."""
    return get_calendar(db, session, year or date.today().year)
