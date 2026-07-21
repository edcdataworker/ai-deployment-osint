# AI Deployment - veille OSINT militaire

Projet académique de déploiement d'une chaîne d'analyse OSINT sur un corpus d'articles de la rubrique « Guerre » de TASS.

La chaîne de traitement couvre :

- l'extraction et le nettoyage des articles ;
- l'annotation et l'entraînement d'un modèle spaCy NER ;
- la détection des labels `WEAPON`, `MIL_UNIT` et `MIL_ORG` ;
- l'indexation des résultats dans Elasticsearch ;
- la visualisation et l'analyse dans Kibana.

## Notebook

Le notebook de travail fourni pour le projet est disponible sur Google Colab :

[Ouvrir le notebook Colab](https://colab.research.google.com/drive/1wE2RMIx62Ic95o7bkGo29yfDAV7svlRQ?authuser=1)

Le fichier `.ipynb` devra être ajouté au dossier `notebooks/` après export depuis Colab afin d'archiver le code directement dans ce dépôt.

## Résultats principaux

- 20 895 articles analysés ;
- 41 665 mentions de systèmes d'armes ;
- 19 116 mentions d'unités militaires ;
- 72 816 mentions d'organisations militaires ;
- période couverte : 2015-2025.

## Contenu du dépôt

- `captures/` : captures des dashboards Kibana ;
- `livrable/` : livrable final au format PDF ;
- `scripts/` : script de génération du livrable.

## Auteurs

E.Cappaert, JC.Dorn, N.Segonds

## Précaution analytique

TASS est un média d'État russe. Les indicateurs décrivent ce que cette source publie et les entités détectées par le modèle ; ils ne constituent pas une validation indépendante des faits rapportés.
