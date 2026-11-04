
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from schema.Listemodel import lister_modeles

interfaces_route = APIRouter(
    prefix="/Chatebot",
    tags=["DiscutionsChat"],
)

templates = Jinja2Templates(
    directory=str(
        Path(__file__).resolve().parent.parent / "templates"
    )
)


@interfaces_route.get("/interface")
def afficher_interface(request: Request):

    resultat = lister_modeles()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "modeles": resultat["modeles"],
            "question": "",
            "reponse": "",
            "erreur": "",
            "modele_choisi": "",
        },
    )
