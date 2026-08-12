import os

from dao.fournisseur_dao import FournisseurDAO
from dao.produit_dao import ProduitDAO
from dao.commande_dao import CommandeDAO
from models.fournisseur import Fournisseur
from models.produit import Produit
from models.commande import Commande, LigneCommande


class Interface:
    def __init__(self):
        self.fournisseur_dao = FournisseurDAO()
        self.produit_dao = ProduitDAO()
        self.commande_dao = CommandeDAO()

    # ---------------------------- Utilitaires ----------------------------

    def cls(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):
        input("\nAppuyez sur ENTREE pour continuer...")

    def lire_entier(self, message):
        """Demande un entier à l'utilisateur en gérant les erreurs de saisie."""
        while True:
            valeur = input(message)
            try:
                return int(valeur)
            except ValueError:
                print("Veuillez saisir un nombre entier valide.")

    def lire_decimal(self, message):
        """Demande un nombre décimal en gérant les erreurs de saisie."""
        while True:
            valeur = input(message)
            try:
                return float(valeur)
            except ValueError:
                print("Veuillez saisir un nombre valide (ex : 1500.50).")

    # ------------------------------ Menu racine ------------------------------

    def menu_principal(self):
        while True:
            self.cls()
            print("===================== MENU PRINCIPAL =====================")
            print("1. Gestion des fournisseurs")
            print("2. Gestion des produits")
            print("3. Gestion des commandes")
            print("4. Rapports et statistiques")
            print("0. Quitter")
            print("============================================================")

            choix = input("Votre choix : ")

            if choix == "1":
                self.menu_fournisseur()
            elif choix == "2":
                self.menu_produit()
            elif choix == "3":
                self.menu_commande()
            elif choix == "4":
                self.menu_rapports()
            elif choix == "0":
                print("Au revoir !")
                break
            else:
                print("Choix invalide.")
                self.pause()

    # --------------------------- Menu fournisseurs ---------------------------

    def menu_fournisseur(self):
        while True:
            self.cls()
            print("=================== GESTION DES FOURNISSEURS ===================")
            print("1. Afficher tous les fournisseurs")
            print("2. Ajouter un fournisseur")
            print("3. Afficher le détail d'un fournisseur")
            print("4. Modifier un fournisseur")
            print("5. Supprimer un fournisseur")
            print("6. Rechercher un fournisseur (code ou raison sociale)")
            print("0. Retour")

            choix = input("Votre choix : ")

            if choix == "1":
                self.cls()
                fournisseurs = self.fournisseur_dao.get_all()
                if not fournisseurs:
                    print("Aucun fournisseur enregistré.")
                else:
                    for f in fournisseurs:
                        print(f)
                self.pause()

            elif choix == "2":
                self.cls()
                print("---- Ajouter un fournisseur ----")
                code = input("Code (ex : F004) : ")
                raison_sociale = input("Raison sociale : ")
                email = input("Email : ")
                telephone = input("Téléphone : ")
                adresse = input("Adresse : ")
                fournisseur = Fournisseur(
                    code=code, raison_sociale=raison_sociale,
                    email=email, telephone=telephone, adresse=adresse,
                )
                if self.fournisseur_dao.ajouter(fournisseur):
                    print("Fournisseur ajouté avec succès.")
                else:
                    print("Échec de l'ajout (code déjà utilisé ?).")
                self.pause()

            elif choix == "3":
                self.cls()
                identifiant = input("ID ou code du fournisseur : ")
                fournisseur = self._trouver_fournisseur(identifiant)
                if fournisseur:
                    fournisseur.afficher()
                else:
                    print("Fournisseur introuvable.")
                self.pause()

            elif choix == "4":
                self.cls()
                identifiant = input("ID ou code du fournisseur à modifier : ")
                fournisseur = self._trouver_fournisseur(identifiant)
                if fournisseur:
                    fournisseur.raison_sociale = input(
                        f"Raison sociale [{fournisseur.raison_sociale}] : "
                    ) or fournisseur.raison_sociale
                    fournisseur.email = input(f"Email [{fournisseur.email}] : ") or fournisseur.email
                    fournisseur.telephone = input(
                        f"Téléphone [{fournisseur.telephone}] : "
                    ) or fournisseur.telephone
                    fournisseur.adresse = input(
                        f"Adresse [{fournisseur.adresse}] : "
                    ) or fournisseur.adresse
                    if self.fournisseur_dao.modifier(fournisseur):
                        print("Fournisseur modifié avec succès.")
                    else:
                        print("Échec de la modification.")
                else:
                    print("Fournisseur introuvable.")
                self.pause()

            elif choix == "5":
                self.cls()
                identifiant = input("ID ou code du fournisseur à supprimer : ")
                fournisseur = self._trouver_fournisseur(identifiant)
                if fournisseur:
                    if self.fournisseur_dao.supprimer(fournisseur.id):
                        print("Fournisseur supprimé avec succès.")
                else:
                    print("Fournisseur introuvable.")
                self.pause()

            elif choix == "6":
                self.cls()
                mot_cle = input("Code exact ou mot-clé de raison sociale : ")
                resultat = self.fournisseur_dao.get_by_code(mot_cle)
                resultats = [resultat] if resultat else \
                    self.fournisseur_dao.rechercher_par_raison_sociale(mot_cle)
                if resultats:
                    for f in resultats:
                        print(f)
                else:
                    print("Aucun fournisseur trouvé.")
                self.pause()

            elif choix == "0":
                return
            else:
                print("Choix invalide.")
                self.pause()

    def _trouver_fournisseur(self, identifiant):
        """Trouve un fournisseur par ID numérique ou par code."""
        if identifiant.isdigit():
            return self.fournisseur_dao.get_by_id(int(identifiant))
        return self.fournisseur_dao.get_by_code(identifiant)

    # ----------------------------- Menu produits -----------------------------

    def menu_produit(self):
        while True:
            self.cls()
            print("====================== GESTION DES PRODUITS ======================")
            print("1. Afficher tous les produits")
            print("2. Ajouter un produit")
            print("3. Afficher le détail d'un produit")
            print("4. Modifier un produit")
            print("5. Supprimer un produit")
            print("6. Rechercher un produit par désignation")
            print("7. Alerte réapprovisionnement (stock sous un seuil)")
            print("0. Retour")

            choix = input("Votre choix : ")

            if choix == "1":
                self.cls()
                produits = self.produit_dao.get_all()
                if not produits:
                    print("Aucun produit enregistré.")
                else:
                    for p in produits:
                        print(p)
                self.pause()

            elif choix == "2":
                self.cls()
                print("---- Ajouter un produit ----")
                reference = input("Référence (ex : REF006) : ")
                designation = input("Désignation : ")
                prix = self.lire_decimal("Prix unitaire : ")
                stock = self.lire_entier("Stock initial : ")
                produit = Produit(
                    reference=reference, designation=designation,
                    prix_unitaire=prix, stock=stock,
                )
                if self.produit_dao.ajouter(produit):
                    print("Produit ajouté avec succès.")
                else:
                    print("Échec de l'ajout (référence déjà utilisée ?).")
                self.pause()

            elif choix == "3":
                self.cls()
                identifiant = input("ID ou référence du produit : ")
                produit = self._trouver_produit(identifiant)
                if produit:
                    produit.afficher()
                else:
                    print("Produit introuvable.")
                self.pause()

            elif choix == "4":
                self.cls()
                identifiant = input("ID ou référence du produit à modifier : ")
                produit = self._trouver_produit(identifiant)
                if produit:
                    designation = input(f"Désignation [{produit.designation}] : ")
                    produit.designation = designation or produit.designation

                    prix_saisi = input(f"Prix unitaire [{produit.prix_unitaire}] : ")
                    if prix_saisi:
                        try:
                            produit.prix_unitaire = float(prix_saisi)
                        except ValueError:
                            print("Prix invalide, valeur conservée.")

                    stock_saisi = input(f"Stock [{produit.stock}] : ")
                    if stock_saisi:
                        try:
                            produit.stock = int(stock_saisi)
                        except ValueError:
                            print("Stock invalide, valeur conservée.")

                    if self.produit_dao.modifier(produit):
                        print("Produit modifié avec succès.")
                    else:
                        print("Échec de la modification.")
                else:
                    print("Produit introuvable.")
                self.pause()

            elif choix == "5":
                self.cls()
                identifiant = input("ID ou référence du produit à supprimer : ")
                produit = self._trouver_produit(identifiant)
                if produit:
                    if self.produit_dao.supprimer(produit.id):
                        print("Produit supprimé avec succès.")
                else:
                    print("Produit introuvable.")
                self.pause()

            elif choix == "6":
                self.cls()
                mot_cle = input("Mot-clé de désignation : ")
                produits = self.produit_dao.rechercher_par_designation(mot_cle)
                if produits:
                    for p in produits:
                        print(p)
                else:
                    print("Aucun produit trouvé.")
                self.pause()

            elif choix == "7":
                self.cls()
                seuil = self.lire_entier("Seuil d'alerte : ")
                produits = self.produit_dao.produits_sous_seuil(seuil)
                if produits:
                    print(f"Produits avec un stock inférieur à {seuil} :")
                    for p in produits:
                        print(p)
                else:
                    print("Aucun produit sous le seuil indiqué.")
                self.pause()

            elif choix == "0":
                return
            else:
                print("Choix invalide.")
                self.pause()

    def _trouver_produit(self, identifiant):
        """Trouve un produit par ID numérique ou par référence."""
        if identifiant.isdigit():
            return self.produit_dao.get_by_id(int(identifiant))
        return self.produit_dao.get_by_reference(identifiant)

    # ---------------------------- Menu commandes ----------------------------

    def menu_commande(self):
        while True:
            self.cls()
            print("===================== GESTION DES COMMANDES =====================")
            print("1. Afficher toutes les commandes")
            print("2. Créer une nouvelle commande")
            print("3. Afficher le détail d'une commande")
            print("4. Changer le statut d'une commande")
            print("5. Annuler une commande")
            print("6. Supprimer une commande")
            print("0. Retour")

            choix = input("Votre choix : ")

            if choix == "1":
                self.cls()
                commandes = self.commande_dao.get_all()
                if not commandes:
                    print("Aucune commande enregistrée.")
                else:
                    for c in commandes:
                        print(c)
                self.pause()

            elif choix == "2":
                self._creer_commande()

            elif choix == "3":
                self.cls()
                identifiant = input("ID ou numéro de la commande : ")
                commande = self._trouver_commande(identifiant)
                if commande:
                    commande = self.commande_dao.detail_commande(commande.id)
                    commande.afficher()
                    print("\nLignes de la commande :")
                    for ligne in commande.lignes:
                        produit = self.produit_dao.get_by_id(ligne.produit_id)
                        nom = produit.designation if produit else f"id:{ligne.produit_id}"
                        print(f"  - {nom} : {ligne}")
                else:
                    print("Commande introuvable.")
                self.pause()

            elif choix == "4":
                self.cls()
                identifiant = input("ID ou numéro de la commande : ")
                commande = self._trouver_commande(identifiant)
                if commande:
                    print(f"Statut actuel : {commande.statut}")
                    print("Statuts possibles : VALIDEE, LIVREE")
                    nouveau = input("Nouveau statut : ").strip().upper()
                    if self.commande_dao.changer_statut(commande.id, nouveau):
                        print("Statut mis à jour avec succès.")
                else:
                    print("Commande introuvable.")
                self.pause()

            elif choix == "5":
                self.cls()
                identifiant = input("ID ou numéro de la commande à annuler : ")
                commande = self._trouver_commande(identifiant)
                if commande:
                    if self.commande_dao.changer_statut(commande.id, "ANNULEE"):
                        print("Commande annulée avec succès.")
                else:
                    print("Commande introuvable.")
                self.pause()

            elif choix == "6":
                self.cls()
                identifiant = input("ID ou numéro de la commande à supprimer : ")
                commande = self._trouver_commande(identifiant)
                if commande:
                    if self.commande_dao.supprimer_commande(commande.id):
                        print("Commande supprimée avec succès.")
                else:
                    print("Commande introuvable.")
                self.pause()

            elif choix == "0":
                return
            else:
                print("Choix invalide.")
                self.pause()

    def _trouver_commande(self, identifiant):
        """Trouve une commande par ID numérique ou par numéro."""
        if identifiant.isdigit():
            return self.commande_dao.get_by_id(int(identifiant))
        return self.commande_dao.get_by_numero(identifiant)

    def _creer_commande(self):
        self.cls()
        print("---- Créer une nouvelle commande ----")
        numero = input("Numéro de commande (ex : CMD003) : ")

        code_fournisseur = input("Code du fournisseur : ")
        fournisseur = self.fournisseur_dao.get_by_code(code_fournisseur)
        if not fournisseur:
            print("Fournisseur introuvable. Création annulée.")
            self.pause()
            return

        lignes = []
        while True:
            ref_produit = input("Référence produit (laisser vide pour terminer) : ")
            if not ref_produit:
                break
            produit = self.produit_dao.get_by_reference(ref_produit)
            if not produit:
                print("Produit introuvable.")
                continue
            quantite = self.lire_entier(f"Quantité de '{produit.designation}' : ")
            lignes.append(LigneCommande(produit_id=produit.id, quantite=quantite))

        if not lignes:
            print("Aucun produit ajouté, commande annulée.")
            self.pause()
            return

        commande = Commande(numero=numero, fournisseur_id=fournisseur.id)
        if self.commande_dao.creer_commande(commande, lignes):
            print(f"Commande créée avec succès. Montant total : {commande.montant_total:.2f} FCFA")
        else:
            print("Échec de la création de la commande.")
        self.pause()

    # --------------------------- Menu rapports ---------------------------

    def menu_rapports(self):
        while True:
            self.cls()
            print("======================= RAPPORTS ET STATISTIQUES =======================")
            print("1. Commandes par fournisseur")
            print("2. Commandes en attente de validation")
            print("3. Valeur totale du stock")
            print("4. Top 5 des produits les plus commandés")
            print("5. Chiffre d'affaires total")
            print("0. Retour")

            choix = input("Votre choix : ")

            if choix == "1":
                self.cls()
                code = input("Code du fournisseur : ")
                fournisseur = self.fournisseur_dao.get_by_code(code)
                if fournisseur:
                    commandes = self.commande_dao.commandes_par_fournisseur(fournisseur.id)
                    if commandes:
                        for c in commandes:
                            print(c)
                    else:
                        print("Aucune commande pour ce fournisseur.")
                else:
                    print("Fournisseur introuvable.")
                self.pause()

            elif choix == "2":
                self.cls()
                commandes = self.commande_dao.commandes_en_attente()
                if commandes:
                    for c in commandes:
                        print(c)
                else:
                    print("Aucune commande en attente.")
                self.pause()

            elif choix == "3":
                self.cls()
                valeur = self.produit_dao.valeur_totale_stock()
                print(f"Valeur totale du stock : {valeur:.2f} FCFA")
                self.pause()

            elif choix == "4":
                self.cls()
                top = self.commande_dao.top_produits_commandes(5)
                if top:
                    print("Top 5 des produits les plus commandés :")
                    for rang, (designation, quantite) in enumerate(top, start=1):
                        print(f"{rang}. {designation} - {quantite} unités commandées")
                else:
                    print("Aucune donnée disponible.")
                self.pause()

            elif choix == "5":
                self.cls()
                ca = self.commande_dao.chiffre_affaires_total()
                print(f"Chiffre d'affaires total (commandes validées et livrées) : {ca:.2f} FCFA")
                self.pause()

            elif choix == "0":
                return
            else:
                print("Choix invalide.")
                self.pause()
