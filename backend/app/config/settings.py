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
