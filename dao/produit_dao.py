
from dao.base_dao import BaseDAO
from database.connexion import DatabaseConnection
from models.produit import Produit


class ProduitDAO(BaseDAO):

    @property
    def table(self):
        return "produit"

    def row_to_objet(self, ligne):
        return Produit(
            id=ligne[0],
            reference=ligne[1],
            designation=ligne[2],
            prix_unitaire=ligne[3],
            stock=ligne[4],
            date_creation=ligne[5],
        )

    def ajouter(self, produit):
        """Insère un nouveau produit en base."""
        db = DatabaseConnection()
        if not db.connect():
            return False
        try:
            sql = """
                INSERT INTO produit (reference, designation, prix_unitaire, stock, date_creation)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                produit.reference,
                produit.designation,
                produit.prix_unitaire,
                produit.stock,
                produit.date_creation,
            )
            ok = db.execute(sql, params)
            if ok:
                db.commit()
                produit.id = db.last_insert_id()
            else:
                db.rollback()
            return ok
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de l'ajout du produit : {e}")
            return False
        finally:
            db.disconnect()

    def modifier(self, produit):
        """Met à jour la désignation, le prix et le stock d'un produit."""
        db = DatabaseConnection()
        if not db.connect():
            return False
        try:
            sql = """
                UPDATE produit
                SET reference = %s, designation = %s, prix_unitaire = %s, stock = %s
                WHERE id = %s
            """
            params = (
                produit.reference,
                produit.designation,
                produit.prix_unitaire,
                produit.stock,
                produit.id,
            )
            ok = db.execute(sql, params)
            if ok:
                db.commit()
            else:
                db.rollback()
            return ok
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la modification du produit : {e}")
            return False
        finally:
            db.disconnect()

    def get_by_reference(self, reference):
        """Recherche un produit par sa référence unique."""
        db = DatabaseConnection()
        if not db.connect():
            return None
        try:
            db.execute("SELECT * FROM produit WHERE reference = %s", (reference,))
            ligne = db.fetchone()
            return self.row_to_objet(ligne) if ligne else None
        except Exception as e:
            print(f"Erreur lors de la recherche par référence : {e}")
            return None
        finally:
            db.disconnect()

    def rechercher_par_designation(self, mot_cle):
        """Recherche les produits dont la désignation contient le mot-clé."""
        db = DatabaseConnection()
        if not db.connect():
            return []
        try:
            sql = "SELECT * FROM produit WHERE designation LIKE %s"
            db.execute(sql, (f"%{mot_cle}%",))
            lignes = db.fetchall()
            return [self.row_to_objet(ligne) for ligne in lignes]
        except Exception as e:
            print(f"Erreur lors de la recherche par désignation : {e}")
            return []
        finally:
            db.disconnect()

    def produits_sous_seuil(self, seuil):
        """Retourne les produits dont le stock est inférieur au seuil donné."""
        db = DatabaseConnection()
        if not db.connect():
            return []
        try:
            db.execute("SELECT * FROM produit WHERE stock < %s", (seuil,))
            lignes = db.fetchall()
            return [self.row_to_objet(ligne) for ligne in lignes]
        except Exception as e:
            print(f"Erreur lors de la recherche des produits sous le seuil : {e}")
            return []
        finally:
            db.disconnect()

    def a_des_commandes(self, produit_id):
        """Vérifie si le produit apparaît dans au moins une ligne de commande."""
        db = DatabaseConnection()
        if not db.connect():
            return True
        try:
            db.execute(
                "SELECT COUNT(*) FROM ligne_commande WHERE produit_id = %s",
                (produit_id,),
            )
            nb = db.fetchone()[0]
            return nb > 0
        except Exception as e:
            print(f"Erreur lors de la vérification des commandes : {e}")
            return True
        finally:
            db.disconnect()

    def supprimer(self, produit_id):
        """Supprime un produit, uniquement s'il n'apparaît dans aucune commande."""
        if self.a_des_commandes(produit_id):
            print("Impossible de supprimer : ce produit apparaît dans une commande.")
            return False
        return self.delete_by_id(produit_id)

    def valeur_totale_stock(self):
        """Calcule la valeur totale du stock (somme de prix_unitaire * stock)."""
        db = DatabaseConnection()
        if not db.connect():
            return 0.0
        try:
            db.execute("SELECT SUM(prix_unitaire * stock) FROM produit")
            resultat = db.fetchone()[0]
            return float(resultat) if resultat is not None else 0.0
        except Exception as e:
            print(f"Erreur lors du calcul de la valeur du stock : {e}")
            return 0.0
        finally:
            db.disconnect()

    def mettre_a_jour_stock(self, produit_id, nouvelle_quantite, db=None):
        """Met à jour le stock d'un produit (utilisé par CommandeDAO dans une transaction)."""
        connexion_locale = db is None
        if connexion_locale:
            db = DatabaseConnection()
            if not db.connect():
                return False
        try:
            ok = db.execute(
                "UPDATE produit SET stock = %s WHERE id = %s",
                (nouvelle_quantite, produit_id),
            )
            if connexion_locale:
                if ok:
                    db.commit()
                else:
                    db.rollback()
            return ok
        except Exception as e:
            if connexion_locale:
                db.rollback()
            print(f"Erreur lors de la mise à jour du stock : {e}")
            return False
        finally:
            if connexion_locale:
                db.disconnect()
