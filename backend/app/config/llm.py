import os

class LLMConfig:
    """
    Centralized LLM runtime configuration.
    Change models/providers here without touching business logic.
    """

    PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")

    # Groq-specific
    GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
    MODEL: str = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")

    # Runtime controls
    TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "512"))

llm_config = LLMConfig()
