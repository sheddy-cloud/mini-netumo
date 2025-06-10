# backend/api/schemas/domain_check.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DomainCheckBase(BaseModel):
    target_id: int
    expiry_date: datetime
    days_remaining: int


class DomainCheckCreate(DomainCheckBase):
    pass


class DomainCheckUpdate(BaseModel):
    expiry_date: Optional[datetime] = None
    days_remaining: Optional[int] = None


class DomainCheckResponse(BaseModel):
    domain_id: int
    target_id: int
    expiry_date: Optional[datetime]
    days_remaining: Optional[int]
    checked_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
