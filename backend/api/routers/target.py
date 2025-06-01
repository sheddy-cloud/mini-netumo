# backend/api/routers/target.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone

from api.database import get_db
from ..models.models import Target
from ..schemas.target import TargetCreate, TargetUpdate, TargetResponse

router = APIRouter(
    prefix="/targets",
    tags=["Targets"]
)

# Create a target
@router.post("/", response_model=TargetResponse)
def create_target(target_in: TargetCreate, db: Session = Depends(get_db)):
    db_target = Target(
        user_id=target_in.user_id,
        url=target_in.url,
        check_interval=target_in.check_interval,
        enabled=target_in.enabled,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_target)
    db.commit()
    db.refresh(db_target)
    return db_target

# Read all targets
@router.get("/", response_model=List[TargetResponse])
def read_targets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Target).offset(skip).limit(limit).all()

# Read one target by ID
@router.get("/{target_id}", response_model=TargetResponse)
def read_target(target_id: int, db: Session = Depends(get_db)):
    db_target = db.query(Target).filter(Target.id == target_id).first()
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    return db_target

# Update a target
@router.put("/{target_id}", response_model=TargetResponse)
def update_target(target_id: int, target_update: TargetUpdate, db: Session = Depends(get_db)):
    db_target = db.query(Target).filter(Target.id == target_id).first()
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")

    db_target.url = target_update.url if target_update.url is not None else db_target.url
    db_target.check_interval = target_update.check_interval if target_update.check_interval is not None else db_target.check_interval
    db_target.enabled = target_update.enabled if target_update.enabled is not None else db_target.enabled

    db.commit()
    db.refresh(db_target)
    return db_target
