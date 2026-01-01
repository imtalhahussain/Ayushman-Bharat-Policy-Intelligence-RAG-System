from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from backend.app.services.auth_service import authenticate_user
from backend.app.services.security import create_access_token
from backend.app.schemas.auth import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        email=form_data.username,
        password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}
