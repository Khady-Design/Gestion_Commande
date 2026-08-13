from datetime import date


class Produit:
    """Représente un produit vendu/géré par l'entreprise."""

    def __init__(self, id=None, reference="", designation="",
                 prix_unitaire=0.0, stock=0, date_creation=None):
        self.id = id
        self.reference = reference
        self.designation = designation
        self.prix_unitaire = float(prix_unitaire)
        self.stock = int(stock)
        self.date_creation = date_creation or date.today()

    def __str__(self):
        return (f"{self.id} - {self.reference} - {self.designation} - "
                f"{self.prix_unitaire:.2f} FCFA - stock: {self.stock}")

    def afficher(self):
        print(f"ID              : {self.id}")
        print(f"REFERENCE       : {self.reference}")
        print(f"DESIGNATION     : {self.designation}")
        print(f"PRIX UNITAIRE   : {self.prix_unitaire:.2f} FCFA")
        print(f"STOCK           : {self.stock}")
        print(f"DATE DE CREATION: {self.date_creation}")

    def valeur_stock(self):
        """Retourne la valeur totale du stock pour ce produit."""
        return self.prix_unitaire * self.stock
