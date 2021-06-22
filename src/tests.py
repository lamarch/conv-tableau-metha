from json import dumps


def run_input():

    chargeur = input.Chargeur(main.FICHIER_IN)
    print(dumps(chargeur.recuperer()))


def run_main():


if __name__ == "__main__":
    run_input()
