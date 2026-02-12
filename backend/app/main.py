"""Point d'entree de l'application API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importe les contrôleurs (routes)
from ..controllers.prediction_controller import router as prediction_router

# Importe la fonction d'initialisation de la BD
from ..utils.database import init_db
import logging

# Configure les logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crée l'application API FastAPI
app = FastAPI(
    title="Accidents Gravité API",
    description="API pour prédire la gravité des accidents de la route",
    version="0.1.0"
)

# Configure CORS pour permettre les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise la BD au démarrage de l'app
# Cela crée la table "predictions" si elle n'existe pas
try:
    init_db()
    logger.info("Base de donnees initialisée avec succes")
except Exception as e:
    logger.warning(f"Impossible d'initialiser la BD: {e}")
    logger.info("L'API fonctionnera sans BD en dev local")

# Inclut les routes de prédiction
app.include_router(prediction_router)


# Endpoint de santé pour vérifier que l'API fonctionne
@app.get("/health")
def health():
    """Endpoint de santé pour vérifier que l'API est en ligne"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
