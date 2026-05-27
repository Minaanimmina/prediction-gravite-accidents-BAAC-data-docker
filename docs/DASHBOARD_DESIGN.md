# Dashboard Design — Justification des choix

## Dashboard 1 : HTTP Overview

**Métriques couvertes** : HTTP (applicatif) + Infrastructure (node-exporter).

### Panels et justifications

| Panel | Type | Métrique | Justification |
| --- | --- | --- | --- |
| Requêtes par seconde | Time series | `rate(http_requests_total[5m])` | Tendance dans le temps → Time series adapté. Permet de détecter les pics de charge. |
| Latence P95 | Time series | `histogram_quantile(0.95, ...)` | Le P95 est plus représentatif que la moyenne : il capture les cas lents qui impactent les utilisateurs. |
| Taux d'erreur % | Stat | `rate(5xx) / rate(total) * 100` | Valeur instantanée critique → Stat avec seuils colorés. Vert=0%, Orange=1%, Rouge=5%. |
| Total requêtes | Gauge | `sum(http_requests_total)` | Vue rapide du volume global depuis le démarrage. |
| CPU Usage % | Time series | `node_cpu_seconds_total` | Tendance CPU dans le temps pour détecter les dérives. |
| RAM Usage % | Gauge | `node_memory_MemAvailable_bytes` | Valeur instantanée avec seuils : orange à 70%, rouge à 90%. |
| Uptime | Stat | `app_uptime_seconds` | Valeur instantanée → Stat. Confirme que l'app n'a pas redémarré pendant les tests de charge. |
| Débit instantané (req/s) | Stat | `sum(rate(http_requests_total[30s]))` | Fenêtre courte pour une valeur très réactive. Utile pendant les tests Locust pour voir le débit en temps réel. |
| Requêtes par route | Time series | `sum by (handler) (rate(http_requests_total[1m]))` | Ventilation du trafic par endpoint. Permet d'identifier quel endpoint est le plus sollicité sous charge. |
| Latence P50/P95/P99 | Time series | `histogram_quantile(0.50/0.95/0.99, ...)` | Trois percentiles sur le même panel pour observer l'écartement sous charge. Un P99 qui explose sans que le P50 bouge indique des cas isolés lents. |
| Latence P95 par route | Time series | `histogram_quantile(0.95, sum by (le, handler) (...))` | Comparaison de la dégradation par endpoint sous charge. Permet d'identifier si `/predict` ou `/history` souffre le plus. |

**Approche** : RED (Rate, Errors, Duration) + infrastructure + stress testing.

---

## Dashboard 2 : ML Model Performance

**Métriques couvertes** : métriques custom métier + BD + containers (cAdvisor) + réseau (node-exporter).

### Panels et justifications

| Panel | Type | Métrique | Justification |
| --- | --- | --- | --- |
| Prédictions par minute | Time series | `sum(rate(predictions_total[5m])) * 60` | Tendance du volume de prédictions dans le temps. Permet de détecter une baisse d'activité anormale. |
| Répartition des gravités | Pie chart | `sum by (predicted_gravity) (predictions_total)` | Distribution des classes prédites → Pie chart idéal pour les proportions. Permet de détecter un biais du modèle. |
| Confidence P50/P95 | Time series | `histogram_quantile(0.50/0.95, ...)` | Suivi de la confiance du modèle dans ses prédictions. Une baisse de confidence peut signaler une dérive du modèle (data drift). |
| Latence BD P95 | Time series | `histogram_quantile(0.95, db_query_duration_seconds_bucket)` | Surveillance des performances de la base de données. Un pic de latence BD peut bloquer les sauvegardes de prédictions. |
| RAM par container | Time series | `container_memory_usage_bytes` | Suivi de la consommation mémoire par container Docker via cAdvisor. Permet de détecter des fuites mémoire. |
| Réseau Mo/s | Time series | `node_network_receive/transmit_bytes_total` | Surveillance du trafic réseau entrant et sortant via node-exporter. |

**Approche** : orientée ML — volume, qualité des prédictions, performance infrastructure.

### Métriques custom utilisées
- `predictions_total` (Counter avec label `predicted_gravity`) — métrique métier
- `prediction_confidence_histogram` (Histogram) — métrique métier custom
- `db_query_duration_seconds` (Histogram) — métrique technique custom
