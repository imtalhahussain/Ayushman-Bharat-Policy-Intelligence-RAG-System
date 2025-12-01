from typing import Dict, Any, List

from .retrieve import retrieve_top_k


def build_naive_answer(query: str, chunks: List[Dict[str, Any]]) -> str:
    """
    For now: just stitch together relevant chunks.
    Later you will replace this with a real LLM call.
    """
    if not chunks:
        return "I could not find any relevant information for this query in the indexed Ayushman Bharat policies."

    intro = f"Here are relevant excerpts from Ayushman Bharat / PM-JAY documents for your query:\n\n\"{query}\"\n\n"
    parts = []
    for i, ch in enumerate(chunks, start=1):
        src = ch.get("source")
        p1 = ch.get("page_start")
        p2 = ch.get("page_end")
        header = f"[{i}] Source: {src}, pages {p1}-{p2}"
        text = ch.get("text", "")
        snippet = text[:700] + ("..." if len(text) > 700 else "")
        parts.append(f"{header}\n{snippet}")

    return intro + "\n\n".join(parts)


def answer_query(query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Main RAG pipeline entry for the API.
    Returns { 'answer': str, 'sources': [...] }
    """
    chunks = retrieve_top_k(query, k=top_k)

    answer = build_naive_answer(query, chunks)

    sources = [
        {
            "source": ch.get("source"),
            "page_start": ch.get("page_start"),
            "page_end": ch.get("page_end"),
            "text": ch.get("text"),
        }
        for ch in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
