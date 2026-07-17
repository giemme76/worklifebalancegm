from datetime import date as date_type

from pydantic import BaseModel

from app.models.attendance import AttendanceType


class AttendanceCreate(BaseModel):
    date: date_type
    type: AttendanceType
    is_simulated: bool = False


class AttendanceOut(BaseModel):
    id: int
    date: date_type
    type: AttendanceType
    is_simulated: bool

    model_config = {"from_attributes": True}
