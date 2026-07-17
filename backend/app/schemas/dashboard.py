from typing import Literal

from pydantic import BaseModel

Pace = Literal["green", "orange", "red"]


class DashboardOut(BaseModel):
    year: int

    total_working_days: int
    required_office_days: int
    required_smart_days: int

    completed_office_days: int
    completed_smart_days: int
    other_days: int  # ferie, permessi, malattia, trasferta

    missing_office_days: int
    current_office_percentage: float
    current_smart_percentage: float

    # Semaforo di andamento rispetto al ritmo atteso nell'anno (come nel design):
    # green = in linea/obiettivo raggiunto, orange = a rischio, red = da recuperare.
    pace: Pace
    pace_label: str

    on_track: bool
