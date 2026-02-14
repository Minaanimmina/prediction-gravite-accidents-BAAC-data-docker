# Prédiction de la Gravité des Accidents de la Route

## Description du Projet

Ce projet prédit la **gravité d'un accident de la route** à partir de ses circonstances (lieu, heure, conditions météo, type de route, etc.).

Le modèle est entraîné sur les données **BAAC de l'ONISR** (2022-2024), puis déployé via :

- **API FastAPI** : Pour les prédictions programmatiques
- **Interface Streamlit** : Pour une utilisation conviviale
- **Base de données PostgreSQL** : Pour enregistrer l'historique des prédictions
- **Docker & Docker Compose** : Pour un déploiement facile et reproductible

### Objectifs du Projet

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
├── docker-compose.yml             # Orchestration des conteneurs
├── pyproject.toml                 # Dépendances Python
├── README.md                      # Documentation du projet
├── .gitignore                     # Fichiers ignorés par Git
├── .dockerignore                  # Fichiers ignorés par Docker
│
├── backend/                       # API FastAPI
│   ├── Dockerfile                 # Image Docker de l'API
│   ├── __init__.py
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py                # Endpoints FastAPI (predict, health, history)
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── prediction_controller.py  # Logique de prédiction
│   ├── data/
│   │   └── models/
│   │       └── best_model_multiclass.joblib  # Modele ML entraine
│   ├── models/
│   │   ├── __init__.py
│   │   └── prediction.py           # Modele SQLAlchemy des predictions
│   └── utils/
│       ├── __init__.py
│       ├── config.py               # Configuration de l'application
│       ├── database.py             # Configuration PostgreSQL & SQLAlchemy
│       └── schemas.py              # Schémas Pydantic (validation)
│
└── frontend/                      # Interface Streamlit
    ├── Dockerfile                 # Image Docker de Streamlit
    └── streamlit_app.py           # Application web
```

## Prérequis

Avant de commencer, assure-toi d'avoir :

### Installation locale (sans Docker)

- **Python >= 3.10**
- **PostgreSQL 15+** (pour la base de données)
- **pip** ou **conda** (gestionnaire de paquets)

### Installation avec Docker (recommandé)

- **Docker** (≥ 20.10)
- **Docker Compose** (≥ 1.29)

Pour vérifier que tu as Docker :

```bash
docker --version
docker-compose --version
```

## Installation et Déploiement

> **Recommandation :** Utilise Docker Compose pour une expérience sans friction et reproductible sur tous les systèmes.

### Option A : Avec Docker Compose

#### 1. Clone ou télécharge le projet

```bash
cd /chemin/vers/le/projet
```

#### 2. Configure le fichier `.env`

Crée un fichier `.env` à la racine du projet :

```env
# API
API_HOST=0.0.0.0
API_PORT=8000

# Streamlit
STREAMLIT_PORT=8501
API_URL=http://api:8000

# Base de données
DATABASE_URL=postgresql://postgres:TON_MOT_DE_PASSE@postgres:5432/accidents_predictions
POSTGRES_PORT=5432

# Python
PYTHONUNBUFFERED=1
```

**IMPORTANT - Sécurité :**

- Remplace `TON_MOT_DE_PASSE` par ton mot de passe réel
- **Ne commit jamais le fichier `.env` !** (déjà dans `.gitignore`)
- Pour Docker, utilise `postgres` au lieu de `localhost` dans DATABASE_URL

#### 3. Lance l'application

```bash
docker-compose up --build
```

**Premier lancement :** Peut prendre quelques minutes (construction des images + démarrage des services)

#### 4. Accède aux services

| Service | URL |
|---------|-----|
| **API** | http://127.0.0.1:8000 |
| **API Docs** | http://127.0.0.1:8000/docs |
| **Streamlit** | http://127.0.0.1:8501 |
| **PostgreSQL** | localhost:5432 |

---

### Option B : Installation Locale (sans Docker)

> **Note :** Cette option est plus complexe et nécessite d'installer PostgreSQL localement. Docker est recommandé.

#### Installation rapide

```bash
# 1. Crée l'environnement
conda create -n accidents-env python=3.11
conda activate accidents-env

# 2. Installe les dépendances
pip install fastapi pydantic uvicorn streamlit requests pandas joblib \
            sqlalchemy psycopg2-binary python-dotenv lightgbm scikit-learn

# 3. Configure .env
# DATABASE_URL=postgresql://postgres:TON_MOT_DE_PASSE@localhost:5432/accidents_predictions

# 4. Assure-toi que PostgreSQL tourne (port 5432)

# 5. Lance l'API
cd api && uvicorn main:app --reload --port 8000

# 6. Lance Streamlit (dans un autre terminal)
streamlit run app/streamlit_app.py
```

**Accès :** API sur `http://127.0.0.1:8000` | Streamlit sur `http://127.0.0.1:8501`

## Images Docker & DockerHub

### Images actuelles

L'application utilise 3 services Docker :

