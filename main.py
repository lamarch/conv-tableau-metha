import sys
import os.path
from os import mkdir
from tkinter.constants import DISABLED, NORMAL
from util import AdvancedThread
from input import Chargeur
from output import Exporteur
from json import dumps
from datetime import datetime
import tkinter as tk
import tkinter.messagebox as messagebox
from ui import OpenFileEntry, SaveFileEntry


def AJD(): return str(datetime.now()).replace(':', '-').replace('/', '-')


FICHIER_IN = './donnees/Pesées terminées.csv'
FICHIER_MOD = './donnees/recapitulatif 21.xlsx'
FICHIER_OUT = f'./donnees/out-{AJD()}.xlsx'

threads = []


def pre_clean_threads():
    global threads
    for t in threads:
        t.stop(t)


def clean_threads():
    global threads
    for t in threads:
        t.join(t)


def panic(self, *args):
    import traceback
    import sys

    pre_clean_threads()

    msg = ''
    msg += 'FROM:'
    msg += str(self)
    msg += '\n\n\n'
    msg += 'MESSAGE:'
    msg += '\n'.join(map(lambda a: str(a), args))

    messagebox.showerror(
        'Erreur critique !', f'Une erreur critique est survenue, demandez de l\'aide à l\'assistance ! Ne pas supprimer le fichier "erreur.txt".\n\n\n')
    with open('erreur.txt', 'w', encoding='UTF8') as f:
        f.write(msg)

    clean_threads()

    sys.exit(0)


def gen(entree_in: str, entree_mod: str, entree_out: str, bt_gen: tk.Button):
    from ui import enable_bt, disable_bt

    def gen_fini(bt_gen: tk.Button):
        enable_bt(bt_gen)
        messagebox.showinfo("Génération terminée !",
                            "La génération du fichier s'est terminée avec succès !")
    global threads

    disable_bt(bt_gen)

    chargeur = Chargeur(entree_in)
    exporteur = Exporteur(entree_mod, entree_out)

    t = AdvancedThread(
        on_quit=lambda: gen_fini(bt_gen),
        target=thread_gen,
        args=(chargeur, exporteur)
    )

    t.start()

    threads.append(t)


def thread_gen(chargeur: Chargeur, exporteur: Exporteur):
    chargeur.recuperer()
    exporteur.charger()
    exporteur.convertir(chargeur.resultats)
    exporteur.sauvegarder()


def ui():
    #tk.Tk.report_callback_exception = panic

    fenetre = tk.Tk()
    fenetre.title("Convertisseur")
    fenetre.geometry("400x160")

    fenetre.rowconfigure(0, weight=1)
    fenetre.rowconfigure(1, weight=1)
    fenetre.rowconfigure(2, weight=1)
    fenetre.rowconfigure(3, weight=1)

    fenetre.columnconfigure(0, weight=1)

    # entree fichier in
    entree_in = OpenFileEntry(
        fenetre, "Fichier données :", exts=(('Fichier CSV', '*.csv'),), defaultext='.csv')
    entree_in.grid(row=0, column=0, sticky="EW")

    # entree fichier mod
    entree_mod = OpenFileEntry(
        fenetre, "Fichier modèle :", exts=(('Fichier Excel', '*.xlsx'),), defaultext='.xlsx')
    entree_mod.grid(row=1, column=0, sticky="EW")

    # entree fichier out
    entree_out = SaveFileEntry(
        fenetre, "Fichier de sortie :", exts=(('Fichier Excel', '*.xlsx'),), defaultext='.xlsx')
    entree_out.grid(row=2, column=0, sticky="EW")

    # bouton action
    bt_go = tk.Button(fenetre, text="Générer", command=lambda: gen(
        entree_in.filename, entree_mod.filename, entree_out.filename, bt_go))
    bt_go.grid(row=3, column=0)

    fenetre.mainloop()


def main():
    global threads

    logs_path = f'./logs/{AJD()}.txt'
    logs_dir = os.path.dirname(logs_path)
    if not os.path.isdir(logs_dir):
        mkdir(logs_dir)

    print(os.path.abspath(logs_path))
    with open(logs_path, 'x', encoding='UTF8') as out:
        sys.stdout = sys.stderr = out
        ui()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        panic(str(e))
