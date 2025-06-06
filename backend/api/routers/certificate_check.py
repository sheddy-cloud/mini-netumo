from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from api.database import get_db
from ..models.models import CertificateCheck, Target, User
from ..schemas.certificate_check import CertificateCheckCreate, CertificateCheckResponse, CertificateCheckUpdate
from api.utils.security import get_current_user

router = APIRouter(prefix="/certificatechecks", tags=["Certificate Checks"])

def verify_target_owner(target_id: int, user: User, db: Session):
    target = db.query(Target).filter(Target.id == target_id, Target.user_id == user.id).first()
    if not target:
        raise HTTPException(status_code=403, detail="Not authorized to access this target")
    return target

@router.post("/", response_model=CertificateCheckResponse)
def create_cert_check(cert: CertificateCheckCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Verify target belongs to current user
    verify_target_owner(cert.target_id, current_user, db)

    db_cert = CertificateCheck(
        target_id=cert.target_id,
        expiry_date=cert.expiry_date,
        days_remaining=cert.days_remaining,
        checked_at=datetime.now(timezone.utc),
    )
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

@router.get("/", response_model=List[CertificateCheckResponse])
def get_all_cert_checks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cert_checks = (
        db.query(CertificateCheck)
        .join(Target, CertificateCheck.target_id == Target.id)
        .filter(Target.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return cert_checks

@router.get("/{check_id}", response_model=CertificateCheckResponse)
def get_cert_check(check_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cert = (
        db.query(CertificateCheck)
        .join(Target, CertificateCheck.target_id == Target.id)
        .filter(CertificateCheck.id == check_id, Target.user_id == current_user.id)
        .first()
    )
    if not cert:
        raise HTTPException(
            status_code=404, detail="Certificate check not found"
        )
    return cert

@router.put("/{check_id}", response_model=CertificateCheckResponse)
def update_cert_check(check_id: int, cert_data: CertificateCheckUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cert = (
        db.query(CertificateCheck)
        .join(Target, CertificateCheck.target_id == Target.id)
        .filter(CertificateCheck.id == check_id, Target.user_id == current_user.id)
        .first()
    )
    if not cert:
        raise HTTPException(
            status_code=404, detail="Certificate check not found"
        )

    if cert_data.expiry_date is not None:
        cert.expiry_date = cert_data.expiry_date
    if cert_data.days_remaining is not None:
        cert.days_remaining = cert_data.days_remaining

    db.commit()
    db.refresh(cert)
    return cert
