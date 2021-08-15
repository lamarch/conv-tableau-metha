import sys
import os.path
from os import mkdir
from Window import AppWindow
from utils import panic, today


FICHIER_IN = './donnees/Pesées terminées.csv'
FICHIER_MOD = './donnees/recapitulatif 21.xlsx'
FICHIER_OUT = f'./donnees/out-{today()}.xlsx'


def main():
    window = AppWindow()

    logs_path = f'./logs/{today()}.txt'
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
