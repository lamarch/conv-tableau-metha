from datetime import datetime
from json import dumps

POIDS = 6
DATE = 14
PRODUIT = 19
CODE_CLIENT = 22

ACCP_ANNEE = 2021

LIENS_PRODUITS = {
    "Fumier bovins C2": 0,
    "Fumier bovins mou C2": 1,
    "Lisiers C2": 2,
    "Fumier ovins C2": 3,
    "DIGESTAT C2": 4,
}

FORMAT_IN_DATE = "%d/%m/%Y %H:%M:%S"
FORMAT_OUT_DATE = "%m %y"


def lire_donnees(nom_fichier: str):
    from csv import reader

    print(f'Chargement fichier données : "{nom_fichier}"\n')
    with open(nom_fichier, encoding='UTF8') as fichier:
        reader = reader(fichier, delimiter=';')

        for i, ligne in enumerate(reader):
            if i > 0 and ligne is not None:
                yield ligne


def lire_date(date: str) -> datetime:

    date_p = datetime.strptime(
        date, FORMAT_IN_DATE)

    return date_p


class Chargeur:
    def __init__(self, nom_fichier: str) -> None:
        self.nom_fichier = nom_fichier

    def recuperer(self):
        return self.convertir(lire_donnees(self.nom_fichier))

    def convertir(self, donnees):
        resultats = {}

        for index, ligne in enumerate(donnees):

            code_client = ligne[CODE_CLIENT]
            date = ligne[DATE]
            produit = ligne[PRODUIT]
            poids = ligne[POIDS]

            mois = None

            try:
                code_client = int(code_client)
            except:
                print(f'{index} - ERREUR : Code client invalide : "{code_client}".')
                continue

            try:
                date_p = lire_date(date)
                mois = date_p.month
                if date_p.year != ACCP_ANNEE:
                    print('Intervalle de date non respecté,')
                    raise ValueError(date)
                if date_p.hour == 00:
                    print(f'Heure minuit,')
                    raise ValueError(date)
            except:
                print(
                    f'{index} - ERREUR : Impossible de lire la date : "{date}".')
                continue

            try:
                produit = LIENS_PRODUITS[produit]
            except:
                print(f'{index} - ERREUR : Produit inconnu : "{produit}".')
                continue

            try:
                poids = float(poids)
            except:
                print(f'{index} - ERREUR : Impossible de lire le poids : "{poids}".')
                continue

            # print(f'Produit : {code_client} {mois} {produit} {poids}')

            # yield (code_client, date, produit, poids)

            if not code_client in resultats:
                resultats[code_client] = {}

            if not produit in resultats[code_client]:
                resultats[code_client][produit] = {}

            if not mois in resultats[code_client][produit]:
                resultats[code_client][produit][mois] = 0

            resultats[code_client][produit][mois] += poids

        self.resultats = resultats
        print(dumps(resultats, indent=2))
