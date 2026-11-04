import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException
from model.user import *
from  fastapi  import APIRouter

# 1. Charger les variables du fichier .env
load_dotenv()

# 2. Récupérer la configuration OpenRouter
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL")

URL = os.getenv("OPENROUTER_ROUTER")

# 3. Créer l'application FastAPI

modem_route=APIRouter(prefix="/LISTEMODEL", tags=["MODEL"])



@modem_route.get("/models")
def lister_modeles():
    if not API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Clé API OpenRouter manquante.",
        )

    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers={
                "Authorization": f"Bearer {API_KEY}",
            },
            timeout=30,
        )

        response.raise_for_status()
        resultat = response.json()

        modeles = [
            {
                "id": modele["id"],
                "nom": modele["name"],
            }
            for modele in resultat.get("data", [])
        ]

        return {
            "nombre": len(modeles),
            "modeles": modeles,
        }

    except requests.RequestException as erreur:
        raise HTTPException(
            status_code=502,
            detail="Impossible de récupérer les modèles OpenRouter.",
        ) from erreur