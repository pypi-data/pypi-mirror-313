# cmpparis

`cmpparis`est une petite bibliothèque Python pour CMP afin de ne pas réecrire les différentes fonctions et de gagner du temps.

## Table des matières

- [Structure du Projet](#structure-du-projet)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Comment Contribuer](#comment-contribuer)
- [Gestion des Versions](#gestion-des-versions)
- [Déploiement sur PyPI](#déploiement-sur-pypi)
- [FAQ](#faq)
- [Licence](#licence)

## Structure du Projet

Voici la structure du projet :

- `cmpparis/` : Contient le code source de la bibliothèque.
- `tests/` : Contient les tests unitaires.
- `.gitignore` : Spécifie les fichiers à ignorer par Git.
- `LICENSE` : La licence du projet.
- `README.md` : Ce fichier, pour la documentation du projet sur CodeCatalyst.
- `README_PYPI.md` : Documentation spécifique pour PyPI.
- `setup.py` : Script de configuration pour le packaging et le déploiement sur PyPI.

## Prérequis

Assurez-vous d'avoir installé les éléments suivants sur votre système :

- Python 3.6 ou supérieur
- pip (le gestionnaire de paquets Python)
- `virtualenv` pour créer un environnement virtuel (optionnel mais recommandé)

## Installation

1. **Clonez le dépôt** :

   ```bash
   git clone https://codecatalyst.com/user/cmpparis.git
   cd cmpparis
   ```

## Utilsation

```python
from cmpparis import hello_paris

print(hello_paris())  # Bonjour, Paris!
```

## Comment contribuer ? 

1. **Créez une branche pour votre modification** :
```bash
git checkout -b nom-de-la-branche
```
2. **Faites vos modifications**
3. **Assurez-vous que tous les tests passent :**
```bash
pytest
```
4. **Ajoutez vos changements et commitez : **
```bash
git add .
git commit -m "Description de la modification"
```
5. **Poussez vos modifications : **
```bash
git push origin nom-de-la-branche
```
5. **Ouvrez une Pull Request sur CodeCatalyst.**

## Gestion des versions ? 
Nous suivons le versionnement sémantique. Les versions sont définies selon le schéma suivant : MAJOR.MINOR.PATCH.

### Mise à jour de la version et des packets
Dans `setup.py`, modifiez la ligne :
```bash
version="0.1.0"
install_requires*
```

## Déploiement sur PyPI ? 
### Étapes pour déployer une nouvelle version

1. **Assurez-vous que tous les tests passent :**

Installer la lib en local avant de la déployer pour faire des tests :
```bash
pip install -e .
```

Tester la lib : 
```bash
pytest
```
2. **Construisez le package :**

Pensez à installer au préalable wheel

```bash
pip install wheel
```

Puis lancer la commande suivante

```bash
python setup.py sdist bdist_wheel
```
Cela génère un répertoire dist/ contenant les fichiers .tar.gz et .whl.
3. **Déployez sur PyPI :**
Assurez-vous d'avoir installé twine :
```bash
pip install twine
```
Puis déployez la nouvelle version sur PyPI :
```bash
twine upload dist/*
```
Astuce : Vous pouvez tester le déploiement sur Test PyPI avant de déployer sur le vrai PyPI :
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
4. **Vérifiez l'installation :**
```bash
pip install cmpparis --upgrade
```