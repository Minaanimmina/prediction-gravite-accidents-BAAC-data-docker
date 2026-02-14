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


# @app.get("/health")
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# test valeurs par défaut du formulaire Streamlit
def test_predict_with_default_streamlit_values():
    """Teste avec les valeurs par défaut du formulaire Streamlit."""
    features = {
        "vitesse_max_auto_clean": 50,
        "acc_est_en_agglo": 1,
        "intersection": 1,
        "nbre_voies_circu": 2,
        "luminosite": 1,
        "cond_atmo": 1,
        "etat_surface": 1,
        "route_rapide": 0,
        "infra_complexe": 0,
        "periode_jour_nuit_bin": 0,
        "saison_Hiver": 1,
        "saison_Printemps": 0,
        "saison_Ete": 0,
        "saison_Automne": 0,
    }
    response = client.post("/api/predictions/predict", json={"features": features})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in [1, 2, 3]
    assert "proba" in data


# Test avec features partielles
def test_predict_with_partial_features():
    """Teste que l'API gère les features manquantes."""
    response = client.post(
        "/api/predictions/predict",
        json={"features": {"luminosite": 1, "cond_atmo": 2}}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in [1, 2, 3]


# Test avec features invalides
def test_predict_invalid_input():
    """Teste qu'une requête sans 'features' retourne une erreur 422."""
    response = client.post("/api/predictions/predict", json={"mauvaise_cle": 123})
    assert response.status_code == 422


# Test historique sans base
def test_history_without_db():
    """Teste que l'historique retourne une liste vide sans base de données."""
    response = client.get("/api/predictions/history")
    assert response.status_code == 200
    assert response.json() == []