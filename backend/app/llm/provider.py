from backend.app.config.settings import settings

def generate_text(prompt: str) -> str:
    provider = settings.LLM_PROVIDER.lower()

    try:
        if provider == "groq":
            return _groq(prompt)
        elif provider == "mock":
            return "LLM temporarily unavailable. This is a safe fallback response."
        else:
            raise ValueError("Unknown LLM provider")
    except Exception:
        return "The language model is temporarily unavailable. Please try again later."


def _groq(prompt: str) -> str:
    from groq import Groq

    client = Groq(api_key=settings.GROQ_API_KEY)

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content
