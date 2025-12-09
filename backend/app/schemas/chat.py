from typing import List, Literal
from pydantic import BaseModel


class SourceChunk(BaseModel):
    source: str
    page_start: int
    page_end: int
    text: str


class ChatRequest(BaseModel):
    query: str
    top_k: int = 3
    role: Literal["citizen", "doctor", "hospital_admin", "policy_maker"] = "citizen"


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
