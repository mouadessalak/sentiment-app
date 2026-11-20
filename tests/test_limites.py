"""Tests aux limites du contrat d'entrée (TP4, étape B). À COMPLÉTER.

PredictRequest promet un champ « text », chaîne de 1 à 2000 caractères.
Ce fichier vérifie cette promesse à ses frontières, puis au hasard (hypothesis).
"""
import json
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


@pytest.fixture(scope="module")
def client():
    """Portée « module » : l'API démarre une fois pour tout le fichier (hypothesis l'exige)."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as c:  # le « with » exécute le lifespan : le modèle est chargé
        yield c


def en_json(valeur: object) -> bytes:
    """Corps de requête JSON, sous forme d'octets : permet aussi d'envoyer un corps invalide."""
    return json.dumps(valeur).encode("utf-8")


CAS = [
    pytest.param(en_json({"text": ""}), 422, id="texte-vide"),
    pytest.param(en_json({"text": "   \t\n"}), 422, id="texte-blanc"),
    pytest.param(en_json({"text": "a"}), 200, id="un-caractere"),
    pytest.param(en_json({"text": "a" * 2000}), 200, id="2000-caracteres"),
    pytest.param(en_json({"text": "a" * 2001}), 422, id="2001-caracteres"),
    pytest.param(en_json({}), 422, id="champ-manquant"),
    pytest.param(en_json({"text": 42}), 422, id="champ-entier"),
    pytest.param(b"pas du json", 422, id="corps-invalide"),
]


@pytest.mark.parametrize("corps, code_attendu", CAS)
def test_frontieres_du_contrat(client, corps, code_attendu):
    reponse = client.post("/predict", content=corps, headers={"Content-Type": "application/json"})
    assert reponse.status_code == code_attendu
    if code_attendu == 422:
        detail = reponse.json()["detail"]
        assert isinstance(detail, list)
        for erreur in detail:
            assert set(("loc", "msg", "type")) <= set(erreur)


@given(st.text(min_size=1, max_size=2000).filter(lambda text: bool(text.strip())))
@settings(deadline=None, max_examples=30)
def test_propriete_texte_contractuel(client, text):
    reponse = client.post("/predict", json={"text": text})
    assert reponse.status_code == 200
    corps = reponse.json()
    assert corps["label"] in {"POSITIVE", "NEGATIVE", "INDETERMINE"}
    assert 0 <= corps["score"] <= 1


@given(st.text(alphabet=" \t\n\r", min_size=1, max_size=200))
@settings(deadline=None, max_examples=30)
def test_propriete_texte_blanc(client, text):
    reponse = client.post("/predict", json={"text": text})
    assert reponse.status_code == 422
    detail = reponse.json()["detail"]
    assert isinstance(detail, list)
    assert all(set(("loc", "msg", "type")) <= set(erreur) for erreur in detail)
