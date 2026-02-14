FROM python:3.11-slim

WORKDIR /app

# Installe les packages Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    streamlit>=1.30 \
    requests>=2.31 \
    pandas>=2.0

# Copie le code du frontend
COPY frontend/streamlit_app.py .

# Crée un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Change vers l'utilisateur non-root
USER appuser

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
