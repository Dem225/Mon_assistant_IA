
from pathlib import Path

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


def extraire_et_decouper(
    chemin_pdf: str,
    taille: int = 350,
    chevauchement: int = 50,
) -> list[dict]:
    """
    Extrait le texte d'un PDF et le découpe en passages.
    Chaque passage conserve sa source et son numéro de page.
    """

    if taille <= 0:
        raise ValueError("La taille doit être positive.")

    if chevauchement < 0 or chevauchement >= taille:
        raise ValueError(
            "Le chevauchement doit être positif et inférieur à la taille."
        )

    chemin = Path(chemin_pdf)

    if not chemin.is_file():
        raise FileNotFoundError(f"PDF introuvable : {chemin}")

    lecteur = PdfReader(str(chemin))
    passages = []
    pas = taille - chevauchement

    for numero_page, page in enumerate(lecteur.pages, start=1):
        texte = page.extract_text() or ""
        mots = texte.split()

        if not mots:
            continue

        for debut in range(0, len(mots), pas):
            morceaux = mots[debut : debut + taille]

            if not morceaux:
                continue

            passages.append({
                "texte": " ".join(morceaux),
                "source": chemin.name,
                "page": numero_page,
            })

    return passages


# Charger le modèle multilingue d'embeddings
modele = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

# Créer ou ouvrir la base ChromaDB persistante
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="reglement_horizon",
    metadata={"hnsw:space": "cosine"},
)


def indexer_pdf(chemin_pdf: str) -> int:
    """Extrait, vectorise et enregistre les passages d'un PDF."""

    passages = extraire_et_decouper(chemin_pdf)

    if not passages:
        return 0

    textes = [passage["texte"] for passage in passages]

    vecteurs = modele.encode(
        textes,
        normalize_embeddings=True,
    ).tolist()

    ids = [
        f"{passage['source']}-passage-{i}"
        for i, passage in enumerate(passages)
    ]

    metadonnees = [
        {
            "source": passage["source"],
            "page": passage["page"],
        }
        for passage in passages
    ]

    collection.upsert(
        ids=ids,
        documents=textes,
        embeddings=vecteurs,
        metadatas=metadonnees,
    )

    return len(passages)



def rechercher_passages(question: str, nombre: int = 3) -> list[dict]:
    """Recherche les passages les plus pertinents pour une question."""

    if not question.strip():
        raise ValueError("La question ne peut pas être vide.")

    if nombre < 1:
        raise ValueError("Le nombre de passages doit être positif.")

    resultat = collection.query(
        query_embeddings=[
            modele.encode(
                question,
                normalize_embeddings=True,
            ).tolist()
        ],
        n_results=min(nombre, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    passages = []

    documents = resultat["documents"][0]
    metadonnees = resultat["metadatas"][0]
    distances = resultat["distances"][0]

    for texte, metadata, distance in zip(
        documents,
        metadonnees,
        distances,
    ):
        passages.append({
            "texte": texte,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": distance,
        })

    return passages
