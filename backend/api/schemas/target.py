# backend/api/schemas/target.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class TargetCreate(BaseModel):
    url: HttpUrl
    check_interval: int
    enabled: bool


class TargetUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    check_interval: Optional[int] = None
    enabled: Optional[bool] = None


class TargetResponse(BaseModel):
    id: int
    user_id: int
    url: HttpUrl
    check_interval: int
    enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True
