from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    top_k: int = 3
    role: str | None = None

class ChatResponse(BaseModel):
    answer: str
    sources: list
