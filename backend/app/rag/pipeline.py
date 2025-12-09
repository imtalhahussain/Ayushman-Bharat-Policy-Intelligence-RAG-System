from typing import List, Dict, Literal

import chromadb
from sentence_transformers import SentenceTransformer

from backend.app.rag.prompts import build_rag_prompt
from backend.app.rag.llm_client import generate_answer
from backend.app.rag.vector_store import CHROMA_DIR


Role = Literal["citizen", "doctor", "hospital_admin", "policy_maker"]

# Load embedding model once at module import
_embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Connect to the same Chroma DB used during ingestion
_chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
_collection = _chroma_client.get_or_create_collection("ayushman_policies")


def _retrieve(query: str, top_k: int = 3) -> List[Dict]:
    """
    Run semantic search in Chroma and return a list of chunks:
    [{source, page_start, page_end, text}, ...]
    """
    # Embed the query using the same model as ingestion
    query_emb = _embedding_model.encode([query]).tolist()

    res = _collection.query(
        query_embeddings=query_emb,
        n_results=top_k,
    )

    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]

    chunks: List[Dict] = []
    for text, meta in zip(docs, metas):
        chunks.append(
            {
                "source": meta.get("source", meta.get("doc_id", "unknown")),
                "page_start": int(meta.get("page_start", meta.get("page", 0))),
                "page_end": int(meta.get("page_end", meta.get("page", 0))),
                "text": text,
            }
        )
    return chunks


def answer_query(query: str, role: Role = "citizen", top_k: int = 3) -> Dict:
    """
    High-level RAG function:
    - retrieve top_k chunks
    - build role-aware prompt
    - call LLM
    - return answer + sources
    """
    chunks = _retrieve(query, top_k=top_k)
    prompt = build_rag_prompt(query=query, role=role, docs=chunks)
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": chunks,
    }
