from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.schemas.auth import UserCreate, Token
from backend.app.db.session import SessionLocal
from backend.app.services.auth_service import create_user
from backend.app.services.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
def signup(user: UserCreate):
    db = SessionLocal()
    create_user(db, user.email, user.name, user.password, user.role)
    return {"status": "created"}

@router.post("/login", response_model=Token)
def login(email: str, password: str):
    token = create_access_token(email)
    return {"access_token": token}
