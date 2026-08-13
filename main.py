"""Point d'entrée principal de l'application de gestion des commandes fournisseurs."""

from menu.interface import Interface


def main():
    print("=" * 60)
    print("  APPLICATION DE GESTION DES COMMANDES FOURNISSEURS")
    print("=" * 60)
    interface = Interface()
    interface.menu_principal()


if __name__ == "__main__":
    main()
