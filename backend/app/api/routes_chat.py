from fastapi import APIRouter, Depends
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.rag.pipeline import answer_query
from backend.app.dependencies import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/ask", response_model=ChatResponse)
def ask(payload: ChatRequest, user=Depends(get_current_user)):
    return answer_query(
        query=payload.query,
        role=payload.role,
        top_k=payload.top_k,
    )
