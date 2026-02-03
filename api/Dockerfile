FROM python:3.11-slim

WORKDIR /app

# Installe les dépendances du système
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# Installe les packages Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    fastapi>=0.100 \
    pydantic>=2.0 \
    uvicorn[standard]>=0.23 \
    pandas>=2.0 \
    joblib>=1.3 \
    lightgbm>=4.0 \
    scikit-learn>=1.3 \
    sqlalchemy>=2.0 \
    psycopg2-binary>=2.9 \
    python-dotenv>=1.0

# Copie le code
COPY api/main.py .
COPY api/database.py .
COPY api/models.py .
COPY api/schemas.py .
COPY api/__init__.py .
COPY models /models
COPY data/processed /data/processed

# Crée un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Change vers l'utilisateur non-root
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]