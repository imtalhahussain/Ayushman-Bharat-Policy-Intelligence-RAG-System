from backend.app.rag.retriever import retrieve_context
from backend.app.llm.provider import generate_llm_answer


def build_prompt(query: str, contexts: list[str], role: str) -> str:
    joined_context = "\n\n".join(contexts)

    return f"""
You are an expert assistant answering questions using ONLY the provided context.

Role: {role}

Context:
{joined_context}

Question:
{query}

Rules:
- If the answer is not in the context, say: "The information is not available in the provided documents."
- Do NOT hallucinate.
- Be concise and factual.
"""


def answer_query(query: str, role: str, top_k: int = 3):
    retrieved = retrieve_context(query, top_k)

    if not retrieved:
        return {
            "answer": "No relevant policy documents found.",
            "sources": [],
        }

    contexts = [r.content for r in retrieved]
    prompt = build_prompt(query, contexts, role)

    answer = generate_llm_answer(prompt)

    sources = [
        r.metadata.get("source", "unknown")
        for r in retrieved
    ]

    return {
        "answer": answer,
        "sources": list(set(sources)),
    }
