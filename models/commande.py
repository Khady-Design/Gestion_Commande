from datetime import date

# Statuts possibles d'une commande, dans leur ordre de progression normal
STATUTS = ["EN_ATTENTE", "VALIDEE", "LIVREE"]
STATUT_ANNULEE = "ANNULEE"


class Commande:
    """Représente une commande passée à un fournisseur."""

    def __init__(self, id=None, numero="", date_commande=None, fournisseur_id=None,
                 montant_total=0.0, statut="EN_ATTENTE", date_creation=None):
        self.id = id
        self.numero = numero
        self.date_commande = date_commande or date.today()
        self.fournisseur_id = fournisseur_id
        self.montant_total = float(montant_total)
        self.statut = statut
        self.date_creation = date_creation or date.today()
        # Les lignes ne sont pas stockées en base dans cette table,
        # mais on les garde en mémoire pour faciliter l'affichage.
        self.lignes = []

    def __str__(self):
        return (f"{self.id} - {self.numero} - {self.date_commande} - "
                f"fournisseur:{self.fournisseur_id} - {self.montant_total:.2f} FCFA - "
                f"[{self.statut}]")

    def afficher(self):
        print(f"ID              : {self.id}")
        print(f"NUMERO          : {self.numero}")
        print(f"DATE COMMANDE   : {self.date_commande}")
        print(f"FOURNISSEUR ID  : {self.fournisseur_id}")
        print(f"MONTANT TOTAL   : {self.montant_total:.2f} FCFA")
        print(f"STATUT          : {self.statut}")
        print(f"DATE DE CREATION: {self.date_creation}")


class LigneCommande:
    """Représente une ligne (un produit) au sein d'une commande."""

    def __init__(self, id=None, commande_id=None, produit_id=None,
                 quantite=0, prix_unitaire=0.0):
        self.id = id
        self.commande_id = commande_id
        self.produit_id = produit_id
        self.quantite = int(quantite)
        self.prix_unitaire = float(prix_unitaire)

    def sous_total(self):
        return self.quantite * self.prix_unitaire

    def __str__(self):
        return (f"produit:{self.produit_id} - qte:{self.quantite} - "
                f"prix u.:{self.prix_unitaire:.2f} - sous-total:{self.sous_total():.2f}")
