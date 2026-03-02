# ============================================
# Stage 1 : BUILDER - compile les dépendances
# ============================================
FROM python:3.13-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
ENV UV_SYSTEM_PYTHON=1

COPY pyproject.toml uv.lock ./
RUN uv pip install .

# ============================================
# Stage 2 : FINAL - image de production
# ============================================
FROM python:3.13-slim

LABEL maintainer="Mina"
LABEL version="0.1.0"
LABEL description="Interface de visualisation des prédictions de gravité des accidents"

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY frontend/ ./frontend/

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "frontend/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
