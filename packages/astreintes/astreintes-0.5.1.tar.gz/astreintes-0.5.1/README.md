# astreintes

Calcul de rotations d'astreintes.

## Installation

```shell
pip install astreintes
```

## Guide d'utilisation Colab

Un exemple de feuille Colab pour un calcul avec la description des résultats se trouve ici: 
[astreintes.ipynb](https://colab.research.google.com/drive/1GXP3sc9TmqSry_GZPLnpuCoPIsUtICHC?usp=sharing)


- Dans la sheet Google choisir extensions / add-ons / get add-ons
- Chercher pour Sheets to Colab, par Google Colab Team
- Install


## Contribution
- Formatage automatique
```shell
ruff format
```
- Lancer les tests
```shell
python -m unittest discover ./src/tests
```
- Mise à jour de la version dans [pyproject.toml](pyproject.toml)
- Pull request vers la branche `main`
- Publication sur pypi:

```shell
pdm publish
```