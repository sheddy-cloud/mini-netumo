from datetime import datetime, timezone
from typing import List

from api.database import get_db
from api.utils.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.models import Alert, User
from ..schemas.alert import AlertCreate, AlertResponse, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("/", response_model=AlertResponse)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_alert = Alert(
        user_id=current_user.id,  # Set user from token, not from client input
        type=alert.type,
        message=alert.message,
        sent_at=datetime.now(timezone.utc),
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/", response_model=List[AlertResponse])
def get_alerts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alerts = db.query(Alert).filter(Alert.user_id == current_user.id).offset(skip).limit(limit).all()
    return alerts

@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user.id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.put("/{alert_id}", response_model=AlertResponse)
def update_alert(alert_id: int, alert: AlertUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_alert = db.query(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user.id).first()
    if not db_alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    if alert.type is not None:
        db_alert.type = alert.type
    if alert.message is not None:
        db_alert.message = alert.message

    db.commit()
    db.refresh(db_alert)
    return db_alert
