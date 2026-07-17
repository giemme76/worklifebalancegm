from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.database import get_db
from app.models.session import UserSession
from app.schemas.dashboard import DashboardOut
from app.services.attendance_service import get_dashboard

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardOut)
def read_dashboard(
    year: int | None = None,
    session: UserSession = Depends(get_current_session),
    db: Session = Depends(get_db),
) -> DashboardOut:
    """Andamento e obiettivi dell'anno rispetto alla policy aziendale."""
    return get_dashboard(db, session, year or date.today().year)
