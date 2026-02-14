"""Tests pour l'API FastAPI."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


# @router.post("/predict")
def test_predict_endpoint_success():
    # Exemple de features pour faire une prédiction
    input_data = {
        "features": {
            "acc_est_en_agglo": 1,
            "intersection": 0,
            "luminosite": 1,
            "cond_atmo": 1,
            "etat_surface": 1,
            "vitesse_max_auto_clean": 50,
            "nbre_voies_circu": 3,
            "route_rapide": 1,
            "infra_complexe": 1,
            "periode_jour_nuit_bin": 1,
            "saison_Automne": 0,
            "saison_Ete": 0,
            "saison_Hiver": 1,
            "saison_Printemps": 0,
        }
    }
    response = client.post("/api/predictions/predict", json=input_data)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert data["prediction"] in [1, 2, 3]
    assert "proba" in data


# @router.get("/history")


# @app.get("/health")
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
