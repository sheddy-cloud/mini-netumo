# backend/api/routers/alert.py

from datetime import datetime, timezone
from typing import List

from api.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.models import Alert
from ..schemas.alert import AlertCreate, AlertResponse, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])


# Create alert (machine/system)
@router.post("/", response_model=AlertResponse)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    db_alert = Alert(
        user_id=alert.user_id,
        type=alert.type,
        message=alert.message,
        sent_at=datetime.now(timezone.utc),
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


# Get all alerts
@router.get("/", response_model=List[AlertResponse])
def get_alerts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    alerts = db.query(Alert).offset(skip).limit(limit).all()
    return alerts


# Get a specific alert by ID
@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


# Update an alert (by admin if necessary)
@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(
    alert_id: int, alert: AlertUpdate, db: Session = Depends(get_db)
):
    db_alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    if alert.type is not None:
        db_alert.type = alert.type
    if alert.message is not None:
        db_alert.message = alert.message

    db.commit()
    db.refresh(db_alert)
    return db_alert
