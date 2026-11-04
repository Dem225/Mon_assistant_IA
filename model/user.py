from pydantic import BaseModel, Field
from enum import Enum


class ModeleIA(str, Enum):
    openrouter_free = "openrouter/free"
    modele_exemple = "openai/gpt-4o-mini"


# 4. Définir les données reçues
class MessageRequest(BaseModel):
    question: str
    model: str
    temperature: float = Field(default=0.2, ge=0, le=2)
    max_tokens: int = Field(default=300, ge=1, le=2000)






# 5. Définir les données renvoyées
class MessageResponse(BaseModel):
    question: str
    reponse: str
    statut: str
    temps_reponse: float
    tokens_entree: int | None = None
    tokens_sortie: int | None = None
    tokens_total: int | None = None





class SourceInfo(BaseModel):
    source: str
    page: int
    distance: float


class AskResponse(BaseModel):
    question: str
    reponse: str
    statut: str
    temps_reponse: float
    tokens_entree: int | None = None
    tokens_sortie: int | None = None
    tokens_total: int | None = None
    sources: list[SourceInfo]

