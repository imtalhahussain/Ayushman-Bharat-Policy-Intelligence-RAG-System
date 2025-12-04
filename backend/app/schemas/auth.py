from pydantic import BaseModel, EmailStr
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: Literal["citizen", "doctor", "hospital_admin", "policy_maker"] = "citizen"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
