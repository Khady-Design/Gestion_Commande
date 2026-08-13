"""
Module de connexion à la base de données.
Implémente le pattern Singleton : une seule instance de connexion
est partagée par toute l'application.
"""

from database.config import TYPE_BD, MYSQL, POSTGRES


class DatabaseConnection:
    """Connexion unique (Singleton) à la base de données."""

    _instance = None

    def __new__(cls):
        # Si aucune instance n'existe encore, on la crée une seule fois
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
            cls._instance.cursor = None
        return cls._instance

    def connect(self):
        """Ouvre la connexion à la base de données si elle n'est pas déjà active."""
        try:
            # Si une connexion est déjà ouverte, on la réutilise
            if self.connection is not None and self.connection.is_connected():
                return True

            if TYPE_BD == "mysql":
                import mysql.connector
                self.connection = mysql.connector.connect(
                    host=MYSQL["host"],
                    port=MYSQL["port"],
                    database=MYSQL["database"],
                    user=MYSQL["user"],
                    password=MYSQL["password"],
                )
                self.cursor = self.connection.cursor()
                return True

            elif TYPE_BD == "postgres":
                import psycopg2
                self.connection = psycopg2.connect(
                    host=POSTGRES["host"],
                    port=POSTGRES["port"],
                    dbname=POSTGRES["database"],
                    user=POSTGRES["user"],
                    password=POSTGRES["password"],
                )
                self.cursor = self.connection.cursor()
                return True

            print("Type de base de données non supporté")
            return False

        except Exception as e:
            print(f"Erreur de connexion : {e}")
            return False

    def disconnect(self):
        """Ferme le curseur et la connexion."""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            print(f"Erreur lors de la fermeture : {e}")
        finally:
            self.connection = None
            self.cursor = None

    def commit(self):
        """Valide la transaction en cours."""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Annule la transaction en cours en cas d'erreur."""
        if self.connection:
            self.connection.rollback()

    def execute(self, query, params=None):
        """Exécute une requête SQL paramétrée (protège contre les injections SQL)."""
        try:
            self.cursor.execute(query, params or ())
            return True
        except Exception as e:
            print(f"Erreur d'exécution de la requête : {e}")
            return False

    def executemany(self, query, params_list):
        """Exécute une même requête pour une liste de paramètres."""
        try:
            self.cursor.executemany(query, params_list)
            return True
        except Exception as e:
            print(f"Erreur d'exécution multiple : {e}")
            return False

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def last_insert_id(self):
        """Retourne l'id généré par la dernière insertion (auto-incrément)."""
        return self.cursor.lastrowid
