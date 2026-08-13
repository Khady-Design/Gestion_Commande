"""DAO pour la gestion des fournisseurs (CRUD complet)."""

from dao.base_dao import BaseDAO
from database.connexion import DatabaseConnection
from models.fournisseur import Fournisseur


class FournisseurDAO(BaseDAO):

    @property
    def table(self):
        return "fournisseur"

    def row_to_objet(self, ligne):
        return Fournisseur(
            id=ligne[0],
            code=ligne[1],
            raison_sociale=ligne[2],
            email=ligne[3],
            telephone=ligne[4],
            adresse=ligne[5],
            date_creation=ligne[6],
        )

    def ajouter(self, fournisseur):
        """Insère un nouveau fournisseur en base."""
        db = DatabaseConnection()
        if not db.connect():
            return False
        try:
            sql = """
                INSERT INTO fournisseur (code, raison_sociale, email, telephone, adresse, date_creation)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                fournisseur.code,
                fournisseur.raison_sociale,
                fournisseur.email,
                fournisseur.telephone,
                fournisseur.adresse,
                fournisseur.date_creation,
            )
            ok = db.execute(sql, params)
            if ok:
                db.commit()
                fournisseur.id = db.last_insert_id()
            else:
                db.rollback()
            return ok
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de l'ajout du fournisseur : {e}")
            return False
        finally:
            db.disconnect()

    def modifier(self, fournisseur):
        """Met à jour les informations d'un fournisseur existant."""
        db = DatabaseConnection()
        if not db.connect():
            return False
        try:
            sql = """
                UPDATE fournisseur
                SET code = %s, raison_sociale = %s, email = %s,
                    telephone = %s, adresse = %s
                WHERE id = %s
            """
            params = (
                fournisseur.code,
                fournisseur.raison_sociale,
                fournisseur.email,
                fournisseur.telephone,
                fournisseur.adresse,
                fournisseur.id,
            )
            ok = db.execute(sql, params)
            if ok:
                db.commit()
            else:
                db.rollback()
            return ok
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la modification du fournisseur : {e}")
            return False
        finally:
            db.disconnect()

    def get_by_code(self, code):
        """Recherche un fournisseur par son code unique."""
        db = DatabaseConnection()
        if not db.connect():
            return None
        try:
            db.execute("SELECT * FROM fournisseur WHERE code = %s", (code,))
            ligne = db.fetchone()
            return self.row_to_objet(ligne) if ligne else None
        except Exception as e:
            print(f"Erreur lors de la recherche par code : {e}")
            return None
        finally:
            db.disconnect()

    def rechercher_par_raison_sociale(self, mot_cle):
        """Recherche les fournisseurs dont la raison sociale contient le mot-clé."""
        db = DatabaseConnection()
        if not db.connect():
            return []
        try:
            sql = "SELECT * FROM fournisseur WHERE raison_sociale LIKE %s"
            db.execute(sql, (f"%{mot_cle}%",))
            lignes = db.fetchall()
            return [self.row_to_objet(ligne) for ligne in lignes]
        except Exception as e:
            print(f"Erreur lors de la recherche par raison sociale : {e}")
            return []
        finally:
            db.disconnect()

    def a_des_commandes(self, fournisseur_id):
        """Vérifie si le fournisseur a au moins une commande associée."""
        db = DatabaseConnection()
        if not db.connect():
            return True  # par sécurité, on bloque la suppression en cas de doute
        try:
            db.execute(
                "SELECT COUNT(*) FROM commande WHERE fournisseur_id = %s",
                (fournisseur_id,),
            )
            nb = db.fetchone()[0]
            return nb > 0
        except Exception as e:
            print(f"Erreur lors de la vérification des commandes : {e}")
            return True
        finally:
            db.disconnect()

    def supprimer(self, fournisseur_id):
        """Supprime un fournisseur, uniquement s'il n'a aucune commande associée."""
        if self.a_des_commandes(fournisseur_id):
            print("Impossible de supprimer : ce fournisseur a des commandes associées.")
            return False
        return self.delete_by_id(fournisseur_id)
