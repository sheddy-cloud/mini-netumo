# backend/api/schemas/status_log.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StatusLogBase(BaseModel):
    target_id: int
    status_code: int
    response_time_ms: float

class StatusLogCreate(StatusLogBase):
    pass

class StatusLogUpdate(BaseModel):
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None

class StatusLogResponse(StatusLogBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
