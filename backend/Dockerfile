# Image de base Python 3.13 version légère (sans outils inutiles)
FROM python:3.13-slim

# Dossier de travail dans le conteneur
WORKDIR /app


# Installe les outils système nécessaires :
# - gcc : compilateur C (nécessaire pour certains packages Python)
# - postgresql-client : pour communiquer avec PostgreSQL
# - curl : pour faire des requêtes HTTP (utile pour les health checks)
# rm -rf ... : nettoie le cache apt pour réduire la taille de l'image
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copie uv depuis son image officielle (multi-stage copy)
# Ça évite d'installer uv manuellement
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Dit à uv d'utiliser le Python du système
ENV UV_SYSTEM_PYTHON=1

# Copie les fichiers de dépendances qui seront stockées en cache pour accélérer les builds suivants
COPY pyproject.toml uv.lock ./

# Installe les dépendances Python
RUN uv pip install .

# Copie le dossier backend/ local dans app/backend/ dans le conteneur
COPY backend/ ./backend/

# Sécurité : crée un utilisateur non-root
# Ne jamais faire tourner un conteneur en root en production
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Change vers l'utilisateur non-root
USER appuser

# Documente le port exposé
EXPOSE 8000

# Lance l'API FastAPI
# backend.app.main = chemin vers le fichier main.py
# :app = l'objet FastAPI dans ce fichier
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
