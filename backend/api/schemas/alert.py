# backend/api/schemas/alert.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AlertBase(BaseModel):
    user_id: int
    type: str
    message: str


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    type: Optional[str] = None
    message: Optional[str] = None


class AlertResponse(AlertBase):
    id: int
    sent_at: datetime
    model_config = ConfigDict(from_attributes=True)
