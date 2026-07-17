from datetime import date as date_type

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.database import get_db
from app.models.session import UserSession
from app.schemas.attendance import AttendanceCreate, AttendanceOut
from app.services.attendance_service import delete_attendance, record_attendance

router = APIRouter(tags=["attendance"])


@router.post("/attendance", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
def create_attendance(
    data: AttendanceCreate,
    session: UserSession = Depends(get_current_session),
    db: Session = Depends(get_db),
) -> AttendanceOut:
    """Inserisce (o aggiorna) la presenza di un giorno."""
    return record_attendance(db, session, data)


@router.delete("/attendance/{entry_date}", status_code=status.HTTP_204_NO_CONTENT)
def remove_attendance(
    entry_date: date_type,
    session: UserSession = Depends(get_current_session),
    db: Session = Depends(get_db),
) -> None:
    """Rimuove la registrazione di un giorno (es. 'Rimuovi registrazione' dal bottom sheet)."""
    deleted = delete_attendance(db, session, entry_date)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nessuna registrazione per questa data")
