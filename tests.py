from json import dumps


def run_input():
    import input
    import main

    chargeur = input.Chargeur(main.FICHIER_IN)
    print(dumps(chargeur.recuperer()))


def run_main():
    import main


if __name__ == "__main__":
    run_input()
