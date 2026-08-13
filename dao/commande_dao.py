"""DAO pour la gestion des commandes et de leurs lignes."""

from dao.base_dao import BaseDAO
from dao.produit_dao import ProduitDAO
from database.connexion import DatabaseConnection
from models.commande import Commande, LigneCommande, STATUTS, STATUT_ANNULEE


class CommandeDAO(BaseDAO):

    @property
    def table(self):
        return "commande"

    def row_to_objet(self, ligne):
        return Commande(
            id=ligne[0],
            numero=ligne[1],
            date_commande=ligne[2],
            fournisseur_id=ligne[3],
            montant_total=ligne[4],
            statut=ligne[5],
            date_creation=ligne[6],
        )

    def get_by_numero(self, numero):
        """Recherche une commande par son numéro unique."""
        db = DatabaseConnection()
        if not db.connect():
            return None
        try:
            db.execute("SELECT * FROM commande WHERE numero = %s", (numero,))
            ligne = db.fetchone()
            return self.row_to_objet(ligne) if ligne else None
        except Exception as e:
            print(f"Erreur lors de la recherche par numéro : {e}")
            return None
        finally:
            db.disconnect()

    def creer_commande(self, commande, lignes):
        """
        Crée une commande avec ses lignes.
        `lignes` est une liste de LigneCommande (produit_id, quantite, prix_unitaire).
        Vérifie la disponibilité du stock avant insertion (le stock n'est pas
        encore décrémenté : il ne le sera qu'à la validation de la commande).
        Calcule automatiquement le montant total à partir des lignes.
        """
        if not lignes:
            print("Impossible de créer une commande sans aucune ligne de produit.")
            return False

        produit_dao = ProduitDAO()

        # Vérification de la disponibilité en stock pour chaque ligne
        for ligne in lignes:
            produit = produit_dao.get_by_id(ligne.produit_id)
            if produit is None:
                print(f"Produit introuvable (id={ligne.produit_id}).")
                return False
            if ligne.quantite > produit.stock:
                print(
                    f"Stock insuffisant pour '{produit.designation}' "
                    f"(demandé : {ligne.quantite}, disponible : {produit.stock})."
                )
                return False
            # On fige le prix unitaire au moment de la commande
            ligne.prix_unitaire = produit.prix_unitaire

        # Calcul automatique du montant total
        commande.montant_total = sum(l.sous_total() for l in lignes)
        commande.statut = "EN_ATTENTE"

        db = DatabaseConnection()
        if not db.connect():
            return False
        try:
            sql_commande = """
                INSERT INTO commande
                    (numero, date_commande, fournisseur_id, montant_total, statut, date_creation)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            ok = db.execute(sql_commande, (
                commande.numero,
                commande.date_commande,
                commande.fournisseur_id,
                commande.montant_total,
                commande.statut,
                commande.date_creation,
            ))
            if not ok:
                db.rollback()
                return False

            commande.id = db.last_insert_id()

            sql_ligne = """
                INSERT INTO ligne_commande (commande_id, produit_id, quantite, prix_unitaire)
                VALUES (%s, %s, %s, %s)
            """
            for ligne in lignes:
                ligne.commande_id = commande.id
                ok = db.execute(sql_ligne, (
                    ligne.commande_id,
                    ligne.produit_id,
                    ligne.quantite,
                    ligne.prix_unitaire,
                ))
                if not ok:
                    db.rollback()
                    return False

            db.commit()
            commande.lignes = lignes
            return True

        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la création de la commande : {e}")
            return False
        finally:
            db.disconnect()

    def get_lignes(self, commande_id):
        """Retourne la liste des lignes (produits/quantités) d'une commande."""
        db = DatabaseConnection()
        if not db.connect():
            return []
        try:
            sql = """
                SELECT id, commande_id, produit_id, quantite, prix_unitaire
                FROM ligne_commande
                WHERE commande_id = %s
            """
            db.execute(sql, (commande_id,))
            lignes = db.fetchall()
            return [
                LigneCommande(
                    id=l[0], commande_id=l[1], produit_id=l[2],
                    quantite=l[3], prix_unitaire=l[4],
                )
                for l in lignes
            ]
        except Exception as e:
            print(f"Erreur lors de la récupération des lignes : {e}")
            return []
        finally:
            db.disconnect()

    def detail_commande(self, commande_id):
        """Retourne la commande avec ses lignes chargées."""
        commande = self.get_by_id(commande_id)
        if commande:
            commande.lignes = self.get_lignes(commande_id)
        return commande

    def changer_statut(self, commande_id, nouveau_statut):
        """
        Fait progresser le statut d'une commande :
        EN_ATTENTE -> VALIDEE -> LIVREE (jamais en arrière).
        La validation décrémente le stock ; l'annulation le restitue
        si la commande avait déjà été validée.
        """
        commande = self.get_by_id(commande_id)
        if commande is None:
            print("Commande introuvable.")
            return False

        if commande.statut == STATUT_ANNULEE:
            print("Cette commande est déjà annulée, aucun changement possible.")
            return False
        if commande.statut == "LIVREE":
            print("Cette commande est déjà livrée, aucun changement possible.")
            return False

        if nouveau_statut == STATUT_ANNULEE:
            return self._annuler(commande)

        if nouveau_statut not in STATUTS:
            print("Statut invalide.")
            return False

        index_actuel = STATUTS.index(commande.statut)
        index_nouveau = STATUTS.index(nouveau_statut)

        if index_nouveau <= index_actuel:
            print("Le statut d'une commande ne peut pas reculer ni rester identique.")
            return False

        # Passage à VALIDEE : on vérifie le stock puis on le décrémente
        if nouveau_statut == "VALIDEE":
            if not self._valider_stock(commande):
                return False

        return self._mettre_a_jour_statut(commande_id, nouveau_statut)

    def _valider_stock(self, commande):
        """Vérifie la disponibilité puis décrémente le stock pour chaque ligne."""
        produit_dao = ProduitDAO()
        lignes = self.get_lignes(commande.id)

        produits = {}
        for ligne in lignes:
            produit = produit_dao.get_by_id(ligne.produit_id)
            if produit is None or ligne.quantite > produit.stock:
                nom = produit.designation if produit else ligne.produit_id
                print(f"Stock insuffisant pour valider la commande (produit : {nom}).")
                return False
            produits[ligne.produit_id] = produit

        for ligne in lignes:
            produit = produits[ligne.produit_id]
            nouveau_stock = produit.stock - ligne.quantite
            produit_dao.mettre_a_jour_stock(ligne.produit_id, nouveau_stock)
        return True

    def _annuler(self, commande):
        """Annule une commande et restitue le stock si elle avait été validée."""
        produit_dao = ProduitDAO()
        if commande.statut == "VALIDEE":
            lignes = self.get_lignes(commande.id)
            for ligne in lignes:
                produit = produit_dao.get_by_id(ligne.produit_id)
                if produit:
                    produit_dao.mettre_a_jour_stock(
                        ligne.produit_id, produit.stock + ligne.quantite
                    )
        return self._mettre_a_jour_statut(commande.id, STATUT_ANNULEE)

    def _mettre_a_jour_statut(self, commande_id, statut):
        db = DatabaseConnection()
        if not db.connect():
            return False
        try:
            ok = db.execute(
                "UPDATE commande SET statut = %s WHERE id = %s",
                (statut, commande_id),
            )
            if ok:
                db.commit()
            else:
                db.rollback()
            return ok
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la mise à jour du statut : {e}")
            return False
        finally:
            db.disconnect()

    def supprimer_commande(self, commande_id):
        """Supprime une commande et ses lignes associées."""
        db = DatabaseConnection()
        if not db.connect():
            return False
        try:
            db.execute("DELETE FROM ligne_commande WHERE commande_id = %s", (commande_id,))
            ok = db.execute("DELETE FROM commande WHERE id = %s", (commande_id,))
            if ok:
                db.commit()
            else:
                db.rollback()
            return ok
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression de la commande : {e}")
            return False
        finally:
            db.disconnect()

    # ---------------------- Rapports et statistiques ----------------------

    def commandes_par_fournisseur(self, fournisseur_id):
        """Retourne toutes les commandes passées auprès d'un fournisseur donné."""
        db = DatabaseConnection()
        if not db.connect():
            return []
        try:
            db.execute(
                "SELECT * FROM commande WHERE fournisseur_id = %s ORDER BY date_commande",
                (fournisseur_id,),
            )
            lignes = db.fetchall()
            return [self.row_to_objet(ligne) for ligne in lignes]
        except Exception as e:
            print(f"Erreur lors de la récupération des commandes du fournisseur : {e}")
            return []
        finally:
            db.disconnect()

    def commandes_en_attente(self):
        """Retourne les commandes en attente de validation."""
        db = DatabaseConnection()
        if not db.connect():
            return []
        try:
            db.execute("SELECT * FROM commande WHERE statut = 'EN_ATTENTE'")
            lignes = db.fetchall()
            return [self.row_to_objet(ligne) for ligne in lignes]
        except Exception as e:
            print(f"Erreur lors de la récupération des commandes en attente : {e}")
            return []
        finally:
            db.disconnect()

    def top_produits_commandes(self, limite=5):
        """Retourne les produits les plus commandés (quantité cumulée)."""
        db = DatabaseConnection()
        if not db.connect():
            return []
        try:
            sql = """
                SELECT p.designation, SUM(lc.quantite) AS quantite_totale
                FROM ligne_commande lc
                JOIN produit p ON p.id = lc.produit_id
                GROUP BY p.id, p.designation
                ORDER BY quantite_totale DESC
                LIMIT %s
            """
            db.execute(sql, (limite,))
            return db.fetchall()  # liste de tuples (designation, quantite_totale)
        except Exception as e:
            print(f"Erreur lors du calcul du top produits : {e}")
            return []
        finally:
            db.disconnect()

    def chiffre_affaires_total(self):
        """Calcule le chiffre d'affaires total (commandes VALIDEE + LIVREE)."""
        db = DatabaseConnection()
        if not db.connect():
            return 0.0
        try:
            sql = """
                SELECT SUM(montant_total) FROM commande
                WHERE statut IN ('VALIDEE', 'LIVREE')
            """
            db.execute(sql)
            resultat = db.fetchone()[0]
            return float(resultat) if resultat is not None else 0.0
        except Exception as e:
            print(f"Erreur lors du calcul du chiffre d'affaires : {e}")
            return 0.0
        finally:
            db.disconnect()
