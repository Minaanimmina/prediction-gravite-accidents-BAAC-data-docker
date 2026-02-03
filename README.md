# Prédiction de la gravité des accidents de la route

Ce projet vise à prédire la gravité d’un accident de la route à partir de ses circonstances (lieu, heure, conditions météo, type de route, etc.).  
Le modèle est entraîné sur les données BAAC de l’ONISR, puis déployé via une **API FastAPI** et une **interface Streamlit**.

## Contexte

Chaque année, la France enregistre environ 50 000 accidents corporels. Les données BAAC décrivent les accidents, les lieux et les usagers.  
L’objectif est d’anticiper la gravité maximale d’un accident à partir de facteurs contextuels.

## Objectifs

- Nettoyer et agréger les données BAAC.
- Explorer les facteurs associés à la gravité.
- Créer des features pertinentes.
- Entraîner et comparer plusieurs modèles.
- Déployer un modèle via une API et une application web.

## Aperçu de l’application

> `![Interface Streamlit](docs/Interface-streamlit.png)`

## Structure du projet

```text
accidents-gravite/
├── api/                # API FastAPI
│   └── main.py
├── app/                # Interface Streamlit
│   └── streamlit_app.py
├── data/
│   ├── doc/            # Documentation BAAC
│   ├── processed/      # Données préparées
│   └── raw/            # Données brutes
├── docs/               # Image README
├── models/             # Modèle entraîné + liste de features
├── notebooks/          # Notebooks
├── .gitignore
├── pyproject.toml
└── README.md
```

## Données

Source : **Base BAAC (ONISR)** (années 2005 à 2024)
[https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024](https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024)

Fichiers utilisés :

- `caract-2022.csv`, `lieux-2022.csv`, `usagers-2022.csv`
- `caract-2023.csv`, `lieux-2023.csv`, `usagers-2023.csv`
- `caract-2024.csv`, `lieux-2024.csv`, `usagers-2024.csv`

Les données nettoyées prêtes pour la modélisation sont exportées dans :

- `data/processed/accidents_model.csv`

### Téléchargement des données

Les données BAAC ne sont pas versionnées dans ce dépôt.

Elles peuvent être téléchargées depuis :
https://www.data.gouv.fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2024

Les fichiers CSV doivent être placés dans le dossier :

data/raw/<année>/

## Modélisation

- Problème : **classification multiclasse**
- Cible : `target_grav`
  - 1 = blessé léger
  - 2 = blessé hospitalisé
  - 3 = tué
- Modèles testés : RandomForest, XGBoost, LightGBM, CatBoost
- Modèle sauvegardé : `models/best_model_multiclass.joblib`
- Liste des features : `models/model_features.csv`

## API FastAPI

Endpoints :

- `GET /health` : statut de l’API
- `POST /predict` : prédiction + probabilités par classe

Exemple de requête :

```json
{
  "features": {
    "vitesse_max_auto_clean": 50,
    "acc_est_en_agglo": 1,
    "intersection": 1,
    "luminosite": 1,
    "cond_atmo": 1,
    "etat_surface": 1,
    "nbre_voies_circu": 2,
    "route_rapide": 0,
    "infra_complexe": 0,
    "periode_jour_nuit_bin": 0,
    "saison_Ete": 1,
    "saison_Hiver": 0,
    "saison_Printemps": 0,
    "saison_Automne": 0
  }
}
```

## Interface Streamlit

L’interface web permet de saisir les caractéristiques d’un accident et d’obtenir la prédiction via l’API.

Fichier principal :

- `app/streamlit_app.py`

## Installation & exécution (local)

Ce projet utilise un fichier `pyproject.toml` pour documenter ses dépendances Python.
Il ne s’agit pas d’un package Python installable, mais d’un projet applicatif (API + interface + notebooks).

Deux méthodes d’installation sont proposées :

- Option A — Conda + pip (recommandée) : solution stable pour la data science
- Option B — uv (optionnelle) : alternative plus rapide pour utilisateurs avancés

### Prérequis

- Python 3.10+
- (recommandé) Conda / Miniconda
- Git

### Option A — Conda + pip (recommandée)

Cette méthode est la plus robuste pour les bibliothèques de data science et de machine learning.

1. Créer et activer un environnement Conda

```bash
conda create -n accidents-gravite python=3.11 -y
conda activate accidents-gravite
```

2. Installer les dépendances

À la racine du projet :

```bash
pip install . .
```

3. (Optionnel) Dépendances pour les notebooks et l’entraînement

```bash
pip install ".[notebooks]"
```

### Option B — `uv` (optionnelle, plus rapide)

`uv` est un gestionnaire de dépendances moderne compatible avec `pyproject.toml`.

1. Installer `uv`

```bash
pip install uv
```

2. Installer les dépendances

```bash
uv pip install .
```

Pour les notebooks :

```bash
uv pip install ".[notebooks]"
```

> Cette option est destinée aux utilisateurs à l’aise avec les outils Python récents.

## Lancer le projet

### 1) Démarrer l’API (FastAPI)

```bash
uvicorn api.main:app --reload
```

Par défaut l’API est disponible sur :

> [http://127.0.0.1:8000](http://127.0.0.1:8000)

### 2) Démarrer l’application Streamlit

```bash
streamlit run app/streamlit_app.py
```

## Livrables

- Notebooks d’exploration et de modélisation
- Données nettoyées (exports)
- Modèle entraîné sauvegardé
- API fonctionnelle
- Interface Streamlit fonctionnelle
- Documentation d’installation et d’exécution
