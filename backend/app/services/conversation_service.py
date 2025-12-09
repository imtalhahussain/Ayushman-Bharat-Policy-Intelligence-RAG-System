from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
import json

from backend.app.db import models


def get_or_create_conversation(
    db: Session,
    user: models.User,
    role: str,
    conversation_id: Optional[int] = None,
) -> models.Conversation:
    if conversation_id is not None:
        conv = db.query(models.Conversation).filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user.id,
        ).first()
        if conv:
            return conv

    conv = models.Conversation(
        user_id=user.id,
        user_role=role,
        created_at=datetime.utcnow(),
        title=None,
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


def add_message(
    db: Session,
    conversation: models.Conversation,
    sender: str,
    text: str,
) -> models.Message:
    msg = models.Message(
        conversation_id=conversation.id,
        sender=sender,
        text=text,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def log_retrieval(
    db: Session,
    conversation: models.Conversation,
    query: str,
    top_k: int,
    chunks: List[dict],
    latency_ms: Optional[int] = None,
) -> models.RetrievalLog:
    # Store only lightweight metadata for now
    meta_list = [
        {
            "source": c.get("source"),
            "page_start": c.get("page_start"),
            "page_end": c.get("page_end"),
        }
        for c in chunks
    ]

    log = models.RetrievalLog(
        conversation_id=conversation.id,
        query=query,
        top_k=top_k,
        latency_ms=latency_ms,
        retrieved_sources=json.dumps(meta_list),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
