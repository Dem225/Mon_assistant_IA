import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL")

URL = "https://openrouter.ai/api/v1/chat/completions"
def poser_question(question: str) -> str:
    if not API_KEY or not MODEL:
        raise ValueError("Configure OPENROUTER_API_KEY et OPENROUTER_MODEL dans .env")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ],
    }

    response = requests.post(
        URL,
        headers=headers,
        json=data,
        timeout=60,
    )

    response.raise_for_status()

    resultat = response.json()

    return resultat["choices"][0]["message"]["content"]


if __name__ == "__main__":
    question = "Explique-moi ce qu'est un token en intelligence artificielle."

    reponse = poser_question(question)

    print("Question :", question)
    print("Réponse :", reponse)