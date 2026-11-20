"""Tests d'intégration : l'API telle qu'elle tourne vraiment (TP4, étape D). À COMPLÉTER.

Les tests du TP3 vérifient des réponses ; ceux-ci vérifient le démarrage de l'API
et son comportement quand le modèle manque ou tombe en panne.
"""
from pathlib import Path

import pytest

MODELE = Path(__file__).resolve().parents[1] / "models" / "sentiment.joblib"
pytestmark = pytest.mark.skipif(not MODELE.exists(), reason="modèle non produit : python src/train.py")


def test_demarrage_reel_charge_le_modele():
    """D.1 (donné en exemple) : un client ouvert par « with » exécute le lifespan."""
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        reponse = client.get("/health")
    assert reponse.status_code == 200
    assert "TP2" in reponse.json()["model"]


def test_modele_absent_refuse_de_demarrer(monkeypatch):
    from fastapi.testclient import TestClient

    import predict
    from api.main import app

    monkeypatch.setattr(predict, "MODELE", Path("modele-inexistant.joblib"))
    predict.charger_modele.cache_clear()
    with pytest.raises(FileNotFoundError):
        with TestClient(app):
            pass
    predict.charger_modele.cache_clear()


def test_modele_non_charge_repond_503(monkeypatch):
    from fastapi.testclient import TestClient

    from api.main import app

    with TestClient(app) as client:
        monkeypatch.delattr(app.state, "classifier", raising=False)
        assert client.get("/health").status_code == 503
        reponse = client.post("/predict", json={"text": "avis normal"})
        assert reponse.status_code == 503


@pytest.mark.parametrize("exception", [RuntimeError("panique"), ValueError("bug interne")])
def test_modele_en_panne_repond_500_sans_detail(monkeypatch, exception):
    from fastapi.testclient import TestClient

    from api.main import app

    class ModeleEnPanne:
        model_name = "modele de test en panne"

        def predict(self, text):
            raise exception

    with TestClient(app) as client:
        monkeypatch.setattr(app.state, "classifier", ModeleEnPanne())
        reponse = client.post("/predict", json={"text": "avis normal"})
        assert reponse.status_code == 500
        assert "panique" not in reponse.text
        assert "bug interne" not in reponse.text
        assert reponse.json() == {"detail": "Erreur interne du serveur"}


def test_classes_inattendues_refusent_de_demarrer(monkeypatch):
    import api.model as api_model

    class PipelineInattendu:
        def __init__(self):
            self.classes_ = type("Classes", (), {"tolist": lambda self: ["positive", "NEUTRAL"]})()

    monkeypatch.setattr(api_model, "charger_modele", lambda: PipelineInattendu())
    with pytest.raises(RuntimeError, match="Classes du modèle inattendues"):
        api_model.load_model()
