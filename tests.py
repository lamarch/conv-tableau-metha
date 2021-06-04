def run_input():
    import input
    import main

    chargeur = input.Chargeur(main.FICHIER_IN)
    chargeur.recuperer()


def run_main():
    import main
    

if __name__ == "__main__":
    run_input()
