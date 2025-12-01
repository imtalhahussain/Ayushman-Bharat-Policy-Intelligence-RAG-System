from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/ready")
def ready():
    # Later: add checks for DB, Chroma, etc.
    return {"status": "ready"}
