**Objectif** : Comparer les outils disponibles pour chaque catégorie et **justifier vos choix**.

### Linters Python

| Outil | Avantages | Inconvénients | Note /10 | Choix ? |
| --- | --- | --- | --- | --- |
| **Ruff** | Ultra rapide, configuration minimale, remplace plusieurs outils (flake8, isort…) | Couverture de règles encore inférieure à Pylint | 9/10 | ✅ |
| **Flake8** | Simple, très répandu, extensible via plugins | Lent comparé à Ruff, configuration fragmentée | 6/10 | ❌ |
| **Pylint** | Analyse très complète, règles poussées | Lent, configuration lourde, bruit pour débutants | 7/10 | ❌ |

Choix justifié : Ruff

Meilleur compromis vitesse / simplicité / modernité, particulièrement adapté à CI/CD.

### Formatters Python

| Outil | Avantages | Inconvénients | Note /10 | Choix ? |
| --- | --- | --- | --- | --- |
| **Ruff format** | Très rapide, compatible Black, unifié avec Ruff | Peu d’options de personnalisation | 9/10 | ✅ |
| **Black** | Standard de facto, zéro débat de style | Peu personnalisable, plus lent | 8/10 | ✅ |
| **autopep8** | Très permissif, personnalisable | Résultats incohérents, peu standard | 5/10 | ❌ |

Choix justifié : Ruff format

Même style que Black, mais beaucoup plus rapide et intégré à l’écosystème Ruff.

### Type Checkers

| Outil | Avantages | Inconvénients | Note /10 | Choix ? |
| --- | --- | --- | --- | --- |
| **Mypy** | Référence historique, très précis, grande communauté | Lent, configuration parfois complexe | 8/10 | ✅ |
| **Pyright** | Très rapide, excellente intégration VS Code | Moins configurable que Mypy | 9/10 | ✅ |
| **Pyre** | Analyse avancée, conçu pour gros projets | Mise en place complexe, peu courant | 6/10 | ❌ |

Choix justifié :

- Pyright pour productivité et vitesse
- Mypy si besoin de précision maximale ou compatibilité large

### Frameworks de Tests

| Outil | Avantages | Inconvénients | Note /10 | Choix ? |
| --- | --- | --- | --- | --- |
| **pytest** | Syntaxe simple, très puissant, énorme écosystème de plugins | Magie implicite parfois déroutante | 9/10 | ✅ |
| **unittest** | Inclus dans la standard library, explicite | Verbeux, peu flexible | 6/10 | ❌ |

Choix justifié : pytest

Plus lisible, plus rapide à écrire, mieux adapté aux projets modernes.

### Security Scanners

Comparez : OPTIONAL

| Outil | Avantages | Inconvénients | Note /10 | Choix ? |
| --- | --- | --- | --- | --- |
| **Bandit** | Analyse statique du code Python, simple | Faux positifs possibles | 7/10 | ✅ |
| **Safety** | Détection vulnérabilités dépendances | Analyse limitée aux packages | 7/10 | ✅ |
| **Snyk** | Très complet, multi-langages | Payant, dépendance à un service externe | 8/10 | ❌ |
| **Trivy** | Containers, images Docker, large spectre | Moins ciblé Python pur | 7/10 | ❌ |

Choix justifié :

- Bandit + Safety pour un projet Python standard
- Outils commerciaux (Snyk) pertinents surtout en contexte entreprise

### Sources utilisées

- Articles
    - [Medium - Why You Should Replace Flake8, Black, and isort with Ruff: The Ultimate Python Code Quality Tool](https://medium.com/@zigtecx/why-you-should-replace-flake8-black-and-isort-with-ruff-the-ultimate-python-code-quality-tool-a9372d1ddc1e)
    - [Medium - My Quest for the Best Python Formatter](https://medium.com/@jillvillany_7737/my-quest-for-the-best-python-formatter-cd25a544ef81)
    - [Infoworld - 4 Python type checkers to keep your code clean](https://www.infoworld.com/article/2260170/4-python-type-checkers-to-keep-your-code-clean.html)
    - [Medium - PyTest vs. unittest: A Comparative Guide for Python Testing](https://laerciosantanna.medium.com/pytest-vs-unittest-navigating-pythons-testing-terrain-2569912a0286)
    - [Geeks for geeks - Difference between Pytest and Unittest](https://www.geeksforgeeks.org/software-testing/difference-between-pytest-and-unittest/)
    - [Medium - Building a Secure CI/CD Pipeline](https://devsecopsai.today/8-practical-security-scans-to-run-in-every-ci-cd-pipeline-6bd243b06e9c)
- Documentations officielles
    - [Ruff](https://docs.astral.sh/ruff/)
    - [Black](https://black.readthedocs.io/)
    - [Flake8](https://flake8.pycqa.org/)
    - [Pylint](https://pylint.pycqa.org/)
    - [autopep8](https://pypi.org/project/autopep8/)
    - [Mypy](https://mypy.readthedocs.io/)
    - [Pyright](https://github.com/microsoft/pyright)
    - [Pyre](https://pyre-check.org/)
    - [pytest](https://docs.pytest.org/)
    - [unittest](https://docs.python.org/3/library/unittest.html)
    - [Bandit](https://bandit.readthedocs.io/)
    - [Safety](https://docs.pyup.io/docs/safety)
    - [Snyk](https://snyk.io/)
    - [Trivy](https://aquasecurity.github.io/trivy/)
