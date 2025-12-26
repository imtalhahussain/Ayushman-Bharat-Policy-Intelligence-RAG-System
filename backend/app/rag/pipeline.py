from backend.app.rag.llm_client import generate_answer

def answer_query(query: str, role: str, top_k: int):
    prompt = f"You are a {role}. Answer based on policy context.\n\nQuestion: {query}"
    answer = generate_answer(prompt)
    return {
        "answer": answer,
        "sources": [],
    }
