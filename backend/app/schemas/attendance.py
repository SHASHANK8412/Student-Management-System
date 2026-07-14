from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import APIModel


class AttendanceBase(BaseModel):
    student_id: int
    attendance_date: date
    status: str = Field(min_length=1, max_length=20)
    remarks: str | None = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceRead(APIModel):
    id: int
    student_id: int
    attendance_date: date
    status: str
    remarks: str | None = None
