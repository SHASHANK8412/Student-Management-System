from datetime import date
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.fee import FeeInvoice, FeeStructure
from app.repositories.fee_repository import FeeInvoiceRepository, FeeStructureRepository


class FeeService:
    def __init__(self, session: Session):
        self.session = session
        self.structures = FeeStructureRepository(session)
        self.invoices = FeeInvoiceRepository(session)

    def calculate_balance(self, invoice: FeeInvoice) -> FeeInvoice:
        invoice.balance_amount = max(float(invoice.total_fee) + float(invoice.late_fee) - float(invoice.scholarship_amount) - float(invoice.discount_amount) - float(invoice.amount_paid), 0)
        invoice.status = "Paid" if invoice.balance_amount == 0 else ("Partial" if float(invoice.amount_paid) > 0 else "Pending")
        return invoice

    def list_overdue(self):
        return self.invoices.overdue()
