import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    JWT_ALGORITHM: str = "HS256"

    # Provider selection
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")

settings = Settings()
# LLM
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")

# Groq
GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
GROQ_MODEL: str = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant"  # ✅ currently supported
)

# OpenAI (optional fallback)
OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL: str = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini"
)
