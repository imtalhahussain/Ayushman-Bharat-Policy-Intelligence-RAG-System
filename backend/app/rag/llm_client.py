# backend/app/rag/llm_client.py

from openai import OpenAI
from backend.app.config import settings  # 👈 from config.py

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_answer(prompt: str) -> str:
    if not settings.OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set in environment")

    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # or your chosen model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return resp.choices[0].message.content.strip()
