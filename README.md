# Prédiction de la Gravité des Accidents de la Route

## Description du projet

Ce projet prédit la **gravité d'un accident de la route** à partir de ses circonstances (lieu, heure, conditions météo, type de route, etc.).

Le modèle est entraîné sur les données **BAAC de l'ONISR** (2022-2024), puis déployé via :

- **API FastAPI** : pour les prédictions programmatiques
- **Interface Streamlit** : pour une utilisation opérationnelle
- **Base de données PostgreSQL** : pour enregistrer l'historique des prédictions
- **Docker & Docker Compose** : pour un déploiement reproductible

### Objectifs du projet

- Nettoyer et agréger les données BAAC
- Explorer les facteurs associés à la gravité
- Créer des features pertinentes
- Entraîner et comparer plusieurs modèles
- Déployer un modèle via une API REST et une application web
- Enregistrer les prédictions en base de données
- Conteneuriser l'application

## Structure du Projet

```ascii
prediction-gravite-accidents-BAAC-data-docker/
├── .dockerignore
├── .env.example                   # Variables d'environnement d'exemple
├── .gitignore
├── .pre-commit-config.yaml        # Hooks pre-commit (lint, format, sécurité)
├── .github/
│   └── workflows/
│       ├── ci.yml                 # Lint, type-check, sécurité, tests
│       ├── build.yml              # Build/push images Docker vers GHCR
│       └── release.yml            # Release sémantique automatique
├── CHANGELOG.md                   # Historique des versions (généré par semantic-release)
├── docker-compose.yml             # Orchestration des conteneurs
├── pyproject.toml                 # Dépendances Python et configuration des outils
├── README.md                      # Documentation du projet
├── uv.lock                        # Versions verrouillées des dépendances
├── backend/                       # API FastAPI
│   ├── Dockerfile                 # Image Docker multi-stage de l'API
│   ├── metrics.py                 # Définition des métriques Prometheus custom
│   ├── app/
│   │   └── main.py                # Point d'entrée FastAPI (middlewares, routing, Prometheus)
│   ├── controllers/
│   │   └── prediction_controller.py  # Endpoints predict et history
│   ├── data/
│   │   └── models/
│   │       └── best_model_multiclass.joblib  # Modèle LightGBM entraîné
│   ├── models/
│   │   └── prediction.py          # Modèle SQLAlchemy des prédictions
│   └── utils/
│       ├── config.py              # Chemins et features du modèle
│       ├── database.py            # Session SQLAlchemy et init DB
│       └── schemas.py             # Schémas Pydantic (entrées/sorties API)
├── docs/
│   ├── DASHBOARD_DESIGN.md        # Justification des choix de dashboards Grafana
│   ├── dashboards_grafana_screenshots/  # Captures des dashboards Grafana (Phase 3)
│   ├── prometheus_screenshots/    # Captures Prometheus : targets UP, requêtes PromQL (Phase 2)
│   └── veille/                    # Documents de veille technologique
│       ├── COMPARATIF_OUTILS.md
│       ├── PROBLEMES_DETECTES.md
│       ├── VEILLE_CICD.md
│       └── VEILLE_OBSERVABILITE.md
├── frontend/                      # Interface Streamlit
│   ├── Dockerfile
│   └── streamlit_app.py
├── monitoring/
│   ├── prometheus.yml             # Configuration Prometheus (scrape jobs)
│   └── dashboards_json/           # Dashboards Grafana exportés en JSON
├── tests/
│   ├── __init__.py
│   └── test_api.py
```

## Prérequis

### Installation avec Docker (recommandé)

- **Docker** (≥ 20.10)
- **Docker Compose** (≥ 1.29)

### Installation locale (optionnelle)

