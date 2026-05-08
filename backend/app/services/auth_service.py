from sqlalchemy.orm import Session
from backend.app.db.session import SessionLocal
from backend.app.db.models import User
from backend.app.schemas.auth import UserCreate
from backend.app.services.security import get_password_hash, verify_password




# ---------- DB session helper ----------
# ---------- Create user ----------
def create_user(db: Session, data: UserCreate):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ValueError("User already exists")

    user = User(
        email=data.email,
        name=data.name or data.email.split('@')[0],
        role=data.role,
        hashed_password=get_password_hash(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------- Authenticate user ----------
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
