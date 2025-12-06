# backend/app/api/routes_auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.schemas.auth import UserCreate, UserLogin, Token, UserOut
from backend.app.dependencies import get_db, get_current_user
from backend.app.services.auth_service import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Token)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    try:
        token = create_user(db, user_in)
        return Token(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_user_token_for_existing_user(user)  # we'll define below
    return Token(access_token=token)


def create_user_token_for_existing_user(user):
    from backend.app.services.security import create_access_token
    return create_access_token(subject=user.email)


@router.get("/me", response_model=UserOut)
def read_me(current_user=Depends(get_current_user)):
    return current_user