1. **API FastAPI** : Construite depuis `api/Dockerfile`
2. **Streamlit** : Construite depuis `app/Dockerfile`
3. **PostgreSQL 15** : Image officielle `postgres:15-alpine`

### Publier sur DockerHub

Pour partager tes images sur DockerHub :

```bash
# Connecte-toi
docker login

# Tag tes images
docker tag accidents-api ton-username/accidents-api:latest
docker tag accidents-app ton-username/accidents-app:latest

# Push
docker push ton-username/accidents-api:latest
docker push ton-username/accidents-app:latest
```

Puis utilise dans `docker-compose.yml` :

```yaml
api:
  image: ton-username/accidents-api:latest
app:
  image: ton-username/accidents-app:latest
```

## Commandes Utiles

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

# Arrêter et supprimer les volumes (ATTENTION: perte de données !)
docker-compose down -v

# Voir les logs d'un service
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

# Requêtes SQL utiles (dans psql)
SELECT * FROM predictions;                    # Voir toutes les prédictions
SELECT COUNT(*) FROM predictions;             # Compter les prédictions
SELECT prediction, COUNT(*) FROM predictions GROUP BY prediction;  # Distribution
DELETE FROM predictions WHERE id = 1;         # Supprimer une entrée
TRUNCATE TABLE predictions;                   # Vider la table
```

### Autres commandes Docker

```bash
# Lister les conteneurs en cours d'exécution
docker ps

# Lister toutes les images
docker images

# Voir les volumes
docker volume ls

# Inspecter un conteneur
docker inspect accidents-api

# Arrêter un conteneur
docker stop accidents-api

# Démarrer un conteneur
docker start accidents-api

# Supprimer une image
docker rmi accidents-api:latest
```

## Publication sur DockerHub

### Pourquoi publier sur DockerHub ?

- Partager facilement ton application avec d'autres
- Déployer sans avoir à cloner le repo et builder les images
- Utiliser les images directement depuis DockerHub
- Bonne pratique professionnelle

### Prérequis pour la publication sur DockerHub

- Compte DockerHub : https://hub.docker.com (gratuit)
- Docker CLI installé
- Connexion internet

### Processus complet de publication

#### Étape 1 : Créer un compte DockerHub

1. Va sur https://hub.docker.com
2. Clique sur "Sign Up"
3. Crée ton compte avec username (ex: `minaanim`)
4. Vérifie ton email

#### Étape 2 : Se connecter à Docker CLI

```bash
docker login
```

Entre ton username et password DockerHub. Tu devrais voir "Login Succeeded"

#### **Étape 3 : Identifier les images construites**

```bash
docker images
```

Tu verras quelque chose comme :

```
2026-01-26-prediction-de-la-gravite-des-accidents-de-la-route-api:latest
2026-01-26-prediction-de-la-gravite-des-accidents-de-la-route-app:latest
```

#### Étape 4 : Tagger les images avec ton username

```bash
# Pour l'API
docker tag 2026-01-26-prediction-de-la-gravite-des-accidents-de-la-route-api:latest TON_USERNAME/accidents-api:latest

# Pour l'App
docker tag 2026-01-26-prediction-de-la-gravite-des-accidents-de-la-route-app:latest TON_USERNAME/accidents-app:latest
```

**Remplace `TON_USERNAME` par ton username DockerHub !**

Exemple avec `minaanim` :

```bash
docker tag 2026-01-26-prediction-de-la-gravite-des-accidents-de-la-route-api:latest minaanim/accidents-api:latest
docker tag 2026-01-26-prediction-de-la-gravite-des-accidents-de-la-route-app:latest minaanim/accidents-app:latest
```

#### Étape 5 : Pousser les images sur DockerHub

```bash
# Pousser l'API
docker push TON_USERNAME/accidents-api:latest

# Pousser l'App
docker push TON_USERNAME/accidents-app:latest
```

**Ça peut prendre quelques minutes**

Quand c'est terminé, tu verras :

```
latest: digest: sha256:abc123... size: 5000
```

#### Étape 6 : Vérifier sur DockerHub

1. Va sur https://hub.docker.com
2. Connecte-toi
3. Tu devrais voir tes images dans ton profil :
   - `TON_USERNAME/accidents-api`
   - `TON_USERNAME/accidents-app`

### Utiliser les images depuis DockerHub

**Quelqu'un d'autre** peut maintenant utiliser ton application directement :

```bash
# Télécharger et lancer l'API
docker run -p 8000:8000 TON_USERNAME/accidents-api:latest

# Télécharger et lancer l'App
docker run -p 8501:8501 TON_USERNAME/accidents-app:latest
```

Ou utiliser le docker-compose modifié :
```yaml
api:
  image: TON_USERNAME/accidents-api:latest
app:
  image: TON_USERNAME/accidents-app:latest
