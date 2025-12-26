from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from backend.app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def create_access_token(sub: str):
    payload = {
        "sub": sub,
        "exp": datetime.utcnow() + timedelta(hours=12),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
