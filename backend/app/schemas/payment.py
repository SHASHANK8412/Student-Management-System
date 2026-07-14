from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import APIModel


class PaymentBase(BaseModel):
    student_id: int
    fee_invoice_id: int | None = None
    amount: float = Field(gt=0)
    payment_date: datetime
    payment_mode: str = Field(min_length=2, max_length=30)
    reference_number: str | None = None
    remarks: str | None = None
    receipt_pdf_url: str | None = None


class PaymentCreate(PaymentBase):
    receipt_number: str | None = None


class PaymentRead(APIModel):
    id: int
    payment_id: str
    receipt_number: str
    student_id: int
    fee_invoice_id: int | None = None
    amount: float
    payment_date: datetime
    payment_mode: str
    reference_number: str | None = None
    remarks: str | None = None
    receipt_pdf_url: str | None = None


class PaymentRefundCreate(BaseModel):
    payment_id: int
    refund_amount: float = Field(gt=0)
    refund_date: datetime
    reason: str | None = None
