import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(prompt: str) -> str:
    """
    Simple wrapper to call an LLM with a text prompt.
    Adjust model name to what you actually have access to.
    """
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is not set in environment.")

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or any other available chat model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()
