from fastapi import FastAPI
from backend.app.api.routes_auth import router as auth_router
from backend.app.api.routes_chat import router as chat_router
from backend.app.db.session import engine
from backend.app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ayushman Bharat RAG")

app.include_router(auth_router)
app.include_router(chat_router)
