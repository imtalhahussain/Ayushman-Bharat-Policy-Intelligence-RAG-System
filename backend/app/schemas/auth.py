from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: Literal["citizen", "doctor", "hospital_admin", "policy_maker"] = "citizen"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str

    model_config = ConfigDict(from_attributes=True)

