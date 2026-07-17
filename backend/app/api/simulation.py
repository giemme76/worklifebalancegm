from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.database import get_db
from app.models.session import UserSession
from app.schemas.simulation import SimulationOut, SimulationRequest
from app.services.attendance_service import simulate

router = APIRouter(tags=["simulation"])


@router.post("/simulation", response_model=SimulationOut)
def run_simulation(
    request: SimulationRequest,
    session: UserSession = Depends(get_current_session),
    db: Session = Depends(get_db),
) -> SimulationOut:
    """Simula l'aggiunta di giorni futuri e restituisce l'effetto sull'obiettivo."""
    return simulate(db, session, request)
