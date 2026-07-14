from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.fee import FeeInvoice
from app.models.payment import Payment, PaymentRefund
from app.repositories.payment_repository import PaymentRepository


class PaymentService:
    def __init__(self, session: Session):
        self.session = session
        self.payments = PaymentRepository(session)

    def record_payment(self, payment: Payment, invoice: FeeInvoice | None = None) -> Payment:
        self.session.add(payment)
        if invoice:
            invoice.amount_paid = float(invoice.amount_paid) + float(payment.amount)
            invoice.balance_amount = max(float(invoice.total_fee) + float(invoice.late_fee) - float(invoice.scholarship_amount) - float(invoice.discount_amount) - float(invoice.amount_paid), 0)
            invoice.status = "Paid" if invoice.balance_amount == 0 else "Partial"
        self.session.flush()
        return payment

    def refund(self, payment_id: int, amount: float, reason: str | None) -> PaymentRefund:
        refund = PaymentRefund(payment_id=payment_id, refund_amount=amount, refund_date=datetime.now(timezone.utc), reason=reason)
        self.session.add(refund)
        self.session.flush()
        return refund
