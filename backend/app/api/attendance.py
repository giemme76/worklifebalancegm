from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.database import get_db
from app.models.session import UserSession
from app.schemas.attendance import AttendanceCreate, AttendanceOut
from app.services.attendance_service import record_attendance

router = APIRouter(tags=["attendance"])


@router.post("/attendance", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
def create_attendance(
    data: AttendanceCreate,
    session: UserSession = Depends(get_current_session),
    db: Session = Depends(get_db),
) -> AttendanceOut:
    """Inserisce (o aggiorna) la presenza di un giorno."""
    return record_attendance(db, session, data)
