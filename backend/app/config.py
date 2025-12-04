import os
from dotenv import load_dotenv

# Load variables from .env at startup
load_dotenv()

class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    JWT_SECRET: str | None = os.getenv("JWT_SECRET", "dev-secret-change-me")

settings = Settings()
