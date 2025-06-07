from datetime import datetime, timezone
from typing import List

from api.database import get_db
from api.utils.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.models import DomainCheck, Target, User
from ..schemas.domain_check import (DomainCheckCreate, DomainCheckResponse,
                                    DomainCheckUpdate)

router = APIRouter(prefix="/domainchecks", tags=["Domain Checks"])

# Helper function ku-check kama target ni ya current user
def verify_target_owner(target_id: int, user: User, db: Session):
    target = db.query(Target).filter(Target.target_id == target_id, Target.user_id == user.id).first()
    if not target:
        raise HTTPException(status_code=403, detail="Not authorized to access this target")
    return target



# Get all domain checks (for current user only)
@router.get("/", response_model=List[DomainCheckResponse])
def get_domain_checks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Get all DomainChecks where the Target.user_id == current_user.id
    domain_checks = (
        db.query(DomainCheck)
        .join(Target, DomainCheck.target_id == Target.target_id)
        .filter(Target.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return domain_checks

# Get single domain check (only if belongs to current user)
@router.get("/{target_id}", response_model=DomainCheckResponse)
def get_domain_check(target_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_check = (
        db.query(DomainCheck)
        .join(Target, DomainCheck.target_id == Target.target_id)
        .filter(Target.user_id == current_user.id)
        .first()
    )
    if not db_check:
        raise HTTPException(status_code=404, detail="Domain check not found")
    return DomainCheckResponse.from_orm(db_check)
