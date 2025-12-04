
# backend/app/api/routes_auth.py

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/ping")
def auth_ping():
    return {"message": "auth router is alive"}
