from pydantic import BaseModel
from typing import List, Optional


class SourceChunk(BaseModel):
    source: str
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    text: str


class ChatRequest(BaseModel):
    query: str
    top_k: int = 3


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]