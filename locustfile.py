"""Script de stress testing pour l'API de prédiction d'accidents."""

import random

from locust import HttpUser, between, task

SAMPLE_FEATURES = {
    "acc_est_en_agglo": 1,
    "intersection": 0,
    "luminosite": 1,
    "cond_atmo": 1,
    "etat_surface": 1,
    "vitesse_max_auto_clean": 50,
    "nbre_voies_circu": 2,
    "route_rapide": 0,
    "infra_complexe": 0,
    "periode_jour_nuit_bin": 1,
    "saison_Automne": 0,
    "saison_Ete": 1,
    "saison_Hiver": 0,
    "saison_Printemps": 0,
}


class PredictionUser(HttpUser):
    """Utilisateur simulant des appels de prédiction complets."""

    wait_time = between(1, 3)

    @task(3)
    def predict(self) -> None:
        """Effectue une prédiction avec des features légèrement variées."""
        features = SAMPLE_FEATURES.copy()
        features["vitesse_max_auto_clean"] = random.choice([30, 50, 70, 90, 110, 130])
        features["nbre_voies_circu"] = random.randint(1, 4)
        features["acc_est_en_agglo"] = random.randint(0, 1)

        self.client.post(
            "/api/predictions/predict",
            json={"features": features},
            name="/api/predictions/predict",
        )

    @task(1)
    def get_history(self) -> None:
        """Consulte l'historique des prédictions."""
        self.client.get(
            "/api/predictions/history",
            name="/api/predictions/history",
        )

    @task(1)
    def health_check(self) -> None:
        """Vérifie la santé de l'API."""
        self.client.get("/health", name="/health")


class ReadOnlyUser(HttpUser):
    """Utilisateur simulant uniquement de la lecture."""

    wait_time = between(2, 5)

    @task
    def get_history(self) -> None:
        self.client.get(
            "/api/predictions/history",
            name="/api/predictions/history",
        )

    @task
    def health_check(self) -> None:
        self.client.get("/health", name="/health")
