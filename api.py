# File: api.py
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def query_groq(prompt: str, model: str = None) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment or .env file.")

    try:
        client = Groq(api_key=api_key)
        model = model or "llama3-groq-70b-8192-tool-use-preview"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=model,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error querying Groq: {e}")

