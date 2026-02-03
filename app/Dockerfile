FROM python:3.11-slim

WORKDIR /app

# Installe les packages Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    streamlit>=1.30 \
    requests>=2.31 \
    pandas>=2.0

# Copie le code
COPY app/streamlit_app.py .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]