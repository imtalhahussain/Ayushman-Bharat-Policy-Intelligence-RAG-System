import os
from groq import Groq
from backend.app.config.llm import llm_config

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=llm_config.MODEL,
            messages=[
                {"role": "system", "content": "You are a policy intelligence assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=llm_config.TEMPERATURE,
            max_tokens=llm_config.MAX_TOKENS,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        # HARD rule: never crash the API due to LLM issues
        print(f"[LLM ERROR] {e}")
        return "The language model is temporarily unavailable. Please try again later."
