from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
