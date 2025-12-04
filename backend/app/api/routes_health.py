from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/ready")
def ready():
    # Later: add real checks (DB, Chroma, etc.)
    return {"status": "ready"}
