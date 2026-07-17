from pydantic import BaseModel


class DashboardOut(BaseModel):
    year: int

    total_working_days: int
    required_office_days: int
    required_smart_days: int

    completed_office_days: int
    completed_smart_days: int
    other_days: int  # ferie, permessi, malattia

    missing_office_days: int
    current_office_percentage: float
    current_smart_percentage: float

    on_track: bool
