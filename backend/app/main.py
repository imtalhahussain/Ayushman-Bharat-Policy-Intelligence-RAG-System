from fastapi import FastAPI

from backend.app.api.routes_chat import router as chat_router
from backend.app.api.routes_health import router as health_router
from backend.app.api.routes_auth import router as auth_router  # if created

from backend.app.config import settings  # 👈 from config.py

app = FastAPI(title="Ayushman Bharat Policy Intelligence RAG API")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(chat_router)

@app.get("/check-key")
def check_key():
    return {"key_loaded": bool(settings.OPENAI_API_KEY)}
