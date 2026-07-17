from pydantic import BaseModel

from app.schemas.attendance import AttendanceOut


class CalendarCounts(BaseModel):
    office: int = 0
    smart_working: int = 0
    vacation: int = 0
    permit: int = 0
    sick: int = 0


class CalendarOut(BaseModel):
    year: int
    entries: list[AttendanceOut]
    counts: CalendarCounts
