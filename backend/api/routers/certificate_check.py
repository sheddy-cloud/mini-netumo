from datetime import datetime, timezone
from typing import List

from api.database import get_db
from api.utils.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.models import CertificateCheck, Target, User
from ..schemas.certificate_check import (CertificateCheckCreate,
                                         CertificateCheckResponse,
                                         CertificateCheckUpdate)

router = APIRouter(prefix="/certificatechecks", tags=["Certificate Checks"])

def verify_target_owner(target_id: int, user: User, db: Session):
    target = db.query(Target).filter(Target.target_id == target_id, Target.user_id == user.id).first()
    if not target:
        raise HTTPException(status_code=403, detail="Not authorized to access this target")
    return target


@router.get("/", response_model=List[CertificateCheckResponse])
def get_all_cert_checks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cert_checks = (
        db.query(CertificateCheck)
        .join(Target, CertificateCheck.target_id == Target.target_id)
        .filter(Target.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return cert_checks

@router.get("/{target_id}", response_model=CertificateCheckResponse)
def get_cert_check(target_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cert = (
        db.query(CertificateCheck)
        .join(Target, CertificateCheck.target_id == Target.target_id)
        .filter(Target.user_id == current_user.id)
        .first()
    )
    if not cert:
        raise HTTPException(
            status_code=404, detail="Certificate check not found"
        )
    return CertificateCheckResponse.from_orm(cert)
