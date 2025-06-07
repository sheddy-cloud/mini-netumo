# backend/api/routers/target.py

from datetime import datetime, timezone
from typing import List

from api.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from scheduler import (cancel_target_jobs, schedule_cert_check,
                       schedule_target_monitoring)
from sqlalchemy.orm import Session

from ..models.models import Target, User
from ..schemas.target import TargetCreate, TargetResponse, TargetUpdate
from ..utils.security import get_current_user

router = APIRouter(
    prefix="/targets",
    tags=["Targets"]
)

# ✅ Create a target (owned by current user)
@router.post("/", response_model=TargetResponse)
def create_target(
    target_in: TargetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_target = Target(
        user_id=current_user.id,
        url=target_in.url,
        check_interval=5,
        enabled=1,
        name=target_in.name,
        created_at=datetime.now(timezone.utc),
    )
    db.add(db_target)
    db.commit()
    db.refresh(db_target)

    # Schedule monitoring jobs
    schedule_target_monitoring(db_target.target_id, db_target.url)
    schedule_cert_check(db_target.target_id, db_target.url)
    return db_target


# ✅ Read all targets (only those owned by current user)
@router.get("/", response_model=List[TargetResponse])
def read_targets(
    skip: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Target).filter(Target.user_id == current_user.id).offset(skip).all()


# ✅ Read one target by ID (only if owned)
@router.get("/{target_id}", response_model=TargetResponse)
def read_target(
    target_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_target = db.query(Target).filter(Target.target_id == target_id).first()
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    if db_target.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this target")
    return TargetResponse.from_orm(db_target)


# ✅ Update a target (only if owned)
@router.put("/{target_id}", response_model=TargetResponse)
def update_target(
    target_id: int,
    target_update: TargetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_target = db.query(Target).filter(Target.target_id == target_id).first()
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    if db_target.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this target")

    db_target.url = target_update.url if target_update.url is not None else db_target.url
    db_target.name = target_update.name if target_update.name is not None else db_target.name

    db.commit()
    db.refresh(db_target)
    return db_target

@router.delete("/{target_id}", status_code=204)
def delete_target(
    target_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_target = db.query(Target).filter(Target.target_id == target_id).first()
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    if db_target.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this target")

    # Cancel the scheduled jobs
    db.delete(db_target)
    db.commit()
    cancel_target_jobs(target_id)
    return None
