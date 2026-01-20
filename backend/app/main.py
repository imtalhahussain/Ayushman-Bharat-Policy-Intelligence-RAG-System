from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.routes_auth import router as auth_router
from backend.app.api.routes_chat import router as chat_router
from backend.app.db.session import engine
from backend.app.db.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ayushman Bharat RAG")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
