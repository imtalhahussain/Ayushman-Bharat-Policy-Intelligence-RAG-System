from groq import Groq
from backend.app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # fast + high quality
        messages=[
            {"role": "system", "content": "You are a helpful policy assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
