# ERP Odoo - Intégration avec Tkinter

Ce projet propose une solution ERP basée sur Odoo, déployée via Docker, ainsi qu'une application desktop développée en Python avec Tkinter pour interagir avec l’ERP via l’API XML-RPC. L’application permet notamment la gestion des ordres de fabrication et l’affichage des images produits.

## Table des Matières
- [Présentation](#pr%C3%A9sentation)
- [Fonctionnalités](#fonctionnalit%C3%A9s)
- [Structure du Projet](#structure-du-projet)
- [Prérequis](#pr%C3%A9requis)
- [Installation et Configuration](#installation-et-configuration)
- [Utilisation](#utilisation)
- [Déploiement de l’ERP Odoo](#d%C3%A9ploiement-de-lerp-odoo)
- [Développement de l’Interface Python](#d%C3%A9veloppement-de-linterface-python)
- [Développement de l’Application Desktop Tkinter](#d%C3%A9veloppement-de-lapplication-desktop-tkinter)
- [Documentation](#documentation)
- [Auteurs](#auteurs)
- [Licence](#licence)

## Présentation

Ce projet a pour objectif de démontrer la mise en place d’un système ERP complet comprenant :

- **Déploiement ERP** : Installation d’Odoo et PostgreSQL via Docker.
- **Interface Python** : Communication avec Odoo via l’API XML-RPC pour récupérer et mettre à jour des données (fiche d’entreprise, produits, ordres de fabrication, commandes clients, tâches récentes, etc.).
- **Application Desktop** : Interface graphique en Tkinter permettant à l’utilisateur de se connecter, de visualiser un tableau de bord enrichi et d’interagir avec les données d’Odoo.

## Fonctionnalités

### Déploiement ERP
- Utilisation de Docker et Docker Compose pour déployer Odoo et PostgreSQL.

### Interface XML-RPC
- Connexion et authentification sur le serveur Odoo.
- Récupération de la fiche d'entreprise.
- Récupération de la liste des produits (avec image, catégorie et description).
- Gestion des ordres de fabrication (OF) avec filtrage par état.
- Mise à jour de la quantité produite d'un OF.
- Récupération du nombre total de commandes clients.
- Affichage des dernières OF et commandes clients.
- Sauvegarde des images produits.

### Application Desktop Tkinter
- Interface de connexion à Odoo.
- Tableau de bord avec indicateurs clés (fiche entreprise, nombre de commandes, OF en cours).
- Section "Nouveautés" présentant les dernières OF et commandes récentes.
- Gestion des OF avec filtrage par état et modification des quantités produites.

## Structure du Projet

```
.
├── ODOO
│   ├── docker-compose.yml        # Configuration Docker pour Odoo et PostgreSQL
│   └── (Autres scripts et configurations spécifiques à Odoo)
│
├── DESKTOP_TKINTER
│   ├── main.py                   # Application principale Tkinter
│   ├── odoo_interface.py         # Interface XML-RPC pour communiquer avec Odoo
│   ├── requirements.txt          # Dépendances Python
│   └── images/                   # Ressources graphiques et icônes
│
└── DOCS
    ├── planning_gantt.md         # Planning et suivi du projet
    ├── rapports.md               # Documentation technique et rapports
    └── README.md                 # Documentation globale du projet
```

## Prérequis

- **Docker et Docker Compose** : pour le déploiement d'Odoo.
- **Git** : pour la gestion du code source.
- **Python 3.7+**
- **Modules Python requis** :
  - `xmlrpc.client` (inclus avec Python)
  - `tkinter` (inclus avec Python)
  - `Pillow` (installer avec `pip install Pillow`)
- (Optionnel) **PyInstaller** : pour générer un exécutable de l'application Tkinter.

## Installation et Configuration

### 1. Cloner le Repository
```sh
git clone https://github.com/ninomrt-bot/mon-projet-erp.git
cd mon-projet-erp
```

### 2. Installer les Dépendances Python
Dans le dossier `DESKTOP_TKINTER`, lancez :
```sh
pip install -r requirements.txt
```

### 3. Configurer Odoo
Modifiez les paramètres de connexion dans `main.py` et `odoo_interface.py` selon votre configuration (adresse, port, nom de la base, etc.).

## Utilisation

### Lancement de l'Application Desktop
Dans le dossier `DESKTOP_TKINTER`, exécutez :
```sh
python main.py
```

### Interface de Connexion
Entrez vos identifiants Odoo pour vous connecter.

### Tableau de Bord
Une fois connecté, le tableau de bord affiche :
- La date du jour et l'utilisateur connecté.
- Des KPI clés (fiche entreprise, nombre de commandes, OF en cours).
- Une section "Nouveautés" et "Tâches récentes".

### Gestion des Ordres de Fabrication
- Utilisation d'un menu déroulant pour filtrer par état.
- Un double-clic sur un OF permet d'afficher ses détails et de modifier la quantité produite.

## Déploiement de l'ERP Odoo

Dans le dossier `ODOO`, utilisez Docker Compose pour déployer Odoo et PostgreSQL :
```sh
docker-compose up -d
```
Accédez à Odoo via [http://localhost:8069](http://localhost:8069).

## Développement de l’Interface Python
La communication avec Odoo se fait via XML-RPC dans `odoo_interface.py`. Vous pouvez modifier ou étendre les méthodes de cette interface.

## Développement de l’Application Desktop Tkinter
Le fichier `main.py` contient l'application Tkinter, structurée en plusieurs pages (Login, Dashboard, Orders, etc.).

## Documentation
- `DOCS/planning_gantt.md` : Planning et suivi du projet.
- `DOCS/rapports.md` : Documentation technique.

## Auteurs
- **Nino Marquet** **Baptiste Sottejeau** **Nicolas Klein** 

## Licence
Ce projet est sous licence MIT.
