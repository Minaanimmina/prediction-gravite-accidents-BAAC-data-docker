"""Initialisation SQLAlchemy et gestion des sessions."""

# Importe les outils SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()  # Charge les variables d'environnement depuis un fichier .env

# Configure la connexion à PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Variables globales qui seront initialisées si la BD est disponible
engine = None
SessionLocal = None

# Base pour tous les modèles
Base = declarative_base()

# Si DATABASE_URL est définie, tente de créer la connexion
if DATABASE_URL:
    try:
        # Crée le moteur
        engine = create_engine(DATABASE_URL)

        # Teste la connexion
        with engine.connect() as conn:
            logger.info("Connexion à la base de données réussie")

        # Crée une "session"
        SessionLocal = sessionmaker(bind=engine)
    except Exception as e:
        logger.warning(f"Impossible de se connecter à la base de données: {e}")
        logger.info("L'API fonctionnera sans persistance en base de données")
        engine = None
        SessionLocal = None
else:
    logger.warning("DATABASE_URL n'est pas définie - l'API fonctionnera sans base de données")


# Fonction pour créer toutes les tables automatiquement
def init_db():
    if engine is not None:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Tables de base de données créées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la création des tables: {e}")
    else:
        logger.info("Pas de base de données disponible - skip init_db")
