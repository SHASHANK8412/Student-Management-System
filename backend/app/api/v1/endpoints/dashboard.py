from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permissions
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()


@router.get("", response_model=DashboardResponse, dependencies=[Depends(require_permissions("reports:read"))])
def dashboard(db: Session = Depends(get_db)):
    return DashboardService(db).build()
