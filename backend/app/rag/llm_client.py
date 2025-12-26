from openai import OpenAI
from backend.app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_answer(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.choices[0].message.content
