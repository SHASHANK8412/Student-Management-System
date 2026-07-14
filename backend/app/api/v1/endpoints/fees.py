from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permissions
from app.models.fee import FeeInvoice, FeeInstallment, FeeStructure
from app.schemas.common import MessageResponse, PaginatedResponse, PaginationMeta
from app.schemas.fee import FeeInvoiceCreate, FeeInvoiceRead, FeeInvoiceUpdate, FeeStructureCreate, FeeStructureRead, InstallmentCreate
from app.services.fee_service import FeeService

router = APIRouter()


@router.get("/structures", response_model=PaginatedResponse[FeeStructureRead], dependencies=[Depends(require_permissions("fees:read"))])
def list_fee_structures(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), class_name: str | None = None, db: Session = Depends(get_db)):
    stmt = select(FeeStructure).where(FeeStructure.is_deleted.is_(False))
    if class_name:
        stmt = stmt.where(FeeStructure.class_name == class_name)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.execute(stmt.order_by(FeeStructure.class_name.asc()).offset((page - 1) * page_size).limit(page_size)).scalars().all()
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(items=items, meta=PaginationMeta(page=page, page_size=page_size, total=total, total_pages=total_pages))


@router.post("/structures", response_model=FeeStructureRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permissions("fees:write"))])
def create_fee_structure(payload: FeeStructureCreate, db: Session = Depends(get_db)):
    structure = FeeStructure(**payload.model_dump())
    db.add(structure)
    db.commit()
    db.refresh(structure)
    return structure


@router.get("/invoices", response_model=PaginatedResponse[FeeInvoiceRead], dependencies=[Depends(require_permissions("fees:read"))])
def list_fee_invoices(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), status: str | None = None, student_id: int | None = None, db: Session = Depends(get_db)):
    stmt = select(FeeInvoice).where(FeeInvoice.is_deleted.is_(False))
    if status:
        stmt = stmt.where(FeeInvoice.status == status)
    if student_id:
        stmt = stmt.where(FeeInvoice.student_id == student_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.execute(stmt.order_by(FeeInvoice.due_date.desc()).offset((page - 1) * page_size).limit(page_size)).scalars().all()
    total_pages = (total + page_size - 1) // page_size if total else 0
    return PaginatedResponse(items=items, meta=PaginationMeta(page=page, page_size=page_size, total=total, total_pages=total_pages))


@router.post("/invoices", response_model=FeeInvoiceRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permissions("fees:write"))])
def create_fee_invoice(payload: FeeInvoiceCreate, db: Session = Depends(get_db)):
    invoice = FeeInvoice(**payload.model_dump())
    invoice = FeeService(db).calculate_balance(invoice)
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.patch("/invoices/{invoice_id}", response_model=FeeInvoiceRead, dependencies=[Depends(require_permissions("fees:write"))])
def update_fee_invoice(invoice_id: int, payload: FeeInvoiceUpdate, db: Session = Depends(get_db)):
    invoice = db.get(FeeInvoice, invoice_id)
    if not invoice or invoice.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(invoice, key, value)
    invoice = FeeService(db).calculate_balance(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


@router.post("/invoices/{invoice_id}/installments", response_model=MessageResponse, dependencies=[Depends(require_permissions("fees:write"))])
def create_installment(invoice_id: int, payload: InstallmentCreate, db: Session = Depends(get_db)):
    invoice = db.get(FeeInvoice, invoice_id)
    if not invoice or invoice.is_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    installment = FeeInstallment(fee_invoice_id=invoice.id, **payload.model_dump(exclude={"fee_invoice_id"}))
    db.add(installment)
    db.commit()
    return MessageResponse(message="Installment created")
