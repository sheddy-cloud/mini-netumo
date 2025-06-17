from datetime import datetime, timezone
from typing import List

from api.database import get_db
from api.models import StatusLog, Target, User
from api.utils.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..schemas.status_log import (StatusLogCreate, StatusLogResponse,
                                  StatusLogUpdate)

router = APIRouter(prefix="/statuslogs", tags=["Status Logs"])

@router.post("/", response_model=StatusLogResponse)
def create_status_log(
    log: StatusLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_log = StatusLog(
        target_id=log.target_id,
        status_code=log.status_code,
        response_time_ms=log.response_time_ms,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/", response_model=List[StatusLogResponse])
def get_status_logs(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Correct subquery using target_id
    subquery = select(Target.target_id).where(Target.user_id == current_user.id).scalar_subquery()

    logs = db.query(StatusLog).filter(StatusLog.target_id.in_(subquery)).offset(skip).limit(limit).all()
    return logs

@router.get("/{target_id}", response_model=List[StatusLogResponse])
def get_status_logs_by_target(
    target_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(StatusLog).filter(StatusLog.target_id == target_id).all()
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found for this target")
    return logs
