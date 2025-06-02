# backend/api/routers/user.py

from typing import List

from api.database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models.models import User
from ..schemas import user
from ..utils.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


# Create a new user
@router.post("/", response_model=user.UserResponse)
def create_user(user_in: user.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = hash_password(user_in.password)
    new_user = User(name=user_in.name, email=user_in.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Read all users
@router.get("/", response_model=List[user.UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


# View single user
@router.get("/{user_id}", response_model=user.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_obj = db.query(User).filter(User.id == user_id).first()
    if user_obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_obj


# Update user
@router.put("/{user_id}", response_model=user.UserResponse)
def update_user(
        user_id: int,
        user_in: user.UserUpdate,
        db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user_in.name is not None:
        db_user.name = user_in.name
    if user_in.email is not None:
        db_user.email = user_in.email

    db.commit()
    db.refresh(db_user)
    return db_user
