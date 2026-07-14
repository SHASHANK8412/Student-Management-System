from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permissions
from app.models.fee import FeeInvoice
from app.models.payment import Payment
from app.models.student import Student

router = APIRouter()


@router.get("/collection", dependencies=[Depends(require_permissions("reports:read"))])
def collection_report(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    stmt = select(func.coalesce(func.sum(Payment.amount), 0)).where(Payment.is_deleted.is_(False))
    if start_date:
        stmt = stmt.where(func.date(Payment.payment_date) >= start_date)
    if end_date:
        stmt = stmt.where(func.date(Payment.payment_date) <= end_date)
    return {"total_collection": float(db.scalar(stmt) or 0)}


@router.get("/pending-fees", dependencies=[Depends(require_permissions("reports:read"))])
def pending_fees(db: Session = Depends(get_db)):
    total = db.scalar(select(func.coalesce(func.sum(FeeInvoice.balance_amount), 0)).where(FeeInvoice.is_deleted.is_(False), FeeInvoice.balance_amount > 0)) or 0
    return {"pending_fees": float(total)}


@router.get("/student-ledger", dependencies=[Depends(require_permissions("reports:read"))])
def student_ledger(student_id: int, db: Session = Depends(get_db)):
    student = db.get(Student, student_id)
    if not student:
        return {"student_id": student_id, "entries": []}
    invoices = db.execute(select(FeeInvoice).where(FeeInvoice.student_id == student_id, FeeInvoice.is_deleted.is_(False))).scalars().all()
    return {
        "student_id": student_id,
        "entries": [
            {
                "invoice_number": invoice.invoice_number,
                "due_date": invoice.due_date,
                "total_fee": float(invoice.total_fee),
                "amount_paid": float(invoice.amount_paid),
                "balance_amount": float(invoice.balance_amount),
                "status": invoice.status,
            }
            for invoice in invoices
        ],
    }
