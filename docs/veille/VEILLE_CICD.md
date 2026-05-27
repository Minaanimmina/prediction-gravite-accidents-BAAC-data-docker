# Veille CI/CD

## CI/CD

### 1. Qu'est-ce que la CI (Continuous Integration) ?

La Continuous Integration (CI) est une pratique qui consiste à intégrer fréquemment les modifications de code dans un dépôt partagé, en déclenchant automatiquement des tests et des vérifications.

L'intégration continue peut être envisagée comme une solution au problème du développement simultané de nombreuses branches d'application potentiellement conflictuelles.

- Quels problèmes résout-elle ?
    - Détecte les bugs plus tôt dans le développement
    - Réduit les conflits de code entre développeurs
    - Évite les intégrations longues et risquées en fin de projet
- Quels sont les principes clés ?
    - Intégrations fréquentes du code (plusieurs fois par jour)
    - Automatisation des tests
    - Vérification automatique du code à chaque changement
    - Feedback rapide pour les développeurs
- Donnez 3 exemples d'outils de CI
    - GitHub Actions
    - GitLab CI/CD
    - Jenkins

### 2. Qu'est-ce que le CD (Continuous Deployment/Delivery) ?

Le Continuous Delivery / Deployment (CD) prolonge la CI en automatisant les étapes qui permettent de préparer ou déployer une application après les tests.

- Différence entre Continuous Delivery et Continuous Deployment ?
    - Continuous Delivery : Le code est toujours prêt à être déployé, mais le déploiement nécessite une action humaine.
    - Continuous Deployment : Chaque modification validée est déployée automatiquement en production, sans intervention humaine.
- Quels sont les risques et bénéfices ?
    - Bénéfices :
        - Déploiements plus rapides et plus fréquents
        - Réduction des erreurs humaines
        - Mise en production plus fiable
    - Risques :
        - Mauvaise configuration des tests
        - Déploiement automatique de bugs si les tests sont insuffisants

### 3. Pourquoi CI/CD est important ?

- Impact sur la qualité du code
    - Tests automatisés systématiques
    - Détection rapide des erreurs
    - Code plus stable et plus fiable
- Impact sur la vitesse de développement
    - Réduction du temps entre le développement et la mise en production
    - Moins de corrections tardives
    - Cycles de développement plus courts
- Impact sur la collaboration en équipe
    - Travail facilité à plusieurs sur le même projet
    - Feedback rapide pour tous les développeurs
    - Processus standardisés et partagés

### Différences CI/CD - résumé

| CI                 | CD                        |
| ------------------ | ------------------------- |
| Vérifie le code    | Livre / déploie le code   |
| Tests automatiques | Déploiement automatisé    |
| À chaque commit    | Après validation de la CI |
| Qualité            | Mise en production        |

### Ressources utilisées

