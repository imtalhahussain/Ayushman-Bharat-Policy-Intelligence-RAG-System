import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Auth
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    JWT_ALGORITHM: str = "HS256"

    # LLM (Groq)
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama3-8b")

settings = Settings()
