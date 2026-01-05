from typing import List, Dict
from backend.app.rag.vector_store import vectorstore


class RetrievalResult:
    def __init__(self, content: str, metadata: Dict):
        self.content = content
        self.metadata = metadata


def retrieve_context(query: str, top_k: int = 3) -> List[RetrievalResult]:
    """
    Retrieve top-k grounded chunks from vector store.
    No LLM involved here.
    """

    docs = vectorstore.similarity_search(
        query=query,
        k=top_k,
    )

    results: List[RetrievalResult] = []

    for doc in docs:
        results.append(
            RetrievalResult(
                content=doc.page_content,
                metadata=doc.metadata,
            )
        )

    return results
