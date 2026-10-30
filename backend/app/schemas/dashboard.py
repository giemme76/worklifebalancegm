from datetime import date
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
    other_days: int  # ferie, permessi, malattia (la trasferta conta come ufficio)

    missing_office_days: int
    current_office_percentage: float
    current_smart_percentage: float

    # Semaforo di andamento rispetto al ritmo atteso nell'anno (come nel design):
    # green = in linea/obiettivo raggiunto, orange = a rischio, red = da recuperare.
    pace: Pace
    pace_label: str

    on_track: bool

    # Finestra di monitoraggio dell'anno (None se non attiva) e copertura delle
    # registrazioni: giorni registrati fino a oggi sui giorni lavorativi già
    # trascorsi dall'inizio della finestra.
    period_start: date | None = None
    period_end: date | None = None
    elapsed_working_days: int = 0
    registered_days: int = 0
    registered_percentage: float = 0.0