```

### Bonnes pratiques

- Utilise des **tags explicites** (pas seulement `latest`)
- Documente tes images sur DockerHub (description, README)
- Ajoute une **version** : `TON_USERNAME/accidents-api:v1.0.0`
- Utilise `latest` pour la version stable
- Crée une **section "Releases"** sur ton repo GitHub

### Exemple avec versions

```bash
# Tagger avec version
docker tag source-image:latest TON_USERNAME/accidents-api:v1.0.0
docker tag source-image:latest TON_USERNAME/accidents-api:latest

# Pousser les deux
docker push TON_USERNAME/accidents-api:v1.0.0
docker push TON_USERNAME/accidents-api:latest
```

---

## Base de Données

### Structure de la table `predictions`

```sql
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    features_json JSON NOT NULL,
    prediction INTEGER NOT NULL,  -- 1, 2 ou 3 (gravité)
    proba_grav1 FLOAT NOT NULL,   -- Probabilité classe 1
    proba_grav2 FLOAT NOT NULL,   -- Probabilité classe 2
    proba_grav3 FLOAT NOT NULL    -- Probabilité classe 3
);
```

### Se connecter avec DBeaver

1. Nouvelle connexion PostgreSQL
2. Host: `localhost` (ou IP du serveur)
3. Port: `5432`
4. Database: `accidents_predictions`
5. Username: `postgres`
6. Password: `mina` (ou celui du `.env`)

---

## API REST - Endpoints

### Health Check

```bash
GET /health
# Réponse : {"status": "ok"}
```

### Faire une prédiction

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

# Réponse : Liste de toutes les prédictions
[
  {
    "id": 1,
    "timestamp": "2026-02-03T12:49:28.043",
    "features_json": {...},
    "prediction": 1,
    "proba_grav1": 0.497,
    "proba_grav2": 0.307,
    "proba_grav3": 0.196
  },
  ...
]
```

Accède à la documentation interactive sur : **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

## Interface Streamlit

L'application Streamlit permet de :

- Envoyer des features et voir une prédiction
- Visualiser les résultats

Accès : **[http://127.0.0.1:8501](http://127.0.0.1:8501)**

## Pipeline du Projet

### Étape 1 : Data Discovery & Cleaning

- Exploration des données BAAC (2022-2024)
- Identification des valeurs manquantes et aberrantes
- Nettoyage et fusion des datasets
- Voir : `notebooks/01_Data_discovery.ipynb` & `notebooks/02_Data_cleaning.ipynb`

### Étape 2 : EDA & Feature Engineering

- Analyse exploratoire des données
- Création de nouvelles features
- Visualisation des corrélations
- Voir : `notebooks/03_EDA_Feature_Engineering.ipynb`

### Étape 3 : Modélisation

- Entraînement de plusieurs modèles (LightGBM, XGBoost, CatBoost)
- Validation croisée et tuning d'hyperparamètres
- Sélection du meilleur modèle (CatBoost)
- Voir : `notebooks/04_Modeling.ipynb`

### Étape 4 : API & Interface Web

- Création de l'API FastAPI
- Développement de l'interface Streamlit
- Intégration de la BDD PostgreSQL
- Enregistrement de l'historique des prédictions

### Étape 5 : Dockerisation

- Création des images Docker
- Orchestration avec Docker Compose
- Déploiement reproductible

## Sécurité

### Bonnes pratiques utilisées

- Variables d'environnement pour les credentials (`.env`)
- `.env` dans `.gitignore` (pas committé)
- Validation des données avec Pydantic
- Gestion propre des sessions bases de données (try/finally)
- Séparation des préoccupations (database, models, schemas, main)

## Technologies Utilisées

| Domaine | Technologie |
|---------|-------------|
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | Streamlit |
| **ML** | CatBoost, scikit-learn, pandas |
| **BD** | PostgreSQL, SQLAlchemy |
| **Validation** | Pydantic |
| **Containerisation** | Docker, Docker Compose |
| **Environnement** | Python 3.11 |

## Données

**Source :** Base BAAC (ONISR) - [Lien data.gouv.fr](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024)

**Années :** 2022, 2023, 2024

**Fichiers :**

- `caract-2022.csv`, `caract-2023.csv`, `caract-2024.csv` → Caractéristiques des accidents
- `lieux-2022.csv`, `lieux-2023.csv`, `lieux-2024.csv` → Lieux des accidents
- `usagers-2022.csv`, `usagers-2023.csv`, `usagers-2024.csv` → Données des usagers impliqués

---

## Contribution

Ce projet est à titre éducatif. N'hésite pas à :

- Améliorer le modèle (meilleurs features, autre algo)
- Ajouter des endpoints API
- Optimiser les performances
- Corriger les bugs

---

## Support

Pour des questions ou des problèmes :

1. Vérifie que Docker & PostgreSQL tournent bien
2. Consulte les logs : `docker-compose logs`
3. Vérifie le fichier `.env`
4. Assure-toi que les ports (8000, 8501, 5432) sont libres

## Licence

MIT License

---

*Dernière mise à jour : 3 février 2026*
