# backend/api/schemas/user.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True
