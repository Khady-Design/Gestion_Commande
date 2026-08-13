"""
Script de création des tables de la base de données.
À exécuter une seule fois (ou après suppression de la base) pour
initialiser la structure : fournisseur, produit, commande, ligne_commande.
"""

from database.connexion import DatabaseConnection

TABLES = {
    "fournisseur": """
        CREATE TABLE IF NOT EXISTS fournisseur (
            id INT AUTO_INCREMENT PRIMARY KEY,
            code VARCHAR(20) NOT NULL UNIQUE,
            raison_sociale VARCHAR(150) NOT NULL,
            email VARCHAR(150),
            telephone VARCHAR(30),
            adresse VARCHAR(255),
            date_creation DATE NOT NULL
        )
    """,
    "produit": """
        CREATE TABLE IF NOT EXISTS produit (
            id INT AUTO_INCREMENT PRIMARY KEY,
            reference VARCHAR(20) NOT NULL UNIQUE,
            designation VARCHAR(150) NOT NULL,
            prix_unitaire DECIMAL(12, 2) NOT NULL,
            stock INT NOT NULL DEFAULT 0,
            date_creation DATE NOT NULL
        )
    """,
    "commande": """
        CREATE TABLE IF NOT EXISTS commande (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero VARCHAR(20) NOT NULL UNIQUE,
            date_commande DATE NOT NULL,
            fournisseur_id INT NOT NULL,
            montant_total DECIMAL(14, 2) NOT NULL DEFAULT 0,
            statut ENUM('EN_ATTENTE', 'VALIDEE', 'LIVREE', 'ANNULEE') NOT NULL DEFAULT 'EN_ATTENTE',
            date_creation DATE NOT NULL,
            CONSTRAINT fk_commande_fournisseur
                FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id)
        )
    """,
    "ligne_commande": """
        CREATE TABLE IF NOT EXISTS ligne_commande (
            id INT AUTO_INCREMENT PRIMARY KEY,
            commande_id INT NOT NULL,
            produit_id INT NOT NULL,
            quantite INT NOT NULL,
            prix_unitaire DECIMAL(12, 2) NOT NULL,
            CONSTRAINT fk_ligne_commande
                FOREIGN KEY (commande_id) REFERENCES commande(id),
            CONSTRAINT fk_ligne_produit
                FOREIGN KEY (produit_id) REFERENCES produit(id)
        )
    """,
}

# Ordre de création important : les tables référencées doivent exister avant
# les tables qui les référencent (clés étrangères).
ORDRE_CREATION = ["fournisseur", "produit", "commande", "ligne_commande"]


def creer_tables():
    db = DatabaseConnection()
    if not db.connect():
        print("Impossible de se connecter à la base de données.")
        return

    try:
        for nom_table in ORDRE_CREATION:
            ok = db.execute(TABLES[nom_table])
            if ok:
                print(f"Table '{nom_table}' créée (ou déjà existante).")
            else:
                print(f"Échec de la création de la table '{nom_table}'.")
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Erreur lors de la création des tables : {e}")
    finally:
        db.disconnect()


if __name__ == "__main__":
    creer_tables()
