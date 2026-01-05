from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt

from backend.app.config.settings import settings

# ---------------- CONFIG ---------------- #

ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_HOURS = 12
MAX_BCRYPT_BYTES = 72

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# ---------------- PASSWORD UTILS ---------------- #

def _normalize_password(password: str) -> str:
    """
    bcrypt hard limit is 72 bytes.
    Normalize consistently for hash + verify.
    """
    return (
        password.encode("utf-8")[:MAX_BCRYPT_BYTES]
        .decode("utf-8", errors="ignore")
    )


def get_password_hash(password: str) -> str:
    password = _normalize_password(password)
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    password = _normalize_password(password)
    return pwd_context.verify(password, hashed_password)

# ---------------- JWT UTILS ---------------- #

def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create JWT access token.
    """
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=ALGORITHM,
    )
