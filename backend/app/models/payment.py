from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import AuditMixin, Base


class Payment(AuditMixin, Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[str] = mapped_column(String(50), unique=True, index=True, default=lambda: f"PAY-{uuid4().hex[:12].upper()}")
    receipt_number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False, index=True)
    fee_invoice_id: Mapped[int | None] = mapped_column(ForeignKey("fee_invoices.id"), nullable=True, index=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    payment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    payment_mode: Mapped[str] = mapped_column(String(30), nullable=False)
    reference_number: Mapped[str | None] = mapped_column(String(100))
    remarks: Mapped[str | None] = mapped_column(Text)
    receipt_pdf_url: Mapped[str | None] = mapped_column(String(500))
    student: Mapped["Student"] = relationship()
    fee_invoice: Mapped[FeeInvoice | None] = relationship()


class PaymentRefund(AuditMixin, Base):
    __tablename__ = "payment_refunds"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey("payments.id"), nullable=False, index=True)
    refund_amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    refund_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reason: Mapped[str | None] = mapped_column(Text)
    payment: Mapped[Payment] = relationship()
