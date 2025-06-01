# backend/api/routers/domain_check.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from api.database import get_db
from ..models.models import DomainCheck
from ..schemas.domain_check import (
    DomainCheckCreate,
    DomainCheckResponse,
    DomainCheckUpdate,
)

router = APIRouter(prefix="/domainchecks", tags=["Domain Checks"])


# Create domain check (by machine)
@router.post("/", response_model=DomainCheckResponse)
def create_domain_check(check: DomainCheckCreate, db: Session = Depends(get_db)):
    db_check = DomainCheck(
        target_id=check.target_id,
        expiry_date=check.expiry_date,
        days_remaining=check.days_remaining,
        checked_at=datetime.now(timezone.utc),
    )
    db.add(db_check)
    db.commit()
    db.refresh(db_check)
    return db_check


# Get all domain checks
@router.get("/", response_model=List[DomainCheckResponse])
def get_domain_checks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(DomainCheck).offset(skip).limit(limit).all()


# Get single domain check
@router.get("/{check_id}", response_model=DomainCheckResponse)
def get_domain_check(check_id: int, db: Session = Depends(get_db)):
    db_check = db.query(DomainCheck).filter(DomainCheck.id == check_id).first()
    if not db_check:
        raise HTTPException(status_code=404, detail="Domain check not found")
    return db_check


# Update domain check (admin only if needed)
@router.put("/{check_id}", response_model=DomainCheckResponse)
def update_domain_check(
    check_id: int, check: DomainCheckUpdate, db: Session = Depends(get_db)
):
    db_check = db.query(DomainCheck).filter(DomainCheck.id == check_id).first()
    if not db_check:
        raise HTTPException(status_code=404, detail="Domain check not found")

    if check.expiry_date is not None:
        db_check.expiry_date = check.expiry_date
    if check.days_remaining is not None:
        db_check.days_remaining = check.days_remaining

    db.commit()
    db.refresh(db_check)
    return db_check
