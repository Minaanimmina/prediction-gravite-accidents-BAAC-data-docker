# Problèmes détectés dans le code initial

Ce document recense les problèmes identifiés et corrigés au cours de la mise en place de la pipeline CI/CD.

## Architecture et imports

### 1. Imports cassés après le refactor MVC

Le passage à une architecture MVC (app, controllers, models, utils) a cassé tous les imports relatifs. Les chemins comme `from models import Prediction` ne fonctionnaient plus et devaient devenir `from ..models.prediction import Prediction`.

### 2. Fichier `backend/models/__init__.py` manquant

Le dossier `backend/models/` n'avait pas de fichier `__init__.py`, ce qui empêchait Python de le reconnaître comme un package. Les imports échouaient avec `ModuleNotFoundError`.

### 3. Fichier `backend/models/prediction.py` non commité

Le fichier existait en local mais n'avait jamais été ajouté à Git. La CI ne pouvait pas importer le module `prediction`.

## Git et .gitignore

### 4. `models/` dans le .gitignore bloquait le code Python

La règle `models/` dans le `.gitignore` visait les fichiers de modèles ML, mais elle ignorait aussi le dossier `backend/models/` contenant le code Python (les modèles SQLAlchemy).

Solution : remplacer par des règles spécifiques (`*.joblib`, `*.pkl`).

### 5. `*.joblib` dans le .gitignore empêchait le modèle ML d'être sur GitHub

Le fichier `best_model_multiclass.joblib` était nécessaire pour que l'API fonctionne, mais la règle `*.joblib` l'excluait de Git. La CI échouait avec `FileNotFoundError`.

Solution : retirer la règle et forcer l'ajout avec `git add -f`.

### 6. `*.joblib` dans le .dockerignore empêchait le modèle d'être dans l'image Docker

Même problème côté Docker : le modèle ML n'était pas copié dans l'image, rendant l'API inutilisable en conteneur.

### 7. Branches non supprimées après merge

Les branches mergées n'étaient pas supprimées, ce qui encombrait le dépôt.

Bonne pratique : supprimer la branche sur GitHub après le merge, puis `git branch -d` en local et `git fetch --prune`.

## Types et mypy

### 8. Fonctions sans annotations de type

Le mode strict de mypy (`disallow_untyped_defs = true`) exige des annotations de type sur toutes les fonctions. Il manquait `-> None` sur les fonctions de test et `-> dict[str, str]` sur les endpoints.

### 9. Stubs manquants pour la librairie `requests`

Mypy signalait `Library stubs not installed for "requests"`.

Solution : ajouter `types-requests` dans les dépendances additionnelles du hook mypy dans `.pre-commit-config.yaml`.

### 10. Valeurs entières au lieu de flottants

Les champs `proba_grav1`, `proba_grav2`, `proba_grav3` étaient initialisés avec `0` (entier) au lieu de `0.0` (flottant), ce qui provoquait une erreur mypy sur le typage.

## Docker

### 11. Version de Python obsolète (3.11 au lieu de 3.13)

Les Dockerfiles utilisaient `python:3.11-slim` alors que le projet tournait en Python 3.13 en local. Risque d'incompatibilités entre les environnements.

### 12. Dépendances installées en dur dans le Dockerfile

Les dépendances étaient listées directement dans le `RUN pip install` du Dockerfile au lieu d'utiliser le `pyproject.toml`. Cela rendait la gestion des versions opaque et cassait le cache Docker à chaque modification.

### 13. `libgomp.so.1` manquant après multi-stage build

Après le passage au multi-stage build, LightGBM ne trouvait plus la librairie OpenMP (`libgomp1`). Elle était installée dans le stage builder (avec `gcc`) mais pas copiée dans l'image finale. Solution : ajouter `libgomp1` dans le `apt-get install` du stage final.

### 14. `DATABASE_URL` pointant vers `localhost` dans Docker

Le fichier `.env` contenait `DATABASE_URL=postgresql://postgres:xxxx@localhost:5433/...`. Dans Docker, les conteneurs communiquent via le nom du service (`postgres`), pas `localhost`.

Solution : surcharger la variable dans le `docker-compose.yml`.

### 15. `API_URL` pointant vers `localhost` dans Docker

Le frontend Streamlit essayait de joindre l'API sur `localhost:8000`, mais dans Docker il faut utiliser le nom du service `api`.

Solution : configurer `API_URL=http://api:8000` dans le docker-compose.

### 16. Mot de passe PostgreSQL en dur dans docker-compose

`POSTGRES_PASSWORD: xxxx` était directement visible dans le `docker-compose.yml`.

Solution : déplacer les credentials dans le fichier `.env` et utiliser des variables (`${POSTGRES_PASSWORD}`).

### 17. `version: '3.8'` obsolète dans docker-compose

La directive `version` est obsolète depuis Docker Compose v2 et génère un warning.

Solution : supprimer la ligne.

### 18. `docker-compose` v1 incompatible avec le multi-stage build

La version 1.29.2 de docker-compose provoquait une erreur `KeyError: 'ContainerConfig'` avec les images multi-stage.

Solution : utiliser `docker compose` (v2, sans tiret) au lieu de `docker-compose`.

## CI/CD

### 19. Branche `main` au lieu de `master` dans les workflows

Tous les workflows référençaient `main` dans leurs triggers, mais la branche par défaut du projet était `master`. Aucun workflow ne se déclenchait sur la branche principale.

Solution : ajouter `master` dans les triggers.

### 20. Fichiers `.ipynb` corrompus dans `.virtual_documents/`

Des restes de notebooks Jupyter invalides faisaient échouer ruff lors du pre-commit.

Solution : supprimer le dossier et l'ajouter au `.gitignore`.

### 21. Pydantic `class Config` déprécié

L'utilisation de `class Config` dans les schémas Pydantic v2 générait un warning.

Solution : migrer vers `model_config = ConfigDict(...)`.

## Sécurité

### 22. Mot de passe PostgreSQL visible dans le README

La section DBeaver du README contenait le mot de passe en clair (`Password: xxxx`).

Solution : supprimer cette section et renvoyer vers le fichier `.env.example`.

### 23. Bind sur `0.0.0.0` signalé par Bandit

Bandit signalait `uvicorn.run(app, host="0.0.0.0")` comme un risque de sécurité (B104). Dans un contexte Docker, c'est nécessaire pour que le conteneur soit accessible.

Solution : ajouter le commentaire `# nosec B104` pour marquer le faux positif.
