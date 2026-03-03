# Veille : Observabilité & Monitoring — Prometheus, Grafana, PromQL

> Réalisée dans le cadre du brief **Monitoring & Observabilité : Prometheus, Grafana et Stress Testing avec FastAPI**
> 

---

## 1. Monitoring vs Observabilité : quelle différence ?

### Définitions

**Le monitoring** est la surveillance continue d'un système à partir d'un ensemble de métriques et de seuils prédéfinis. Il répond à la question : *"Est-ce que ça marche ?"*. Il détecte les pannes connues, génère des alertes et produit des rapports sur l'état de santé du système.

**L'observabilité** est la capacité à comprendre l'état interne d'un système à partir des données qu'il produit (métriques, logs, traces). Elle répond à la question : *"Pourquoi est-ce que ça ne marche pas ?"*. Elle permet d'explorer et de diagnostiquer des problèmes **inconnus à l'avance**, notamment dans des architectures distribuées complexes.

> Une formule pour retenir : *le monitoring te dit que quelque chose ne va pas, l'observabilité te dit quoi et pourquoi.*
> 

### Complémentarité

Le monitoring est un **sous-ensemble** de l'observabilité : on ne peut surveiller efficacement que ce qui est observable. Les deux approches se nourrissent mutuellement.

| Aspect | Monitoring | Observabilité |
| --- | --- | --- |
| Question | "Est-ce cassé ?" | "Pourquoi est-ce cassé ?" |
| Approche | Métriques prédéfinies, seuils | Analyse de logs, métriques, traces |
| Périmètre | Composants individuels | Système dans son ensemble |
| Réactivité | Détection d'incidents connus | Diagnostic d'incidents inconnus |
| Outils typiques | Nagios, Zabbix, PRTG | Prometheus + Grafana, OpenTelemetry |

### Sources

