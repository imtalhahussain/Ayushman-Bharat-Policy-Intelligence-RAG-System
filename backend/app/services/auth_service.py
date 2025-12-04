# backend/app/services/auth_service.py

from sqlalchemy.orm import Session

from backend.app.db import models
from backend.app.schemas.auth import UserCreate
from backend.app.services.security import hash_password, create_access_token
from backend.app.logging_config import logger

def create_user(db: Session, user_in: UserCreate) -> str:
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise ValueError("User already exists")

    hashed = hash_password(user_in.password)
    user = models.User(
        email=user_in.email,
        name=user_in.name,
        role=user_in.role,
        hashed_password=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"Created user {user.email} with role {user.role}")
    token = create_access_token(subject=user.email)
    return token
