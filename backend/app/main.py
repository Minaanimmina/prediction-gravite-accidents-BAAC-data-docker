"""Point d'entree de l'application API."""

import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from ..controllers.prediction_controller import router as prediction_router
from ..metrics import app_uptime_seconds, update_uptime
from ..utils.database import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Accidents Gravité API",
    description="API pour prédire la gravité des accidents de la route",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Prometheus : expose /metrics automatiquement ---
# Ajoute les métriques HTTP standards : nb requêtes, latence, status codes
Instrumentator().instrument(app).expose(app)

try:
    init_db()
    logger.info("Base de donnees initialisée avec succes")
except Exception as e:
    logger.warning(f"Impossible d'initialiser la BD: {e}")
    logger.info("L'API fonctionnera sans BD en dev local")

app.include_router(prediction_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Endpoint de santé pour vérifier que l'API est en ligne."""
    update_uptime()  # on met à jour l'uptime à chaque appel health
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec B104