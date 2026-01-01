import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    JWT_SECRET: str | None = os.getenv("JWT_SECRET", "dev-secret-change-me")


settings = Settings()
