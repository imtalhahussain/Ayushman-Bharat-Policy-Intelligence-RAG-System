import os
from pathlib import Path
from dotenv import dotenv_values

# Find project root (folder that contains backend/ and .env)
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = BASE_DIR / ".env"

# Load ONLY from this .env file (ignore system env)
file_values = dotenv_values(ENV_PATH)

class Settings:
    OPENAI_API_KEY: str | None = file_values.get("OPENAI_API_KEY")
    JWT_SECRET: str | None = file_values.get("JWT_SECRET", "dev-secret-change-me")

settings = Settings()
