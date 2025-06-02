# backend/api/schemas/certificate_check.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CertificateCheckBase(BaseModel):
    target_id: int
    expiry_date: datetime
    days_remaining: int


class CertificateCheckCreate(CertificateCheckBase):
    pass


class CertificateCheckUpdate(BaseModel):
    expiry_date: Optional[datetime] = None
    days_remaining: Optional[int] = None


class CertificateCheckResponse(CertificateCheckBase):
    id: int
    checked_at: datetime

    class Config:
        from_attributes = True