- [Red Hat - Qu'est-ce que la CI/CD ?](https://www.redhat.com/fr/topics/devops/what-is-ci-cd)
- [Unity - Glossary CI/CD](https://unity.com/fr/glossary/ci-cd)
- [Wikipédia - CI/CD](https://en.wikipedia.org/wiki/CI/CD)

## Maîtriser uv

### 1. Qu'est-ce que uv ?

uv est un outil Python tout-en-un qui permet de gérer les dépendances, les environnements virtuels, l’installation des paquets et le build de projets Python, en s’appuyant sur pyproject.toml.

- En quoi est-ce différent de pip/poetry/pipenv ?
    - pip : installe des paquets, mais ne gère pas le projet dans son ensemble
    - pipenv / poetry : gèrent dépendances + environnements, mais sont plus lents et plus complexes
    - uv :
        - remplace pip, pip-tools, virtualenv et parfois poetry
        - est conçu pour être très rapide
        - utilise un seul outil pour plusieurs usages
- Quels sont les avantages ?
    - Très grande rapidité (écrit en Rust)
    - Unification des outils (moins de configuration)
    - Compatible avec les standards Python existants (pyproject.toml)
    - Adapté aux environnements locaux et CI/CD

### 2. Comment uv fonctionne avec pyproject.toml ?

uv utilise pyproject.toml comme fichier central de configuration du projet, conformément aux standards Python.

### Structure du fichier

Le fichier pyproject.toml contient notamment :

- les métadonnées du projet
- les dépendances
- la configuration du build backend

Exemple de pyproject.toml

```toml
[project]
name = "mon-projet"
version = "0.1.0"
description = "Exemple de projet Python utilisant uv"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }

authors = [
  { name = "Mina G", email = "mina@example.com" }
]

dependencies = [
  "requests>=2.31.0"
]

[project.optional-dependencies]
dev = [
  "pytest",
  "ruff",
  "pyright"
]

[build-system]
requires = ["uv"]
build-backend = "uv"

```

1. **`[project]`**

= Carte d’identité du projet
- `name` : nom du package (celui utilisé par pip install)
- `version` : version du projet (SemVer)
- `description` / `readme` : description et documentation
- `requires-python` : versions Python compatibles
- `license`, `authors` : métadonnées

2. **`dependencies`**

= Dépendances nécessaires pour faire tourner le projet

Elles sont installées quand qqn fait : `pip install mon-projet`

3. **`[project.optional-dependencies]**

= Dépendances optionnelles, souvent pour le développement


Installées avec : `pip install mon-projet[dev]`

4. **[build-system]**

= C’est ici que uv agit comme build backend.


### Gestion des dépendances (séparé par sections)

Les dépendances sont définies dans différentes sections, par exemple :

- dépendances principales du projet
- dépendances optionnelles (ex : dev, test)
- dépendances spécifiques à certains usages

uv lit ces sections pour installer uniquement les dépendances nécessaires, selon le contexte.

### Build backend

#### uv peut agir comme build backend

Dire que uv peut agir comme build backend signifie que uv est capable de fabriquer un package Python à partir du code source.
Concrètement, uv peut transformer un projet Python (fichiers .py + configuration) en formats standards installables, comme :
- une archive source (sdist)
- un package binaire (wheel)

Ces formats sont ceux utilisés par pip pour installer un projet.

#### Il implémente les interfaces standard de build Python (PEP 517 / PEP 518)

Python définit des standards officiels pour expliquer comment un projet doit être construit.
Ces standards sont décrits dans les PEP 517 et PEP 518.

- PEP 517 définit une interface commune entre les outils (pip) et le build backend
- PEP 518 définit comment déclarer le build backend et ses dépendances dans pyproject.toml

En les implémentant, uv devient compatible avec l’écosystème Python existant : pip, GitHub Actions ou d’autres outils peuvent demander à uv de construire le projet sans configuration spécifique.

#### Cela permet de construire et distribuer le projet sans outil supplémentaire

Grâce à ce rôle de build backend :
- uv peut remplacer des outils comme setuptools, flit ou poetry-core
- il n’est pas nécessaire d’ajouter un outil dédié uniquement au build
- toute la chaîne (dépendances, environnements, build) peut être gérée par un seul outil

Cela simplifie :
- la configuration du projet
- les pipelines CI/CD
- la reproductibilité du build

### 3. Comment utiliser uv dans GitHub Actions ?

uv est conçu pour s’intégrer facilement dans les pipelines CI/CD, notamment GitHub Actions.

### Installation

- uv peut être installé directement dans le workflow GitHub Actions
- Une action officielle est fournie pour simplifier l’installation

### Cache des dépendances

- uv utilise un cache de dépendances : c'est un endroit où uv garde en mémoire les packages déjà téléchargés et construits, pour éviter de refaire le travail à chaque fois.
- Ce cache peut être réutilisé entre les runs GitHub Actions
- Cela permet de réduire fortement le temps d’exécution des pipelines

### Exécution de commandes

Une fois installé, uv peut être utilisé pour :

- installer les dépendances
- lancer des scripts
- exécuter des commandes Python (tests, lint, build, etc.)

Exemples de commandes uv

```python
# Exécuter un script
uv run python script.py

# Lancer un module
uv run python -m http.server

# Exécuter un outil installé en dépendance dev
uv run pytest
uv run ruff check .

```

### Ressources utilisées

- [Documentation uv](https://docs.astral.sh/uv/)
- [uv - GitHub Integration](https://docs.astral.sh/uv/guides/integration/github/)
- [uv - Build Backend](https://docs.astral.sh/uv/concepts/build-backend/#modules)
- [uv Tutorial](https://www.youtube.com/watch?v=mFyE9xgeKcA&t=1040s)

## Comprendre Semantic Release

### 1. Qu'est-ce que le versionnage sémantique (SemVer) ?

Le versionnage sémantique (Semantic Versioning / SemVer) est une convention pour numéroter les versions d’un logiciel afin d’indiquer clairement l’impact des changements.

- Format MAJOR.MINOR.PATCH
    - MAJOR : changements incompatibles avec les versions précédentes
    - MINOR : nouvelles fonctionnalités compatibles avec l’existant
    - PATCH : corrections de bugs sans changement de fonctionnalité

Exemple : `2.3.1`

- Quand bumper chaque niveau ?
    - PATCH : correction de bug
    - MINOR : ajout de fonctionnalité sans casser l’existant
    - MAJOR : changement qui casse la compatibilité (breaking change)

### 2. Qu'est-ce que Conventional Commits ?

Conventional Commits est une convention pour écrire des messages de commit structurés et lisibles, afin de faciliter l’automatisation (changelog, versioning, releases).

- Format des messages

Le format général est :

```bash
type(scope): description

```

Exemple :

```bash
feat(api): add user authentication

```

- Types de commits (feat, fix, etc.)
    - `feat` : nouvelle fonctionnalité
    - `fix` : correction de bug
    - `docs` : documentation
    - `style` : formatage (pas de changement de code)
    - `refactor` : refactorisation
    - `test` : ajout ou modification de tests
    - `chore` : tâches techniques diverses

- Impact sur le versionnage
    - `fix` : incrément PATCH
    - `feat` : incrément MINOR
    - `feat!` ou `BREAKING CHANGE` : incrément MAJOR

### 3. Comment python-semantic-release fonctionne ?

`python-semantic-release` est un outil qui automatise le versionnage, le changelog et les releases, à partir des commits Conventional Commits. Cela permet d'automatiser tout le cycle de version d’un projet à partir de Git. Il se base sur une règle simple :

> La manière dont tu écris tes messages de commit détermine automatiquement la version, le changelog et la release.

#### Configuration dans `pyproject.toml`

Le comportement de l’outil est défini dans `pyproject.toml`

La configuration indique à python-semantic-release :
- où trouver la version du projet
- comment lire les commits
- quoi générer automatiquement

Tout est centralisé dans pyproject.toml.

**Que fait concrètement l’outil ?**

Quand on lance python-semantic-release, il :
1. lit l’historique Git depuis la dernière release
2. analyse les messages de commit
3. détermine le type de changements effectués
4. décide de la prochaine version à publier

**Comment il décide du bump de version**

Il s’appuie sur la convention Conventional Commits :

| Type de commit                | Impact sur la version |
| ----------------------------- | --------------------- |
| `fix:`                        | incrément PATCH       |
| `feat:`                       | incrément MINOR       |
| `feat!:` ou `BREAKING CHANGE` | incrément MAJOR       |

Exemple :
- dernière version : 1.2.3
- commits depuis :
  - fix: correct typo
  - feat: add new filter

La prochaine version sera : 1.3.0

**Pourquoi Git est central**

python-semantic-release ne lit pas le code.
Il lit Git :
- l’historique des commits
- les tags existants
- les messages de commit

#### Génération du `CHANGELOG`

**À quoi sert le CHANGELOG ?**

Le CHANGELOG est un fichier qui liste :
- ce qui a changé
- depuis la dernière version
- de manière lisible pour les humains

Comment il est généré
`python-semantic-release` :
1. prend tous les commits depuis le dernier tag Git
2. les classe par type :
- `feat` : nouvelles fonctionnalités
- `fix` : corrections
- autres types si configurés
3. génère un texte structuré

#### Création des releases GitHub

Ce que fait réellement une “release”

Une release GitHub, ce n’est pas juste une étiquette :
- c’est un tag Git
- associé à une version précise
- avec des notes de version visibles sur GitHub

Quand on déclenche une release, python-semantic-release :
1. met à jour le numéro de version dans le projet
2. crée un commit de release
3. crée un tag Git (ex : v1.3.0)
4. pousse le tag sur le dépôt distant
5. crée une release GitHub
6. y insère le contenu du changelog

#### Vision d'ensemble

```
Commits bien écrits
        ↓
Analyse automatique
        ↓
Version correcte
        ↓
CHANGELOG cohérent
        ↓
Release GitHub

```

### Ressources utilisées

- [Conventional Commits](https://www.conventionalcommits.org/fr/v1.0.0/)
- [Conventional Commits - Gist](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13)
- [Python Semantic Release](https://python-semantic-release.readthedocs.io/)

## MkDocs & GitHub Pages

### Comment MkDocs génère de la documentation ?

MkDocs est un générateur de site statique orienté documentation.
- La documentation est écrite en Markdown
- MkDocs lit les fichiers Markdown et un fichier de configuration (mkdocs.yml)
- Il génère un site web statique (HTML/CSS/JS)
- La navigation est automatiquement construite à partir de la structure définie dans mkdocs.yml
- Le thème (par défaut ou Material) contrôle l’apparence du site

### Comment déployer sur GitHub Pages ?

GitHub Pages permet d’héberger gratuitement des sites statiques depuis un dépôt GitHub

MkDocs fournit une commande dédiée (mkdocs gh-deploy)

Cette commande :
- génère le site statique
- le publie automatiquement sur une branche dédiée (gh-pages)

GitHub Pages sert ensuite le site à partir de cette branche

### Qu'est-ce que mkdocstrings ?

mkdocstrings est une extension pour MkDocs qui permet de :
- Générer automatiquement de la documentation à partir du code source
- Extraire docstrings, fonctions, classes et modules
- Intégrer cette documentation directement dans les pages Markdown
- Maintenir la documentation synchronisée avec le code

### Ressources utilisées

- [MkDocs](https://www.mkdocs.org/)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages](https://pages.github.com/)
