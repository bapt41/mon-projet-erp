# Projet ERP Odoo - Intégration avec Tkinter

Ce projet propose une solution ERP basée sur Odoo, déployée via Docker, ainsi qu'une application desktop développée en Python avec Tkinter pour interagir avec l’ERP via l’API XML-RPC. Il intègre notamment la gestion des ordres de fabrication et l'affichage des images produits.

## Table des Matières
- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Structure du Projet](#structure-du-projet)
- [Prérequis](#prérequis)
- [Installation et Configuration](#installation-et-configuration)
- [Utilisation](#utilisation)
- [Déploiement de l’ERP Odoo](#déploiement-de-lerp-odoo)
- [Développement de l’Interface Python](#développement-de-linterface-python)
- [Développement de l’Application Desktop Tkinter](#développement-de-lapplication-desktop-tkinter)
- [Documentation](#documentation)
- [Auteurs](#auteurs)
- [Licence](#licence)

## Présentation
Ce projet a pour objectif de démontrer la mise en place d’un système ERP complet avec :
- **Déploiement ERP** : Installation d’Odoo et PostgreSQL via Docker.
- **Interface Python** : Communication avec Odoo via l’API XML-RPC pour récupérer et mettre à jour des données (ordres de fabrication, images produits, etc.).
- **Application Desktop** : Interface graphique en Tkinter permettant à l’utilisateur de se connecter, de visualiser et d'interagir avec les données d’Odoo.

## Fonctionnalités
- **Déploiement ERP :**  
  Utilisation de Docker pour déployer Odoo et PostgreSQL.
- **Interface XML-RPC :**  
  Connexion et authentification sur le serveur Odoo, interrogation des données, mise à jour des ordres de fabrication, et récupération d'images produits.
- **Application Desktop :**  
  Application Tkinter offrant :
  - Une interface de connexion à Odoo.
  - Une Spinbox pour sélectionner l’ID d’un ordre de fabrication.
  - Un bouton pour incrémenter la quantité produite d’un ordre.
  - Un bouton pour charger et afficher une image d’un produit.
  - Une barre de status affichant la version d’Odoo, l’heure et l’état de l’OF.

## Structure du Projet

# ODOO
- **`docker-compose.yml`** – Configuration Docker pour Odoo et PostgreSQL  
- Autres scripts et configurations spécifiques à Odoo

# DESKTOP_TKINTER
- **`main.py`** – Application principale développée avec Tkinter  
- **`odoo_interface.py`** – Interface XML-RPC pour communiquer avec Odoo  
- **`requirements.txt`** – Liste des dépendances Python (ex : Pillow)  
- Ressources graphiques, icônes, etc.

# DOCS
- **`planning_gantt.md`** – Planning et suivi du projet  
- **`rapports.md`** – Documentation technique et rapports  
- **`README.md`** – Documentation globale du projet

# Autres fichiers
- **`.gitignore`** – Fichier listant les fichiers et dossiers à ignorer par Git


## Prérequis
- **Docker** et **Docker Compose** : pour le déploiement d’Odoo.
- **Git** : pour la gestion du code source.
- **Python 3.7+**.
- Modules Python requis :
  - `xmlrpc.client` (inclus avec Python)
  - `tkinter` (inclus avec Python)
  - `Pillow` (pour la gestion des images, installer avec `pip install Pillow`)
- (Optionnel) **PyInstaller** : pour générer un exécutable de l’application Tkinter.

## Installation et Configuration

### 1. Cloner le Repository
```bash
git clone https://github.com/votre_nom_utilisateur/nom_du_projet.git
cd nom_du_projet
