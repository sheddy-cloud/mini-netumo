# backend/api/routers/status_log.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import List

from api.database import get_db
from ..models.models import StatusLog
from ..schemas.status_log import StatusLogCreate, StatusLogResponse, StatusLogUpdate

router = APIRouter(prefix="/statuslogs", tags=["Status Logs"])

# Create status log (by machine)
@router.post("/", response_model=StatusLogResponse)
def create_status_log(log: StatusLogCreate, db: Session = Depends(get_db)):
    db_log = StatusLog(
        target_id=log.target_id,
        status_code=log.status_code,
        response_time_ms=log.response_time_ms,
        timestamp=datetime.now(timezone.utc)
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# Get all logs
@router.get("/", response_model=List[StatusLogResponse])
def get_status_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(StatusLog).offset(skip).limit(limit).all()

# Get single log
@router.get("/{log_id}", response_model=StatusLogResponse)
def get_status_log(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(StatusLog).filter(StatusLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Status log not found")
    return db_log

# Update log (optional for admin)
@router.put("/{log_id}", response_model=StatusLogResponse)
def update_status_log(log_id: int, log: StatusLogUpdate, db: Session = Depends(get_db)):
    db_log = db.query(StatusLog).filter(StatusLog.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Status log not found")

    if log.status_code is not None:
        db_log.status_code = log.status_code
    if log.response_time_ms is not None:
        db_log.response_time_ms = log.response_time_ms

    db.commit()
    db.refresh(db_log)
    return db_log
