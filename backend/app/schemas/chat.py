from pydantic import BaseModel
from typing import List

class ChatRequest(BaseModel):
    query: str
    top_k: int = 3
    role: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[dict]
