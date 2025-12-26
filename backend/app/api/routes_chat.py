from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.dependencies import get_db, get_current_user
from backend.app.rag.pipeline import answer_query

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/ask", response_model=ChatResponse)
def ask(payload: ChatRequest, user=Depends(get_current_user)):
    result = answer_query(payload.query, payload.role, payload.top_k)
    return result
