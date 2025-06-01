# backend/api/routers/certificate_check.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from api.database import get_db
from ..models.models import CertificateCheck
from ..schemas.certificate_check import (
    CertificateCheckCreate,
    CertificateCheckResponse,
    CertificateCheckUpdate,
)

router = APIRouter(prefix="/certificatechecks", tags=["Certificate Checks"])


# Create certificate check (machine action)
@router.post("/", response_model=CertificateCheckResponse)
def create_cert_check(cert: CertificateCheckCreate, db: Session = Depends(get_db)):
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


# Get all certificate checks
@router.get("/", response_model=List[CertificateCheckResponse])
def get_all_cert_checks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(CertificateCheck).offset(skip).limit(limit).all()


# Get single certificate check
@router.get("/{check_id}", response_model=CertificateCheckResponse)
def get_cert_check(check_id: int, db: Session = Depends(get_db)):
    cert = db.query(CertificateCheck).filter(CertificateCheck.id == check_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate check not found")
    return cert


# Update certificate check (if needed, by admin)
@router.put("/{check_id}", response_model=CertificateCheckResponse)
def update_cert_check(
    check_id: int, cert_data: CertificateCheckUpdate, db: Session = Depends(get_db)
):
    cert = db.query(CertificateCheck).filter(CertificateCheck.id == check_id).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate check not found")

    if cert_data.expiry_date is not None:
        cert.expiry_date = cert_data.expiry_date
    if cert_data.days_remaining is not None:
        cert.days_remaining = cert_data.days_remaining

    db.commit()
    db.refresh(cert)
    return cert
