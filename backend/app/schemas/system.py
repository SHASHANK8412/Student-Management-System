from pydantic import BaseModel, EmailStr

from app.schemas.common import APIModel


class SchoolProfileRead(APIModel):
    id: int
    school_name: str
    logo_url: str | None = None
    address: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    currency: str
    timezone: str
    academic_year: str | None = None
    is_active: bool


class AcademicYearCreate(BaseModel):
    name: str
    start_date: str
    end_date: str
    is_active: bool = False


class AcademicYearRead(APIModel):
    id: int
    name: str
    start_date: str
    end_date: str
    is_active: bool


class SystemSettingRead(APIModel):
    id: int
    setting_key: str
    setting_value: str
    description: str | None = None
    is_sensitive: bool
