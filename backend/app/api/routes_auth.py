from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.services.auth_service import (
    authenticate_user,
    create_user,
)
from backend.app.services.security import create_access_token
from backend.app.schemas.auth import Token, UserCreate
from backend.app.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", status_code=201)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, payload)
    return {"message": "User created successfully"}


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}
