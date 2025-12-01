# backend/app/api/routes_chat.py

from fastapi import APIRouter
from ..schemas.chat import ChatRequest, ChatResponse, SourceChunk
from ..rag.pipeline import answer_query

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
def ask_question(payload: ChatRequest):
    result = answer_query(payload.query, top_k=payload.top_k)

    sources = [
        SourceChunk(
            source=src["source"],
            page_start=src["page_start"],
            page_end=src["page_end"],
            text=src["text"],
        )
        for src in result["sources"]
    ]

    return ChatResponse(
        answer=result["answer"],
        sources=sources,
    )
