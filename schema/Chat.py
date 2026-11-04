
import os
import time
import requests

from pathlib import Path
from dotenv import load_dotenv
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates

from schema.Listemodel import lister_modeles

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
URL = os.getenv(
    "OPENROUTER_ROUTER",
    "https://openrouter.ai/api/v1/chat/completions",
)

Chat_route = APIRouter(
    prefix="/Chatebot",
    tags=["DiscutionsChat"],
)

templates = Jinja2Templates(
    directory=str(
        Path(__file__).resolve().parent.parent / "templates"
    )
)


@Chat_route.post("/chat")
def chat(
    request: Request,
    question: str = Form(...),
    model: str = Form(...),
):
    modeles = lister_modeles()["modeles"]

    reponse_ia = ""
    erreur = ""

    if not API_KEY:
        erreur = "La clé API OpenRouter est manquante."

    else:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant pédagogique spécialisé "
                        "en intelligence artificielle. "
                        "Réponds toujours en français avec des "
                        "explications simples et des exemples."
                    ),
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
            "temperature": 0.2,
            "max_tokens": 1000,
        }

        debut = time.perf_counter()

        try:
            response = requests.post(
                URL,
                headers=headers,
                json=data,
                timeout=60,
            )

            response.raise_for_status()

            resultat = response.json()
            choices = resultat.get("choices", [])

            if not choices:
                raise ValueError(
                    "OpenRouter n'a renvoyé aucun résultat."
                )

            premier_choix = choices[0]
            message_ia = premier_choix.get("message") or {}
            contenu = message_ia.get("content")

            if isinstance(contenu, str):
                reponse_ia = contenu

            elif isinstance(contenu, list):
                reponse_ia = "\n".join(
                    element["text"]
                    for element in contenu
                    if isinstance(element, dict)
                    and isinstance(element.get("text"), str)
                )

            if not reponse_ia.strip():
                raison = premier_choix.get("finish_reason")
                raise ValueError(
                    f"Le modèle n'a pas produit de texte. "
                    f"Raison : {raison}"
                )

            duree = round(
                time.perf_counter() - debut, 2
            )

            print(f"Temps de réponse : {duree} secondes")

        except requests.Timeout:
            erreur = "OpenRouter n'a pas répondu dans les 60 secondes."

        except requests.RequestException as exc:
            print("Erreur OpenRouter :", repr(exc))
            erreur = "Impossible de communiquer avec OpenRouter."

        except (ValueError, KeyError, IndexError, TypeError) as exc:
            print("Erreur de réponse :", repr(exc))
            erreur = str(exc)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "modeles": modeles,
            "question": question,
            "reponse": reponse_ia,
            "erreur": erreur,
            "modele_choisi": model,
        },
    )
