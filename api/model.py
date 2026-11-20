"""Raccord entre l'API et le modèle entraîné au TP2.

L'API n'entraîne rien et ne connaît pas scikit-learn : elle appelle la fonction
predict() de src/predict.py, qui charge models/sentiment.joblib une seule fois.
"""
import sys
from pathlib import Path
from typing import TypedDict

from api.schemas import SentimentLabel

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "src"))
from predict import charger_modele  # noqa: E402  (fonctions du TP2)
from predict import predict as _predict  # noqa: E402  (fonctions du TP2)

SEUIL_ABSTENTION = 0.60
ETIQUETTES_MODELE: dict[str, SentimentLabel] = {
    "positive": "POSITIVE",
    "negative": "NEGATIVE",
}


class ClassifierResult(TypedDict):
    label: SentimentLabel
    score: float
    text: str


class SentimentClassifier:
    """Enveloppe du modèle TP2 avec l'interface attendue par l'API."""

    model_name = "tfidf-logreg (TP2, models/sentiment.joblib)"

    def __init__(self) -> None:
        pipeline = charger_modele()
        classes = set(pipeline.classes_.tolist())
        attendues = set(ETIQUETTES_MODELE)
        if classes != attendues:
            raise RuntimeError(
                f"Classes du modèle inattendues : {sorted(classes)!r}; attendues : {sorted(attendues)!r}"
            )

    def predict(self, text: str) -> ClassifierResult:
        """Renvoie une étiquette du contrat et sa confiance."""
        r = _predict(text)
        if r["score"] < SEUIL_ABSTENTION:
            label: SentimentLabel = "INDETERMINE"
        else:
            label = ETIQUETTES_MODELE[r["label"]]
        return {"label": label, "score": r["score"], "text": text[:100]}


def load_model() -> SentimentClassifier:
    """Construit le classifier (le cache de chargement est dans src/predict.py)."""
    return SentimentClassifier()
