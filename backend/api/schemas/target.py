# backend/api/schemas/target.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class TargetCreate(BaseModel):
    url: str
    name: str


class TargetUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    name: Optional[str] = None


class TargetResponse(BaseModel):
    target_id: int
    user_id: int
    url: str
    check_interval: int
    enabled: bool
    created_at: datetime
    name: str
    model_config = ConfigDict(from_attributes=True)
