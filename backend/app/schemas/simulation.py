from datetime import date as date_type

from pydantic import BaseModel

from app.models.attendance import AttendanceType
from app.schemas.dashboard import DashboardOut


class SimulationEntry(BaseModel):
    date: date_type
    type: AttendanceType


class SimulationRequest(BaseModel):
    hypothetical_entries: list[SimulationEntry]


class SimulationOut(BaseModel):
    projected: DashboardOut
    delta_office_days: int
    delta_office_percentage: float
