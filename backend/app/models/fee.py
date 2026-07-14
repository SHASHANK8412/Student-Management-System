from datetime import date
from uuid import uuid4

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, Base


class FeeStructure(AuditMixin, Base):
    __tablename__ = "fee_structures"

    id: Mapped[int] = mapped_column(primary_key=True)
    class_name: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    section: Mapped[str | None] = mapped_column(String(20), index=True)
    academic_year: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    admission_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    tuition_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    transport_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    hostel_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    library_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    lab_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    exam_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    miscellaneous_charges: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


class FeeInvoice(AuditMixin, Base):
    __tablename__ = "fee_invoices"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, default=lambda: f"INV-{uuid4().hex[:12].upper()}")
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    fee_structure_id: Mapped[int | None] = mapped_column(ForeignKey("fee_structures.id"), nullable=True)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    billing_period: Mapped[str | None] = mapped_column(String(50))
    total_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    scholarship_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    discount_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    late_fee: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    amount_paid: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    balance_amount: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    status: Mapped[str] = mapped_column(String(30), default="Pending", index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    student: Mapped["Student"] = relationship()
    fee_structure: Mapped[FeeStructure | None] = relationship()


class FeeInstallment(AuditMixin, Base):
    __tablename__ = "fee_installments"

    id: Mapped[int] = mapped_column(primary_key=True)
    fee_invoice_id: Mapped[int] = mapped_column(ForeignKey("fee_invoices.id"), nullable=False, index=True)
    installment_no: Mapped[int] = mapped_column(Integer, nullable=False)
    amount_due: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    amount_paid: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    status: Mapped[str] = mapped_column(String(30), default="Pending", index=True)
    fee_invoice: Mapped[FeeInvoice] = relationship()
