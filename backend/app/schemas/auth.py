from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None
    role: str = "user"


class Token(BaseModel):
    access_token: str
    token_type: str
