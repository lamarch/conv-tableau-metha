import openpyxl

LIGNE_HAUT = 7
COLONNE_DROITE = 9

MAX_MOIS = 12
MAX_PRODUITS = 6
DECALAGE_CLIENT = 1


class Exporteur:
    def __init__(self, nom_fichier_modele: str, nom_fichier_sortie: str) -> None:
        self.nom_fichier_modele = nom_fichier_modele
        self.nom_fichier_sortie = nom_fichier_sortie

    def charger(self):
        print(f'Chargement fichier modèle : "{self.nom_fichier_modele}"')
        self.wb = openpyxl.load_workbook(self.nom_fichier_modele)
        self.ws = self.wb.active

    def convertir(self, donnees: dict):

        len_donnees = len(donnees)
        i = 1
        for code_client, produits in donnees.items():
            print(f'Export en cours, client {i}/{len_donnees}...')
            i += 1

            for produit, mois in produits.items():

                for mois, poids in mois.items():

                    ligne = (code_client - 1) * (MAX_PRODUITS +
                                                 DECALAGE_CLIENT) + produit + LIGNE_HAUT
                    colonne = mois + COLONNE_DROITE

                    self.ws.cell(row=ligne, column=colonne, value=poids)

    def sauvegarder(self):
        print(f'Sauvegarde fichier sortie : "{self.nom_fichier_sortie}"\n')
        self.wb.save(self.nom_fichier_sortie)
