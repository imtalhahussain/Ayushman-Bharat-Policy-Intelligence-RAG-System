from pydantic import BaseModel, EmailStr
from typing import Literal


# ---------- Request Schemas ----------

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: Literal["citizen", "doctor", "hospital_admin"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ---------- Response Schemas ----------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

    class Config:
        from_attributes = True
