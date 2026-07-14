from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import APIModel


class FeeStructureBase(BaseModel):
    class_name: str = Field(min_length=1, max_length=50)
    section: str | None = None
    academic_year: str = Field(min_length=4, max_length=20)
    admission_fee: float = 0
    tuition_fee: float = 0
    transport_fee: float = 0
    hostel_fee: float = 0
    library_fee: float = 0
    lab_fee: float = 0
    exam_fee: float = 0
    miscellaneous_charges: float = 0
    is_active: bool = True


class FeeStructureCreate(FeeStructureBase):
    pass


class FeeStructureRead(APIModel):
    id: int
    class_name: str
    section: str | None = None
    academic_year: str
    admission_fee: float
    tuition_fee: float
    transport_fee: float
    hostel_fee: float
    library_fee: float
    lab_fee: float
    exam_fee: float
    miscellaneous_charges: float
    is_active: bool


class FeeInvoiceBase(BaseModel):
    student_id: int
    fee_structure_id: int | None = None
    due_date: date
    billing_period: str | None = None
    total_fee: float = 0
    scholarship_amount: float = 0
    discount_amount: float = 0
    late_fee: float = 0
    amount_paid: float = 0
    balance_amount: float = 0
    status: str = "Pending"
    notes: str | None = None


class FeeInvoiceCreate(FeeInvoiceBase):
    pass


class FeeInvoiceUpdate(BaseModel):
    fee_structure_id: int | None = None
    due_date: date | None = None
    billing_period: str | None = None
    total_fee: float | None = None
    scholarship_amount: float | None = None
    discount_amount: float | None = None
    late_fee: float | None = None
    amount_paid: float | None = None
    balance_amount: float | None = None
    status: str | None = None
    notes: str | None = None


class FeeInvoiceRead(APIModel):
    id: int
    invoice_number: str
    student_id: int
    fee_structure_id: int | None = None
    due_date: date
    billing_period: str | None = None
    total_fee: float
    scholarship_amount: float
    discount_amount: float
    late_fee: float
    amount_paid: float
    balance_amount: float
    status: str
    notes: str | None = None


class InstallmentBase(BaseModel):
    fee_invoice_id: int
    installment_no: int
    amount_due: float
    due_date: date
    amount_paid: float = 0
    status: str = "Pending"


class InstallmentCreate(InstallmentBase):
    pass
