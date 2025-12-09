from fastapi import APIRouter
from backend.app.schemas.chat import ChatRequest, ChatResponse, SourceChunk
from backend.app.rag.pipeline import answer_query

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
def ask_question(payload: ChatRequest) -> ChatResponse:
    """
    RAG endpoint:
    - Takes query + top_k + role
    - Returns LLM answer + retrieved sources
    """
    result = answer_query(
        query=payload.query,
        role=payload.role,
        top_k=payload.top_k,
    )

    sources = [
        SourceChunk(
            source=s["source"],
            page_start=s["page_start"],
            page_end=s["page_end"],
            text=s["text"],
        )
        for s in result["sources"]
    ]

    return ChatResponse(
        answer=result["answer"],
        sources=sources,
    )
