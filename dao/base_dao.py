"""
Classe abstraite BaseDAO.
Contient les méthodes génériques (get_all, get_by_id, delete_by_id)
qui seront héritées par tous les DAO spécifiques (Fournisseur, Produit, Commande).
"""

from abc import ABC, abstractmethod

from database.connexion import DatabaseConnection


class BaseDAO(ABC):
    """DAO générique : à hériter dans chaque DAO spécifique."""

    @property
    @abstractmethod
    def table(self):
        """Nom de la table SQL associée à ce DAO (à définir dans la sous-classe)."""
        raise NotImplementedError

    @abstractmethod
    def row_to_objet(self, ligne):
        """Convertit une ligne (tuple) issue de la BD en objet métier."""
        raise NotImplementedError

    def get_all(self):
        """Retourne la liste de tous les enregistrements de la table."""
        db = DatabaseConnection()
        if not db.connect():
            return []
        try:
            db.execute(f"SELECT * FROM {self.table} ORDER BY id")
            lignes = db.fetchall()
            return [self.row_to_objet(ligne) for ligne in lignes]
        except Exception as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return []
        finally:
            db.disconnect()

    def get_by_id(self, id_):
        """Retourne un enregistrement par son id, ou None s'il n'existe pas."""
        db = DatabaseConnection()
        if not db.connect():
            return None
        try:
            db.execute(f"SELECT * FROM {self.table} WHERE id = %s", (id_,))
            ligne = db.fetchone()
            return self.row_to_objet(ligne) if ligne else None
        except Exception as e:
            print(f"Erreur lors de la récupération par id : {e}")
            return None
        finally:
            db.disconnect()

    def delete_by_id(self, id_):
        """Supprime un enregistrement par son id."""
        db = DatabaseConnection()
        if not db.connect():
            return False
        try:
            db.execute(f"DELETE FROM {self.table} WHERE id = %s", (id_,))
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"Erreur lors de la suppression : {e}")
            return False
        finally:
            db.disconnect()
