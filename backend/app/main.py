# backend/app/main.py

from fastapi import FastAPI

from .api.routes_chat import router as chat_router
from .config import settings  # ✅ use new config

app = FastAPI(title="Ayushman Bharat Policy Intelligence RAG API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/check-key")
def check_key():
    # This will just tell us if the key is loaded, not show the key
    return {"key_loaded": bool(settings.OPENAI_API_KEY)}


# Mount chat routes
app.include_router(chat_router)
