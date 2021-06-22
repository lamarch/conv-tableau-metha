from Window import Window
import sys
import os.path
from os import mkdir

from datetime import datetime
import tkinter.messagebox as messagebox


def AJD(): return str(datetime.now()).replace(':', '-').replace('/', '-')


FICHIER_IN = './donnees/Pesées terminées.csv'
FICHIER_MOD = './donnees/recapitulatif 21.xlsx'
FICHIER_OUT = f'./donnees/out-{AJD()}.xlsx'


def panic(*args):
    import sys

    msg = '\n'.join(map(lambda a: str(a), args))

    messagebox.showerror(
        'Erreur critique !', f'Une erreur critique est survenue, demandez de l\'aide à l\'assistance ! Ne pas supprimer le fichier "erreur.txt".\n\n\n')
    with open('erreur.txt', 'w', encoding='UTF8') as f:
        f.write(msg)

    sys.exit(0)


def main():
    window = Window()

    logs_path = f'./logs/{AJD()}.txt'
    logs_dir = os.path.dirname(logs_path)
    if not os.path.isdir(logs_dir):
        mkdir(logs_dir)

    print(os.path.abspath(logs_path))
    with open(logs_path, 'x', encoding='UTF8', buffering=1) as out:
        sys.stdout = sys.stderr = out
        window.mainloop()

    window.ask_stop()
    window.stop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        panic(str(e))
