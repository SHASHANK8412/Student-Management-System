from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permissions
from app.models.fee import FeeInvoice
from app.models.payment import Payment, PaymentRefund
from app.schemas.common import MessageResponse, PaginatedResponse, PaginationMeta
from app.schemas.payment import PaymentCreate, PaymentRead, PaymentRefundCreate
from app.services.payment_service import PaymentService

router = APIRouter()


@router.get("", response_model=PaginatedResponse[PaymentRead], dependencies=[Depends(require_permissions("payments:read"))])
def list_payments(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), student_id: int | None = None, db: Session = Depends(get_db)):
    stmt = select(Payment).where(Payment.is_deleted.is_(False))
    if student_id:
        stmt = stmt.where(Payment.student_id == student_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.execute(stmt.order_by(Payment.payment_date.desc()).offset((page - 1) * page_size).limit(page_size)).scalars().all()
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(items=items, meta=PaginationMeta(page=page, page_size=page_size, total=total, total_pages=total_pages))


@router.post("", response_model=PaymentRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permissions("payments:write"))])
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    invoice = db.get(FeeInvoice, payload.fee_invoice_id) if payload.fee_invoice_id else None
    payment = Payment(
        receipt_number=payload.receipt_number or f"RCPT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        **payload.model_dump(exclude={"receipt_number"}),
    )
    payment = PaymentService(db).record_payment(payment, invoice)
    db.commit()
    db.refresh(payment)
    return payment


@router.post("/refunds", response_model=MessageResponse, dependencies=[Depends(require_permissions("payments:write"))])
def create_refund(payload: PaymentRefundCreate, db: Session = Depends(get_db)):
    payment = db.get(Payment, payload.payment_id)
    if not payment or payment.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    PaymentService(db).refund(payment.id, payload.refund_amount, payload.reason)
    db.commit()
    return MessageResponse(message="Refund recorded")
