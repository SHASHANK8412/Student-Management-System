from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permissions
from app.models.fee import FeeInvoice
from app.models.payment import Payment
from app.models.student import Student

router = APIRouter()


@router.get("/global", dependencies=[Depends(require_permissions("students:read"))])
def global_search(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    pattern = f"%{q}%"
    students = db.execute(
        select(Student).where(
            Student.is_deleted.is_(False),
            or_(
                Student.student_name.ilike(pattern),
                Student.father_name.ilike(pattern),
                Student.parent_name.ilike(pattern),
                Student.admission_number.ilike(pattern),
                Student.phone.ilike(pattern),
                Student.aadhar_number.ilike(pattern),
                Student.class_name.ilike(pattern),
            ),
        ).limit(10)
    ).scalars().all()
    receipts = db.execute(select(Payment).where(Payment.receipt_number.ilike(pattern)).limit(10)).scalars().all()
    invoices = db.execute(select(FeeInvoice).where(FeeInvoice.invoice_number.ilike(pattern)).limit(10)).scalars().all()
    return {
        "students": students,
        "receipts": receipts,
        "invoices": invoices,
    }
