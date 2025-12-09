from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import time

from backend.app.schemas.chat import ChatRequest, ChatResponse, SourceChunk
from backend.app.rag.pipeline import answer_query
from backend.app.dependencies import get_db, get_current_user
from backend.app.db import models
from backend.app.services.conversation_service import (
    get_or_create_conversation,
    add_message,
    log_retrieval,
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/ask", response_model=ChatResponse)
def ask_question(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> ChatResponse:
    """
    Authenticated RAG endpoint:
    - Uses current_user from JWT
    - Creates/uses a conversation
    - Logs user & assistant messages
    - Logs retrieval metadata
    """

    # 1) Create a new conversation for now (later you can pass conv_id)
    conversation = get_or_create_conversation(
        db=db,
        user=current_user,
        role=payload.role or current_user.role,
        conversation_id=None,
    )

    # 2) Log user question as a message
    add_message(
        db=db,
        conversation=conversation,
        sender="user",
        text=payload.query,
    )

    # 3) Run RAG pipeline
    t0 = time.time()
    result = answer_query(
        query=payload.query,
        role=payload.role or current_user.role,
        top_k=payload.top_k,
    )
    latency_ms = int((time.time() - t0) * 1000)

    # 4) Log retrieval metadata
    log_retrieval(
        db=db,
        conversation=conversation,
        query=payload.query,
        top_k=payload.top_k,
        chunks=result["sources"],
        latency_ms=latency_ms,
    )

    # 5) Log assistant answer as a message
    add_message(
        db=db,
        conversation=conversation,
        sender="assistant",
        text=result["answer"],
    )

    # 6) Build response
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
