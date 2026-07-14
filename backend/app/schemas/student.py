from datetime import date
import re

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.schemas.common import APIModel


class StudentBase(BaseModel):
    admission_number: str = Field(min_length=1, max_length=50)
    student_name: str = Field(min_length=2, max_length=200)
    photo_url: str | None = None
    gender: str | None = None
    date_of_birth: date | None = None
    class_name: str = Field(min_length=1, max_length=50)
    section: str | None = None
    roll_number: str | None = None
    father_name: str | None = None
    parent_name: str | None = None
    mother_name: str | None = None
    guardian_name: str | None = None
    phone: str | None = None
    aadhar_number: str | None = None
    pen_number: str | None = None
    caste: str | None = None
    sub_caste: str | None = None
    alternate_phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    pin_code: str | None = None
    joining_date: date | None = None
    status: str = Field(default="Active", max_length=30)
    notes: str | None = None

    @field_validator("phone", "alternate_phone", "aadhar_number", "pen_number", mode="before")
    @classmethod
    def normalize_blank_strings(cls, value):
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None and not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must be exactly 10 digits")
        return value

    @field_validator("aadhar_number")
    @classmethod
    def validate_aadhar_number(cls, value):
        if value is not None and not re.fullmatch(r"\d{12}", value):
            raise ValueError("Aadhaar number must be exactly 12 digits")
        return value


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    student_name: str | None = Field(default=None, max_length=200)
    photo_url: str | None = None
    gender: str | None = None
    date_of_birth: date | None = None
    class_name: str | None = None
    section: str | None = None
    roll_number: str | None = None
    father_name: str | None = None
    parent_name: str | None = None
    mother_name: str | None = None
    guardian_name: str | None = None
    phone: str | None = None
    aadhar_number: str | None = None
    pen_number: str | None = None
    caste: str | None = None
    sub_caste: str | None = None
    alternate_phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    pin_code: str | None = None
    joining_date: date | None = None
    status: str | None = Field(default=None, max_length=30)
    notes: str | None = None

    @field_validator("phone", "alternate_phone", "aadhar_number", "pen_number", mode="before")
    @classmethod
    def normalize_blank_strings(cls, value):
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None and not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must be exactly 10 digits")
        return value

    @field_validator("aadhar_number")
    @classmethod
    def validate_aadhar_number(cls, value):
        if value is not None and not re.fullmatch(r"\d{12}", value):
            raise ValueError("Aadhaar number must be exactly 12 digits")
        return value


class StudentRead(APIModel):
    id: int
    public_id: str
    admission_number: str
    student_name: str
    photo_url: str | None = None
    gender: str | None = None
    date_of_birth: date | None = None
    class_name: str
    section: str | None = None
    roll_number: str | None = None
    father_name: str | None = None
    parent_name: str | None = None
    mother_name: str | None = None
    guardian_name: str | None = None
    phone: str | None = None
    aadhar_number: str | None = None
    pen_number: str | None = None
    caste: str | None = None
    sub_caste: str | None = None
    alternate_phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    pin_code: str | None = None
    joining_date: date | None = None
    status: str
    notes: str | None = None
