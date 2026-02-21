FROM python:3.13-slim

# Metadata pour l'image Docker
LABEL maintainer="Mina"
LABEL version="0.1.0"
LABEL description="Interface de visualisation des prédictions de gravité des accidents"

# Dossier de travail dans le conteneur
WORKDIR /app

# Copie uv depuis son image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Dit à uv d'utiliser le Python du système
ENV UV_SYSTEM_PYTHON=1

# Copie les fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installe les dépendances Python
RUN uv pip install .

# Copie le code du frontend
COPY frontend/ ./frontend/

# Crée un utilisateur non-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Change vers l'utilisateur non-root
USER appuser

# Documente le port exposé
EXPOSE 8501

# Lance l'application Streamlit
CMD ["streamlit", "run", "frontend/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
