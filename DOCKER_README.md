# Documentation Docker

## Prérequis

- Docker installé (version 20.10+)
- Docker Compose installé (version 2.0+)

## Démarrage rapide

### 1. Configuration des variables d'environnement

Le fichier `.env` contient les configurations de l'application :

```bash
# Les valeurs par défaut sont déjà configurées
cp .env.example .env  # Si besoin de modifier
```

### 2. Construire et lancer les services

```bash
# Construire les images et démarrer les conteneurs
docker-compose up --build

# Ou en arrière-plan (mode détaché)
docker-compose up -d --build
```

### 3. Accéder à l'application

- **Interface Streamlit** : http://localhost:8501
- **API FastAPI** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

## Commandes utiles

### Gestion des conteneurs

```bash
# Arrêter les services
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f api
docker-compose logs -f app

# Redémarrer un service
docker-compose restart api
```

### Vérifier l'état des services

```bash
# Voir l'état des conteneurs
docker-compose ps

# Vérifier les healthchecks
docker inspect accidents-api | grep -A 10 Health
docker inspect accidents-app | grep -A 10 Health
```

### Développement

```bash
# Reconstruire une image après modification du code
docker-compose build api
docker-compose up -d api

# Exécuter une commande dans un conteneur
docker-compose exec api python --version
docker-compose exec app streamlit --version
```

## Structure des volumes

### Volumes de développement (bind mounts)

- `./api:/app` - Code de l'API synchronisé en temps réel
- `./app:/app` - Code Streamlit synchronisé en temps réel
- `./models:/models` - Modèles ML accessibles par l'API
- `./data/processed:/data/processed` - Données traitées

### Volumes nommés (persistance)

- `api-logs` - Logs de l'API (persiste entre les redémarrages)

## Healthchecks

Les services incluent des healthchecks automatiques :

- **API** : Vérifie `/health` toutes les 30s
- **App** : Vérifie `/_stcore/health` toutes les 30s

Le service `app` attend que l'`api` soit en bonne santé avant de démarrer.

## Optimisations

### Multi-stage build

Les Dockerfiles utilisent le multi-stage build pour :

- Réduire la taille des images finales
- Séparer les dépendances de build des dépendances runtime
- Améliorer la sécurité (pas d'outils de compilation en production)

### Cache des layers

Pour optimiser les builds :

- Les dépendances système sont installées en premier
- Les dépendances Python sont installées avant le code
- Le code applicatif est copié en dernier

## Dépannage

### L'API ne démarre pas

```bash
# Vérifier les logs
docker-compose logs api

# Vérifier que les fichiers sont bien copiés
docker-compose exec api ls -la /models
```

### Streamlit ne peut pas contacter l'API

```bash
# Vérifier que l'API est accessible
docker-compose exec app curl http://api:8000/health

# Vérifier les variables d'environnement
docker-compose exec app env | grep API_URL
```

### Rebuild complet si problèmes persistants

```bash
# Supprimer tout et reconstruire
docker-compose down -v
docker system prune -a
docker-compose up --build
```

## Production

Pour un déploiement en production :

1. Créer un fichier `.env.production` avec les vraies valeurs
2. Retirer les volumes de développement (bind mounts)
3. Utiliser des secrets Docker pour les données sensibles
4. Configurer un reverse proxy (nginx/traefik)
5. Activer HTTPS
