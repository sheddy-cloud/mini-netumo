# backend/api/schemas/domain_check.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DomainCheckBase(BaseModel):
    target_id: int
    expiry_date: datetime
    days_remaining: int


class DomainCheckCreate(DomainCheckBase):
    pass


class DomainCheckUpdate(BaseModel):
    expiry_date: Optional[datetime] = None
    days_remaining: Optional[int] = None


class DomainCheckResponse(DomainCheckBase):
    id: int
    checked_at: datetime

    class Config:
        from_attributes = True
