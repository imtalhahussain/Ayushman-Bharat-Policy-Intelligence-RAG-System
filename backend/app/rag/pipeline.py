from backend.app.rag.llm_client import generate_answer

def answer_query(query: str, role: str | None = None, top_k: int = 3):
    prompt = f"""
You are an expert on Ayushman Bharat health policies.

Question:
{query}

Answer clearly and factually.
"""
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "sources": []  # sources added later when vector DB is plugged in
    }
