from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permissions
from app.models.system import AcademicYear, SchoolProfile, SystemSetting
from app.schemas.common import MessageResponse
from app.schemas.system import AcademicYearCreate, AcademicYearRead, SchoolProfileRead, SystemSettingRead

router = APIRouter()


@router.get("/school", response_model=SchoolProfileRead, dependencies=[Depends(require_permissions("settings:read"))])
def get_school_profile(db: Session = Depends(get_db)):
    profile = db.query(SchoolProfile).filter(SchoolProfile.is_deleted.is_(False)).order_by(SchoolProfile.id.asc()).first()
    if not profile:
        profile = SchoolProfile(school_name="Student Fee Management System")
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


@router.get("/academic-years", response_model=list[AcademicYearRead], dependencies=[Depends(require_permissions("settings:read"))])
def list_academic_years(db: Session = Depends(get_db)):
    return db.execute(select(AcademicYear).where(AcademicYear.is_deleted.is_(False)).order_by(AcademicYear.created_at.desc())).scalars().all()


@router.post("/academic-years", response_model=AcademicYearRead, dependencies=[Depends(require_permissions("settings:write"))])
def create_academic_year(payload: AcademicYearCreate, db: Session = Depends(get_db)):
    academic_year = AcademicYear(**payload.model_dump())
    db.add(academic_year)
    db.commit()
    db.refresh(academic_year)
    return academic_year


@router.get("/system", response_model=list[SystemSettingRead], dependencies=[Depends(require_permissions("settings:read"))])
def list_system_settings(db: Session = Depends(get_db)):
    return db.execute(select(SystemSetting).where(SystemSetting.is_deleted.is_(False)).order_by(SystemSetting.setting_key.asc())).scalars().all()


@router.post("/backup", response_model=MessageResponse, dependencies=[Depends(require_permissions("settings:write"))])
def backup_database():
    return MessageResponse(message="Database backup should be triggered by your managed infrastructure or scheduled job")


@router.post("/restore", response_model=MessageResponse, dependencies=[Depends(require_permissions("settings:write"))])
def restore_database():
    return MessageResponse(message="Database restore should be handled from a verified backup artifact")
