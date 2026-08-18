## Présentation du projet

Ce projet est une application Python de gestion des commandes.
Elle permet de gérer les produits, les fournisseurs et les commandes
à travers une interface simple.


## Fonctionnalités

- Gestion des produits
- Gestion des fournisseurs
- Gestion des commandes
- Création des tables de la base de données
- Insertion de données de test


# Gestion des Commandes Fournisseurs

Application console en Python (POO) avec base de données MySQL, réalisée dans
le cadre du projet de programmation (POO & Base de données) — Licence 2
Informatique de Gestion (IAGE).

## Contexte

Application permettant à une entreprise sénégalaise de distribution de
matériel informatique de gérer ses fournisseurs, ses produits et ses
commandes (remplaçant un suivi papier source d'erreurs et de retards).

## Fonctionnalités

- **Fournisseurs** : ajout, liste, détail, modification, suppression
  (si aucune commande associée), recherche par code ou raison sociale.
- **Produits** : ajout, liste, détail, modification, suppression
  (si non présent dans une commande), recherche par désignation, alerte
  de réapprovisionnement (stock sous un seuil).
- **Commandes** : création avec plusieurs lignes de produits, vérification
  de la disponibilité du stock, calcul automatique du montant total,
  changement de statut (`EN_ATTENTE` → `VALIDEE` → `LIVREE`, jamais en
  arrière), annulation avec restitution du stock, suppression.
- **Rapports** : commandes par fournisseur, commandes en attente, valeur
  totale du stock, top 5 des produits les plus commandés, chiffre
  d'affaires total (commandes validées + livrées).

## Architecture

```
gestion_commandes/
├── database/
│   ├── config.py        # Configuration de connexion (hôte, base, identifiants)
│   └── connexion.py      # Singleton DatabaseConnection
├── models/
│   ├── fournisseur.py
│   ├── produit.py
│   └── commande.py       # Commande + LigneCommande
├── dao/
│   ├── base_dao.py       # Classe abstraite (get_all, get_by_id, delete_by_id)
│   ├── fournisseur_dao.py
│   ├── produit_dao.py
│   └── commande_dao.py
├── menu/
│   └── interface.py       # Interface utilisateur console
├── sql/
│   └── create_tables.sql  # Script SQL de création des tables
├── create_tables.py        # Crée les tables via Python
├── insert_test_data.py     # Insère des données de test
├── main.py                  # Point d'entrée de l'application
└── requirements.txt
```

### Choix techniques

- **Singleton** : `DatabaseConnection` garantit une seule instance de
  connexion partagée dans toute l'application.
- **Héritage** : `BaseDAO` (classe abstraite) factorise les méthodes
  génériques `get_all`, `get_by_id`, `delete_by_id`, héritées par
  `FournisseurDAO`, `ProduitDAO` et `CommandeDAO`.
- **Requêtes paramétrées** : toutes les requêtes SQL utilisent des
  paramètres (`%s`) pour éviter les injections SQL.
- **Transactions** : `commit()` / `rollback()` à chaque opération sensible
  pour garantir l'intégrité des données.
- **Gestion des erreurs** : chaque opération sensible est encapsulée dans
  un bloc `try/except`.

## Installation

1. Cloner le dépôt :
   ```bash
   git clone <url-du-depot>
   cd gestion_commandes
   ```
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Créer la base de données MySQL (vide) :
   ```sql
   CREATE DATABASE gestion_commandes;
   ```
4. Adapter `database/config.py` avec vos identifiants MySQL.
5. Créer les tables :
   ```bash
   python create_tables.py
   ```
6. (Optionnel) Insérer des données de test :
   ```bash
   python insert_test_data.py
   ```
7. Lancer l'application :
   ```bash
   python main.py
   ```

## Auteurs

Projet réalisé par : *(à compléter avec les membres du groupe)*
