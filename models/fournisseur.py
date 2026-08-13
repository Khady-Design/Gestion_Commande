from datetime import date


class Fournisseur:
    """Représente un fournisseur de l'entreprise."""

    def __init__(self, id=None, code="", raison_sociale="", email="",
                 telephone="", adresse="", date_creation=None):
        self.id = id
        self.code = code
        self.raison_sociale = raison_sociale
        self.email = email
        self.telephone = telephone
        self.adresse = adresse
        self.date_creation = date_creation or date.today()

    def __str__(self):
        return (f"{self.id} - {self.code} - {self.raison_sociale} - "
                f"{self.email} - {self.telephone}")

    def afficher(self):
        print(f"ID              : {self.id}")
        print(f"CODE            : {self.code}")
        print(f"RAISON SOCIALE  : {self.raison_sociale}")
        print(f"EMAIL           : {self.email}")
        print(f"TELEPHONE       : {self.telephone}")
        print(f"ADRESSE         : {self.adresse}")
        print(f"DATE DE CREATION: {self.date_creation}")
