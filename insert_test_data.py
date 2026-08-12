
from dao.fournisseur_dao import FournisseurDAO
from dao.produit_dao import ProduitDAO
from dao.commande_dao import CommandeDAO
from models.fournisseur import Fournisseur
from models.produit import Produit
from models.commande import Commande, LigneCommande


def inserer_fournisseurs():
    dao = FournisseurDAO()
    fournisseurs = [
        Fournisseur(code="F001", raison_sociale="Sénégal Informatique SARL",
                    email="contact@senegal-info.sn", telephone="338201010",
                    adresse="Avenue Cheikh Anta Diop, Dakar"),
        Fournisseur(code="F002", raison_sociale="Distritech Afrique",
                    email="info@distritech.sn", telephone="338302020",
                    adresse="Zone Industrielle, Dakar"),
        Fournisseur(code="F003", raison_sociale="TechPlus Sénégal",
                    email="contact@techplus.sn", telephone="338403030",
                    adresse="Sacré Cœur 3, Dakar"),
    ]
    for f in fournisseurs:
        if dao.ajouter(f):
            print(f"Fournisseur ajouté : {f.raison_sociale}")
    return dao.get_all()


def inserer_produits():
    dao = ProduitDAO()
    produits = [
        Produit(reference="REF001", designation="Ordinateur portable HP 15", prix_unitaire=350000, stock=20),
        Produit(reference="REF002", designation="Souris sans fil Logitech", prix_unitaire=8500, stock=100),
        Produit(reference="REF003", designation="Clavier mécanique", prix_unitaire=22000, stock=50),
        Produit(reference="REF004", designation="Écran 24 pouces Dell", prix_unitaire=120000, stock=15),
        Produit(reference="REF005", designation="Disque dur externe 1To", prix_unitaire=35000, stock=4),
    ]
    for p in produits:
        if dao.ajouter(p):
            print(f"Produit ajouté : {p.designation}")
    return dao.get_all()


def inserer_commandes(fournisseurs, produits):
    dao = CommandeDAO()

    commande1 = Commande(numero="CMD001", fournisseur_id=fournisseurs[0].id)
    lignes1 = [
        LigneCommande(produit_id=produits[0].id, quantite=2),
        LigneCommande(produit_id=produits[1].id, quantite=5),
    ]
    if dao.creer_commande(commande1, lignes1):
        print(f"Commande créée : {commande1.numero}")

    commande2 = Commande(numero="CMD002", fournisseur_id=fournisseurs[1].id)
    lignes2 = [
        LigneCommande(produit_id=produits[3].id, quantite=3),
    ]
    if dao.creer_commande(commande2, lignes2):
        print(f"Commande créée : {commande2.numero}")
        # On valide directement cette commande pour avoir un exemple de
        # commande VALIDEE avec stock décrémenté.
        dao.changer_statut(commande2.id, "VALIDEE")


def main():
    print("Insertion des données de test...")
    fournisseurs = inserer_fournisseurs()
    produits = inserer_produits()
    inserer_commandes(fournisseurs, produits)
    print("Terminé.")


if __name__ == "__main__":
    main()
