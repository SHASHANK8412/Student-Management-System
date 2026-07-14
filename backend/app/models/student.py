from datetime import date
from uuid import uuid4

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, Base


class Student(AuditMixin, Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid4()), unique=True, index=True, nullable=False)
    admission_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    student_name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    photo_url: Mapped[str | None] = mapped_column(String(500))
    gender: Mapped[str | None] = mapped_column(String(20))
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    class_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    section: Mapped[str | None] = mapped_column(String(20), index=True)
    roll_number: Mapped[str | None] = mapped_column(String(30), index=True)
    father_name: Mapped[str | None] = mapped_column(String(200), index=True)
    parent_name: Mapped[str | None] = mapped_column(String(200), index=True)
    mother_name: Mapped[str | None] = mapped_column(String(200))
    guardian_name: Mapped[str | None] = mapped_column(String(200))
    phone: Mapped[str | None] = mapped_column(String(30), index=True)
    aadhar_number: Mapped[str | None] = mapped_column(String(20), index=True)
    pen_number: Mapped[str | None] = mapped_column(String(30), index=True)
    caste: Mapped[str | None] = mapped_column(String(100), index=True)
    sub_caste: Mapped[str | None] = mapped_column(String(100), index=True)
    alternate_phone: Mapped[str | None] = mapped_column(String(30))
    email: Mapped[str | None] = mapped_column(String(255), index=True)
    address: Mapped[str | None] = mapped_column(Text)
    city: Mapped[str | None] = mapped_column(String(100), index=True)
    state: Mapped[str | None] = mapped_column(String(100), index=True)
    pin_code: Mapped[str | None] = mapped_column(String(20))
    joining_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="Active", nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text)


class StudentDocument(AuditMixin, Base):
    __tablename__ = "student_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    document_name: Mapped[str] = mapped_column(String(120), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str | None] = mapped_column(String(120))
    student: Mapped[Student] = relationship()