- [AWS — Observability vs Monitoring](https://aws.amazon.com/compare/the-difference-between-monitoring-and-observability/)
- [Interdata Blog — Observabilité vs Monitoring](https://blog.interdata.fr/article/observabilite-vs-monitoring)
- [IBM — Observability vs. monitoring](https://www.ibm.com/think/topics/observability-vs-monitoring)
- [CrowdStrike — Observability vs. Monitoring](https://www.crowdstrike.com/en-us/cybersecurity-101/observability/observability-vs-monitoring/)

---

## 2. Les 3 piliers de l'observabilité

L'observabilité repose sur trois sources de données complémentaires :

### Métriques (Metrics)

Des mesures numériques collectées à intervalles réguliers : taux de requêtes, utilisation CPU, latence, nombre d'erreurs… Légères à stocker, idéales pour les dashboards et alertes.

### Logs

Des enregistrements horodatés d'événements discrets. Plus verbeux que les métriques, ils fournissent le contexte détaillé d'un incident (stack trace, paramètres de requête, messages d'erreur).

### Traces

Une trace suit le cheminement complet d'une requête à travers les différents composants d'un système distribué (microservices, bases de données, files de messages). Essentielle pour identifier où se produisent les goulots d'étranglement.

> Dans ce brief, on se concentre sur le **premier pilier : les métriques**, avec Prometheus comme collecteur et Grafana comme visualiseur.
> 

### Source

- [TechTarget — Observability vs. monitoring](https://www.techtarget.com/searchitoperations/tip/Observability-vs-monitoring-Whats-the-difference)

---

## 3. Architecture de Prometheus : le modèle Pull

### Fonctionnement général

Prometheus collecte ses métriques selon un **modèle pull** : c'est lui qui va activement interroger (scraper) les endpoints `/metrics` exposés par les applications cibles, à intervalles réguliers (par défaut toutes les 15 secondes).

```
[Application FastAPI]  ──expose──▶  /metrics (HTTP)
        ▲
        │  scrape toutes les 15s
[Prometheus Server]  ──stocke──▶  Time Series Database (TSDB)
        │
        ▼
    [Grafana]  ──requêtes PromQL──▶  Dashboards
```

Ce modèle présente plusieurs avantages :

- Prometheus contrôle la fréquence de collecte
- Plus simple à configurer pour des architectures stables
- Facilite la détection des cibles "down" (si une cible ne répond pas, Prometheus le sait)

### Configuration : `prometheus.yml`

```yaml
global:
  scrape_interval: 15s  # fréquence de scraping par défaut

scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['fastapi:8000']  # l'app expose /metrics sur le port 8000

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
```

### Sources

- [Prometheus — Documentation officielle](https://prometheus.io/docs/introduction/overview/)
- [Better Stack — Prometheus Metrics Explained](https://betterstack.com/community/guides/monitoring/prometheus-metrics-explained/)

---

## 4. Les 4 types de métriques Prometheus

### Counter (Compteur)

Un counter **ne fait qu'augmenter** (ou se réinitialise à 0 au redémarrage). Il mesure un total cumulatif d'événements.

- **Quand l'utiliser** : nombre total de requêtes HTTP, nombre d'erreurs, nombre d'items créés
- **Convention de nommage** : toujours suffixer par `_total`
- **En PromQL** : ne jamais lire la valeur brute, toujours utiliser `rate()` ou `increase()`

```python
# Exemple Python avec prometheus_client
from prometheus_client import Counter
items_created_total = Counter('items_created_total', 'Nombre total d\'items créés')
items_created_total.inc()  # +1 à chaque création
```

```
# Taux de création d'items par seconde sur 5 minutes
rate(items_created_total[5m])
```

### Gauge (Jauge)

Un gauge représente une valeur **qui peut monter ou descendre**. Il reflète l'état courant d'une mesure.

- **Quand l'utiliser** : nombre d'items actuellement en base, utilisation mémoire, nombre de connexions actives, température
- **En PromQL** : peut être lu directement, ou avec des fonctions comme `avg_over_time()`

```python
items_total = Gauge('items_total', 'Nombre d\'items actuellement en base')
items_total.inc()   # +1 au create
items_total.dec()   # -1 au delete
```

### Histogram

Un histogram **distribue des observations dans des buckets prédéfinis**. Il stocke automatiquement trois séries :

- `<metric>_bucket{le="X"}` : compteur cumulatif pour chaque bucket
- `<metric>_count` : nombre total d'observations
- `<metric>_sum` : somme de toutes les valeurs observées

**Quand l'utiliser** : durée de requêtes HTTP, latence de requêtes DB, distribution des prix

**Avantage** : permet de calculer des percentiles (P50, P95, P99) **après la collecte**, et d'agréger les données entre instances

```python
from prometheus_client import Histogram
items_price_histogram = Histogram(
    'items_price_histogram',
    'Distribution des prix des items',
    buckets=[1, 5, 10, 50, 100, 200, 500, 1000]  # buckets adaptés au domaine
)
items_price_histogram.observe(prix)  # à chaque création d'item
```

```
# P95 des prix sur les 5 dernières minutes
histogram_quantile(0.95, rate(items_price_histogram_bucket[5m]))
```

### Summary (Résumé)

Similaire à l'histogram, mais les quantiles sont calculés **côté client** (dans l'application). Les quantiles sont précis, mais **ne peuvent pas être agrégés** entre plusieurs instances.

- **Quand l'utiliser** : rare — uniquement pour une instance unique où l'agrégation n'est pas nécessaire
- **Recommandation** : préférer les Histograms dans la grande majorité des cas

---

### Tableau récapitulatif

| Type | Valeur | Monte/Descend | Agrégable | Cas d'usage typique |
| --- | --- | --- | --- | --- |
| Counter | Cumulatif | Monte uniquement | ✅ | Requêtes totales, erreurs totales |
| Gauge | Instantané | Les deux | ✅ | RAM utilisée, items en base |
| Histogram | Distribution (buckets) | Monte (compteurs) | ✅ | Latence, taille des réponses, prix |
| Summary | Quantiles pré-calculés | Monte (compteurs) | ❌ | Cas rares (instance unique) |

### Sources

- [Prometheus — Metric types (docs officielles)](https://prometheus.io/docs/concepts/metric_types/)
- [Prometheus — Understanding metric types (tutorial)](https://prometheus.io/docs/tutorials/understanding_metric_types/)
- [Better Stack — Prometheus Metrics Explained](https://betterstack.com/community/guides/monitoring/prometheus-metrics-explained/)
- [Dash0 — Understanding the Prometheus Metric Types](https://www.dash0.com/knowledge/prometheus-metrics)

---

## 5. Rôle de Grafana

Grafana est un outil open-source de **visualisation de données**. Il ne collecte pas lui-même les métriques : il se connecte à des sources de données (comme Prometheus) et permet de créer des **dashboards interactifs**.

### Fonctionnalités clés

- **Datasources** : Prometheus, InfluxDB, Loki, Elasticsearch, et bien d'autres
- **Panels** : blocs de visualisation individuels (Time series, Stat, Gauge, Heatmap, Table…)
- **Dashboards** : assemblages de panels, exportables en JSON
- **Alerting** : règles d'alerte basées sur des requêtes PromQL
- **Variables** : paramètres dynamiques pour filtrer les dashboards (ex: sélectionner un job, une instance)

### Types de visualisation adaptés

| Type de panel | Usage |
| --- | --- |
| Time series | Tendances dans le temps (taux de requêtes, latence) |
| Stat | Valeur instantanée en grand format (taux d'erreur actuel) |
| Gauge | Valeur avec seuils colorés visuels (% CPU, % RAM) |
| Heatmap | Distribution (idéal pour les histograms Prometheus) |
| Table | Données tabulaires comparatives |

### Source

- [Grafana — Site officiel](https://grafana.com/)
- [Grafana Blog — Introduction to PromQL](https://grafana.com/blog/2020/02/04/introduction-to-promql-the-prometheus-query-language/)

---

## 6. PromQL : fonctions essentielles

PromQL (Prometheus Query Language) est le langage de requête de Prometheus. Il opère sur des **séries temporelles**.

### Sélecteurs de base

```
# Valeur brute d'une métrique
items_total

# Filtrer par label
http_errors_total{error_type="not_found"}

# Filtrer par regex
http_errors_total{error_type=~"not_found|validation"}
```

### `rate()` — Taux de variation (pour les counters)

```
# Nombre de requêtes par seconde sur les 5 dernières minutes
rate(http_requests_total[5m])

# rate() ne s'applique QUE sur les counters
# La fenêtre [5m] doit être au moins 4x le scrape_interval
```

### `increase()` — Augmentation totale sur une période

```
# Nombre total d'items créés au cours de la dernière heure
increase(items_created_total[1h])
```

### Agrégations

```
# Somme de toutes les requêtes toutes méthodes confondues
sum(rate(http_requests_total[5m]))

# Somme par type d'erreur
sum(rate(http_errors_total[5m])) by (error_type)

# Moyenne CPU par job
avg(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (job)
```

### `histogram_quantile()` — Percentiles depuis un Histogram

```
# P95 de latence HTTP sur 5 minutes
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# P50 (médiane), P95 et P99 agrégés par route
histogram_quantile(0.99,
  sum by (le, handler) (
    rate(http_request_duration_seconds_bucket[5m])
  )
)

# Toujours wrapper avec rate() pour une fenêtre glissante récente
# Toujours conserver le label "le" dans les agrégations by()
```

### Calcul de taux d'erreur

```
# Taux d'erreur HTTP 5xx (% sur toutes les requêtes)
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
* 100
```

### Sources

- [Prometheus — Query functions (docs officielles)](https://prometheus.io/docs/prometheus/latest/querying/functions/)
- [PromLabs — PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/)
- [Grafana Blog — Introduction to PromQL](https://grafana.com/blog/2020/02/04/introduction-to-promql-the-prometheus-query-language/)
- [Chronosphere — Top 3 queries to add to your PromQL cheat sheet](https://chronosphere.io/learn/top-3-queries-to-add-to-your-promql-cheat-sheet/)

---

## 7. Bonnes pratiques de nommage des métriques

Le respect des conventions de nommage est essentiel pour la lisibilité et l'interopérabilité des métriques.

### Règles fondamentales

1. **snake_case** : tout en minuscules, mots séparés par des underscores
    - ok : `http_requests_total`
    - pas ok : `HttpRequestsTotal`, `http-requests-total`
2. **Préfixe domaine** : commencer par le nom de l'application ou du composant
    - ok : `fastapi_items_created_total`
    - ok : `node_cpu_seconds_total`
3. **Unités de base** : toujours utiliser les unités SI de base, jamais leurs multiples
    - ok : `_seconds` (jamais `_milliseconds`)
    - ok : `_bytes` (jamais `_megabytes`)
    - ok : `_ratio` pour les valeurs entre 0 et 1
4. **Suffixes réservés** :
    - `_total` : obligatoire pour les **counters**
    - `_seconds`, `_bytes`, `_ratio` : pour les unités
    - `_bucket`, `_count`, `_sum` : réservés aux **histograms** (générés automatiquement)
    - Ne jamais mettre `_total` ou `_count` sur un Gauge
5. **Labels vs métriques séparées** : utiliser des labels pour la segmentation, pas des noms de métriques différents
    - ok : `http_errors_total{error_type="not_found"}`
    - pas ok : `http_errors_not_found_total` + `http_errors_validation_total`
6. **Cardinalité** : éviter les labels à haute cardinalité (IDs utilisateurs, adresses email, UUIDs)

### Exemples corrects du projet

```
items_created_total          → Counter, création d'items
items_read_total             → Counter, lectures d'items
items_updated_total          → Counter, mises à jour
items_deleted_total          → Counter, suppressions
items_total                  → Gauge, items actuellement en base
items_price_histogram        → Histogram, distribution des prix
http_errors_total            → Counter avec label error_type
app_uptime_seconds           → Gauge, temps de fonctionnement
db_query_duration_seconds    → Histogram, latence des requêtes DB
```

### Sources

- [Prometheus — Metric and label naming (docs officielles)](https://prometheus.io/docs/practices/naming/)
- [Robust Perception — On the naming of things](https://www.robustperception.io/on-the-naming-of-things/)
- [Better Stack — Prometheus Best Practices](https://betterstack.com/community/guides/monitoring/prometheus-best-practices/)
