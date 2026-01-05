from typing import Optional, Any
from backend.app.config.settings import settings

# --- Provider imports (runtime-safe) ---
try:
    from groq import Groq
except Exception:
    Groq = None

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class LLMUnavailableError(Exception):
    """Raised when no LLM provider is available."""


def _get_groq_client() -> Optional[Any]:
    if not settings.GROQ_API_KEY or not Groq:
        return None
    return Groq(api_key=settings.GROQ_API_KEY)


def _get_openai_client() -> Optional[Any]:
    if not settings.OPENAI_API_KEY or not OpenAI:
        return None
    return OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_llm_answer(prompt: str) -> str:
    """
    Provider-agnostic LLM call.
    Priority:
    1. Configured provider
    2. Automatic fallback
    """

    provider = settings.LLM_PROVIDER.lower()

    if provider == "groq":
        try:
            return _call_groq(prompt)
        except Exception:
            return _call_openai(prompt)

    if provider == "openai":
        try:
            return _call_openai(prompt)
        except Exception:
            return _call_groq(prompt)

    # Last-resort fallback
    for fn in (_call_groq, _call_openai):
        try:
            return fn(prompt)
        except Exception:
            continue

    raise LLMUnavailableError("No LLM provider available")


# ---------------- PROVIDERS ---------------- #

def _call_groq(prompt: str) -> str:
    client = _get_groq_client()
    if not client:
        raise LLMUnavailableError("Groq client unavailable")

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a factual policy assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=800,
    )

    return response.choices[0].message.content.strip()


def _call_openai(prompt: str) -> str:
    client = _get_openai_client()
    if not client:
        raise LLMUnavailableError("OpenAI client unavailable")

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a factual policy assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=800,
    )

    return response.choices[0].message.content.strip()
