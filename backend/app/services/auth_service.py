from sqlalchemy.orm import Session
from backend.app.db.session import SessionLocal
from backend.app.db.models import User
from backend.app.schemas.auth import UserCreate
from backend.app.services.security import get_password_hash, verify_password




# ---------- DB session helper ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Create user ----------
def create_user(data: UserCreate):
    db: Session = next(get_db())

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise ValueError("User already exists")

    user = User(
        email=data.email,
        name=data.name,
        role=data.role,
        hashed = get_password_hash(data.password)

    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------- Authenticate user ----------
def authenticate_user(email: str, password: str):
    db: Session = next(get_db())

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
