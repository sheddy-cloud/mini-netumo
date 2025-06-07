# backend/api/schemas/target.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl


class TargetCreate(BaseModel):
    url: HttpUrl
    name: str


class TargetUpdate(BaseModel):
    url: Optional[HttpUrl] = None
    name: Optional[str] = None


class TargetResponse(BaseModel):
    target_id: int
    user_id: int
    url: HttpUrl
    check_interval: int
    enabled: bool
    created_at: datetime
    name: str

    class Config:
        orm_mode = True