- **Python 3.13**
- **uv** (gestionnaire d'environnement et dépendances)
- **PostgreSQL 15+**

Pour vérifier Docker :

```bash
docker --version
docker-compose --version
```

## Installation et Déploiement

> **Recommandation :** utiliser Docker Compose pour un déploiement simple et reproductible.

### 1) Cloner ou ouvrir le projet

```bash
cd /chemin/vers/le/projet
```

### 2) Configurer l'environnement

Copier le fichier d'exemple puis adapter les valeurs :

```bash
cp .env.example .env
```

Points de vigilance :

- Remplacer les mots de passe par des valeurs robustes
- Ne jamais versionner le fichier `.env`
- Avec Docker, utiliser `postgres` (et non `localhost`) dans `DATABASE_URL`

### 3) Lancer l'application

```bash
docker-compose up --build
```

**Premier lancement :** peut prendre quelques minutes (build des images + démarrage des services).

### 4) Accéder aux services

| Service | URL |
| --------- | ----- |
| **API** | http://127.0.0.1:8000 |
| **API Docs** | http://127.0.0.1:8000/docs |
| **Streamlit** | http://127.0.0.1:8501 |
| **PostgreSQL** | localhost:5432 |
| **Prometheus** | http://localhost:9090 |
| **Grafana** | http://localhost:3000 |
| **node-exporter** | http://localhost:9100 |
| **cAdvisor** | http://localhost:8080 |

---

### Option locale (uv)

```bash
# 1) Créer l'environnement virtuel
uv venv

# 2) Installer les dépendances
uv sync

# 3) Démarrer l'API
uv run uvicorn backend.app.main:app --reload --port 8000

# 4) Démarrer Streamlit (autre terminal)
uv run streamlit run frontend/streamlit_app.py
```

## Images Docker

Les images applicatives sont construites automatiquement via **GitHub Actions** et publiées dans **GHCR** (GitHub Container Registry).

- Workflow de build : `.github/workflows/build.yml`
- Registre : `ghcr.io`
- Services : API (`backend/Dockerfile`) et application Streamlit (`frontend/Dockerfile`)

## Commandes utiles

### Avec Docker Compose

```bash
# Démarrer tous les services
docker-compose up

# Démarrer en arrière-plan
docker-compose up -d

# Reconstruire les images
docker-compose up --build

# Arrêter les services
docker-compose down

# Arrêter les services et supprimer les volumes (attention : perte de données)
docker-compose down -v

# Afficher les logs d'un service
docker-compose logs api
docker-compose logs app
docker-compose logs postgres

# Logs en temps réel
docker-compose logs -f api

# Exécuter une commande dans un conteneur
docker-compose exec api bash
docker-compose exec postgres psql -U postgres -d accidents_predictions
```

### Gestion des données PostgreSQL

```bash
# Accéder à PostgreSQL depuis le conteneur
docker-compose exec postgres psql -U postgres -d accidents_predictions

# Exemples de requêtes SQL (dans psql)
SELECT * FROM predictions;
SELECT COUNT(*) FROM predictions;
SELECT prediction, COUNT(*) FROM predictions GROUP BY prediction;
DELETE FROM predictions WHERE id = 1;
TRUNCATE TABLE predictions;
```

### Autres commandes Docker

```bash
docker ps
docker images
docker volume ls
docker inspect accidents-api
docker stop accidents-api
docker start accidents-api
docker rmi accidents-api:latest
```

## Base de Données

### Structure de la table `predictions`

```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    features_json JSON NOT NULL,
    prediction INTEGER NOT NULL,
    proba_grav1 FLOAT NOT NULL,
    proba_grav2 FLOAT NOT NULL,
    proba_grav3 FLOAT NOT NULL
);
```

## API REST - Endpoints

### Health Check

```bash
GET /health
# Réponse : {"status": "ok"}
```

### Créer une prédiction

```bash
POST /predict

# Body :
{
  "features": {
    "vitesse_max_auto_clean": 50,
    "acc_est_en_agglo": 1,
    "type_de_route_clean": 2
  }
}

# Réponse :
{
  "prediction": 1,
  "proba": {
    "grav_1": 0.497,
    "grav_2": 0.307,
    "grav_3": 0.196
  }
}
```

### Consulter l'historique

```bash
GET /history

# Réponse : liste des prédictions enregistrées
[
  {
    "id": 1,
    "timestamp": "2026-02-03T12:49:28.043",
    "features_json": {...},
    "prediction": 1,
    "proba_grav1": 0.497,
    "proba_grav2": 0.307,
    "proba_grav3": 0.196
  }
]
```

Documentation interactive : **http://127.0.0.1:8000/docs**

## Monitoring & Observabilité

La stack de monitoring comprend :

- **Prometheus** : collecte des métriques (scraping toutes les 15s)
- **Grafana** : visualisation (login: admin/admin)
- **node-exporter** : métriques système (CPU, RAM, réseau, disque)
- **cAdvisor** : métriques par container Docker

Dashboards disponibles :

- **HTTP Overview** : requêtes/sec, latence P95, taux d'erreur, CPU, RAM
- **ML Model Performance** : prédictions, répartition gravités, confidence modèle

## CI/CD et versioning

Le projet s'appuie sur **GitHub Actions** pour automatiser les contrôles qualité, le build et les releases :

- `ci.yml` : pre-commit, lint (`ruff`), type-check (`mypy`), sécurité (`bandit`, `safety`), tests (`pytest`)
- `build.yml` : build et publication des images Docker sur **GHCR**
- `release.yml` : publication de versions automatiques via **python-semantic-release**

Le versioning suit le **Semantic Versioning** (`MAJOR.MINOR.PATCH`), avec génération automatique des versions à partir des commits conventionnels.

## Interface Streamlit

L'application Streamlit permet de :

- Soumettre des variables d'entrée et obtenir une prédiction
- Visualiser les résultats

Accès : **http://127.0.0.1:8501**

## Sécurité

Pratiques de sécurité appliquées :

- Variables d'environnement pour les secrets (`.env`)
- Fichier `.env` exclu du versioning
- Validation des données avec Pydantic
- Gestion maîtrisée des sessions de base de données
- Séparation claire des responsabilités (app, controllers, models, utils)

## Technologies utilisées

| Domaine | Technologie |
| --------- | ------------- |
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | Streamlit |
| **ML** | LightGBM, scikit-learn, pandas |
| **BD** | PostgreSQL, SQLAlchemy |
| **Validation** | Pydantic |
| **Containerisation** | Docker, Docker Compose |
| **Environnement** | Python 3.13 + uv |

## Données

**Source :** Base BAAC (ONISR) - [Lien data.gouv.fr](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024)

**Années :** 2022, 2023, 2024

**Fichiers :**

- `caract-2022.csv`, `caract-2023.csv`, `caract-2024.csv`
- `lieux-2022.csv`, `lieux-2023.csv`, `lieux-2024.csv`
- `usagers-2022.csv`, `usagers-2023.csv`, `usagers-2024.csv`

## Support

En cas de problème :

1. Vérifier que Docker et PostgreSQL sont démarrés
2. Consulter les logs : `docker-compose logs`
3. Vérifier la configuration du fichier `.env`
4. Vérifier la disponibilité des ports (8000, 8501, 5432)

## Licence

MIT License

---

*Dernière mise à jour : 03 mars 2026*
