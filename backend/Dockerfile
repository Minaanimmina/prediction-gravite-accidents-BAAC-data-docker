# ============================================
# Stage 1 : BUILDER - compile les dépendances
# ============================================
FROM python:3.13-slim AS builder

WORKDIR /app

# gcc est nécessaire pour compiler certains packages Python (ex: psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Récupère uv depuis son image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_SYSTEM_PYTHON=1

# Copie les fichiers de dépendances et installe
# On copie ces fichiers EN PREMIER pour profiter du cache Docker :
# si le code change mais pas les dépendances, cette étape est skipée
COPY pyproject.toml uv.lock ./
RUN uv pip install .

# ============================================
# Stage 2 : FINAL - image de production
# ============================================
FROM python:3.13-slim

LABEL maintainer="Mina"
LABEL version="0.1.0"
LABEL description="API de prédiction de gravité des accidents"

WORKDIR /app

# curl est nécessaire pour les healthchecks Docker
# libgomp1 est nécessaire pour LightGBM
RUN apt-get update && apt-get install -y \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copie les packages Python compilés depuis le builder
# C'est la clé du multi-stage : on récupère le résultat sans les outils
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copie le code source
COPY backend/ ./backend/

# Sécurité : ne jamais faire tourner un conteneur en root en production
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# backend.app.main = chemin vers le fichier main.py
# :app = l'objet FastAPI créé dans ce fichier
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
