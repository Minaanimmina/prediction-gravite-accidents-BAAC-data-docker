"""Métriques Prometheus pour l'API de prédiction d'accidents."""

import time
from prometheus_client import Counter, Gauge, Histogram

# --- Counters : événements cumulatifs (ne font que monter) ---

# Nombre total de prédictions effectuées, segmenté par résultat
predictions_total = Counter(
    "predictions_total",
    "Nombre total de prédictions effectuées",
    ["predicted_gravity"]  # label : "1", "2" ou "3"
)

# Nombre total de consultations de l'historique
history_requests_total = Counter(
    "history_requests_total",
    "Nombre total de requêtes sur l'historique des prédictions"
)

# Erreurs HTTP segmentées par type
http_errors_total = Counter(
    "http_errors_total",
    "Nombre total d'erreurs HTTP par type",
    ["error_type"]  # label : "validation", "not_found", "server_error"
)

# --- Gauges : valeurs instantanées (montent ET descendent) ---

# Temps de fonctionnement de l'app depuis le démarrage
# On stocke le timestamp de démarrage, on calcule la durée à la volée
_app_start_time = time.time()

app_uptime_seconds = Gauge(
    "app_uptime_seconds",
    "Temps écoulé depuis le démarrage de l'application en secondes"
)

# --- Histograms : distributions de valeurs ---

# Distribution des probabilités de gravité maximale prédite
# Buckets adaptés : probabilités entre 0 et 1
prediction_confidence_histogram = Histogram(
    "prediction_confidence_histogram",
    "Distribution de la probabilité de confiance de la prédiction",
    buckets=[0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
)

# Latence des requêtes DB (sauvegarde en BD)
db_query_duration_seconds = Histogram(
    "db_query_duration_seconds",
    "Durée des opérations en base de données en secondes",
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)


def update_uptime() -> None:
    """Met à jour le gauge uptime — à appeler régulièrement ou à chaque requête."""
    app_uptime_seconds.set(time.time() - _app_start_time)