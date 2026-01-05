from typing import List, Dict, Any

from backend.app.llm.provider import generate_llm_answer
from backend.app.rag.retriever import retrieve_documents


def build_prompt(
    query: str,
    documents: List[Dict[str, Any]],
    role: str | None = None,
) -> str:
    """
    Builds a grounded prompt using retrieved documents.
    """

    context_blocks = []
    for i, doc in enumerate(documents, start=1):
        context_blocks.append(
            f"[Source {i}]\n{doc['content']}"
        )

    context = "\n\n".join(context_blocks)

    system_instruction = (
        "You are a policy intelligence assistant for Ayushman Bharat.\n"
        "Answer ONLY using the provided sources.\n"
        "If the answer is not present in the sources, say so explicitly.\n"
        "Do not hallucinate or assume facts.\n"
    )

    if role:
        system_instruction += f"\nUser role/context: {role}\n"

    prompt = f"""
{system_instruction}

Context:
{context}

Question:
{query}

Answer (with references to source numbers):
"""

    return prompt.strip()


def answer_query(
    query: str,
    role: str | None = None,
    top_k: int = 3,
) -> Dict[str, Any]:
    """
    End-to-end RAG pipeline:
    1. Retrieve documents
    2. Build grounded prompt
    3. Call LLM provider
    4. Return answer + sources
    """

    # 1. Retrieve
    documents = retrieve_documents(query=query, top_k=top_k)

    if not documents:
        return {
            "answer": "No relevant policy documents were found for this query.",
            "sources": [],
        }

    # 2. Prompt
    prompt = build_prompt(
        query=query,
        documents=documents,
        role=role,
    )

    # 3. LLM call (provider-abstracted)
    try:
        answer = generate_llm_answer(prompt)
    except Exception:
        # Graceful degradation (NO crash)
        return {
            "answer": "The language model is temporarily unavailable. Please try again later.",
            "sources": [],
        }

    # 4. Return structured response
    return {
        "answer": answer,
        "sources": [
            {
                "id": i + 1,
                "metadata": doc.get("metadata", {}),
            }
            for i, doc in enumerate(documents)
        ],
    }
