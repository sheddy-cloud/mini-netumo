from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from api.database import get_db
from ..models.models import DomainCheck, Target, User
from ..schemas.domain_check import DomainCheckCreate, DomainCheckResponse, DomainCheckUpdate
from api.utils.security import get_current_user

router = APIRouter(prefix="/domainchecks", tags=["Domain Checks"])

# Helper function ku-check kama target ni ya current user
def verify_target_owner(target_id: int, user: User, db: Session):
    target = db.query(Target).filter(Target.id == target_id, Target.user_id == user.id).first()
    if not target:
        raise HTTPException(status_code=403, detail="Not authorized to access this target")
    return target

# Create domain check (by machine/user)
@router.post("/", response_model=DomainCheckResponse)
def create_domain_check(check: DomainCheckCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Verify target belongs to current user
    verify_target_owner(check.target_id, current_user, db)

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

# Get all domain checks (for current user only)
@router.get("/", response_model=List[DomainCheckResponse])
def get_domain_checks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Get all DomainChecks where the Target.user_id == current_user.id
    domain_checks = (
        db.query(DomainCheck)
        .join(Target, DomainCheck.target_id == Target.id)
        .filter(Target.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return domain_checks

# Get single domain check (only if belongs to current user)
@router.get("/{check_id}", response_model=DomainCheckResponse)
def get_domain_check(check_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_check = (
        db.query(DomainCheck)
        .join(Target, DomainCheck.target_id == Target.id)
        .filter(DomainCheck.id == check_id, Target.user_id == current_user.id)
        .first()
    )
    if not db_check:
        raise HTTPException(status_code=404, detail="Domain check not found")
    return db_check


# Update domain check (admin only if needed)
@router.put("/{check_id}", response_model=DomainCheckResponse)
def update_domain_check(check_id: int, check: DomainCheckUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_check = (
        db.query(DomainCheck)
        .join(Target, DomainCheck.target_id == Target.id)
        .filter(DomainCheck.id == check_id, Target.user_id == current_user.id)
        .first()
    )
    if not db_check:
        raise HTTPException(status_code=404, detail="Domain check not found")

    if check.expiry_date is not None:
        db_check.expiry_date = check.expiry_date
    if check.days_remaining is not None:
        db_check.days_remaining = check.days_remaining

    db.commit()
    db.refresh(db_check)
    return db_check
