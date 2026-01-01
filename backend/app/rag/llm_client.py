from groq import Groq
from backend.app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expert assistant for Ayushman Bharat health policies. Answer factually."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=512,
    )

    return response.choices[0].message.content
