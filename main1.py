import os
from dotenv import load_dotenv
from fastapi import FastAPI
from schema.Ask import Ask_route
from schema.Chat import Chat_route
from schema.Listemodel import modem_route
from schema.Interfase import interfaces_route
# 1. Charger les variables du fichier .env
load_dotenv()

# 2. Récupérer la configuration OpenRouter
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL")

URL = os.getenv("OPENROUTER_ROUTER")


app = FastAPI()


app.include_router(Ask_route)
app.include_router(modem_route)
app.include_router(Chat_route)
app.include_router(interfaces_route)