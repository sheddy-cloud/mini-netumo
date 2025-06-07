# backend/api/schemas/status_log.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StatusLogBase(BaseModel):
    target_id: int
    status_code: int
    response_time_ms: float


class StatusLogCreate(StatusLogBase):
    pass


class StatusLogUpdate(BaseModel):
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None



class StatusLogResponse(BaseModel):
    log_id: int
    target_id: Optional[int] = None
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    timestamp: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)
