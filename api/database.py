# Importe les outils SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables d'environnement depuis un fichier .env

# Configure la connexion à PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Vérification : s'assurer que la variable existe
if not DATABASE_URL:
    raise ValueError("DATABASE_URL n'est pas définie dans le .env !")

# Crée le moteur
engine = create_engine(DATABASE_URL)

# Crée une "session"
SessionLocal = sessionmaker(bind=engine)

# Base pour tous tes modèles
Base = declarative_base()

# Fonction pour créer toutes les tables automatiquement
def init_db():
    Base.metadata.create_all(bind=engine)