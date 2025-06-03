# api/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from ..models import User
from api.utils import security  # file iliyo na hashing na jwt utils
from api.database import get_db  # function ya getting db session importation

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)
# for registration
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Angalia kama email imetumika
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password kabla ya ku-save
    hashed_password = security.hash_password(user.password)

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#for login
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Angalia kama user yupo
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Hakiki password
    if not security.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Tengeneza token
    access_token = security.create_access_token(data={"sub": str(db_user.id)})

    return {"access_token": access_token, "token_type": "bearer"}

# Hii route inalindwa, haiwezi kufikiwa bila token sahihi
@router.get("/me", response_model=UserResponse)
def read_profile(current_user: User = Depends(security.get_current_user)):
    return current_user