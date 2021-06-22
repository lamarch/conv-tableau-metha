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

FICHIER_NON_SELECTIONNE = "Aucun fichier séléctionné."

threads = []


def pre_clean_threads():
    global threads
    for t in threads:
        t.stop()


def clean_threads():
    global threads
    for t in threads:
        t.join(t)


def panic(*args):
    import sys

    pre_clean_threads()

    msg = '\n'.join(map(lambda a: str(a), args))

    messagebox.showerror(
        'Erreur critique !', f'Une erreur critique est survenue, demandez de l\'aide à l\'assistance ! Ne pas supprimer le fichier "erreur.txt".\n\n\n')
    with open('erreur.txt', 'w', encoding='UTF8') as f:
        f.write(msg)

    clean_threads()

    sys.exit(0)


def gen(fichier_in: str, fichier_modele: str, fichier_out: str, annee: str, bt_gen: tk.Button):
    from ui import enable_bt, disable_bt

    def gen_fini(bt_gen: tk.Button):
        enable_bt(bt_gen)
        messagebox.showinfo("Génération terminée !",
                            "La génération du fichier s'est terminée avec succès !")
    global threads

    # entree
    if fichier_in == None or fichier_in == "" or fichier_in == FICHIER_NON_SELECTIONNE:
        messagebox.showerror(
            "Erreur !", "Valeur de fichier d'entrée invalide !")
        return

    if not os.path.isfile(fichier_in):
        messagebox.showerror("Erreur !", "Fichier d'entrée inexistant !")
        return

    # modele
    if fichier_modele == None or fichier_modele == "" or fichier_modele == FICHIER_NON_SELECTIONNE:
        messagebox.showerror(
            "Erreur !", "Valeur de fichier modèle invalide !")
        return

    if not os.path.isfile(fichier_modele):
        messagebox.showerror("Erreur !", "Fichier modèle inexistant !")
        return

    # sortie
    if fichier_out == None or fichier_out == "" or fichier_out == FICHIER_NON_SELECTIONNE:
        messagebox.showerror(
            "Erreur !", "Valeur de fichier de sortie invalide !")
        return

    # annee
    try:
        annee = int(annee)
        assert annee >= 0 and annee <= 3000
    except:
        messagebox.showerror("Erreur !", "Format de l'année invalide !")
        return

    disable_bt(bt_gen)

    chargeur = Chargeur(fichier_in, annee)
    exporteur = Exporteur(fichier_modele, fichier_out)

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
    exporteur.exporter(chargeur.resultats)
    exporteur.sauvegarder()


def ui():
    #tk.Tk.report_callback_exception = panic

    fenetre = tk.Tk()
    fenetre.title("Convertisseur")
    fenetre.geometry("490x160")

    #fenetre.rowconfigure(0, weight=0)
    #fenetre.rowconfigure(1, weight=0)
    #fenetre.rowconfigure(2, weight=0)
    #fenetre.rowconfigure(3, weight=1)

    fenetre.columnconfigure(1, weight=1)

    # entree fichier in
    entree_in = OpenFileEntry(
        fenetre, "Fichier données :", exts=(('Fichier CSV', '*.csv'),), defaultext='.csv', defval=FICHIER_NON_SELECTIONNE)
    entree_in.grid(row=0, column=0, columnspan=2, sticky="EW")

    # entree fichier mod
    entree_mod = OpenFileEntry(
        fenetre, "Fichier modèle :", exts=(('Fichier Excel', '*.xlsx'),), defaultext='.xlsx', defval=FICHIER_NON_SELECTIONNE)
    entree_mod.grid(row=1, column=0, columnspan=2, sticky="EW")

    # entree fichier out
    entree_out = SaveFileEntry(
        fenetre, "Fichier de sortie :", exts=(('Fichier Excel', '*.xlsx'),), defaultext='.xlsx', defval=FICHIER_NON_SELECTIONNE)
    entree_out.grid(row=2, column=0, columnspan=2, sticky="EW")

    # entree année
    lbl_annee = tk.Label(fenetre, text="Année séléctionnée :")
    lbl_annee.grid(row=3, column=0)
    entree_annee = tk.Entry(fenetre)
    entree_annee.grid(row=3, column=1)

    # bouton action
    bt_go = tk.Button(fenetre, text="Générer", command=lambda: gen(
        entree_in.filename, entree_mod.filename, entree_out.filename, entree_annee.get(), bt_go))
    bt_go.grid(row=4, column=0, columnspan=2)

    fenetre.mainloop()


def main():
    global threads

    logs_path = f'./logs/{AJD()}.txt'
    logs_dir = os.path.dirname(logs_path)
    if not os.path.isdir(logs_dir):
        mkdir(logs_dir)

    print(os.path.abspath(logs_path))
    with open(logs_path, 'x', encoding='UTF8', buffering=1) as out:
        sys.stdout = sys.stderr = out
        ui()

    pre_clean_threads()

    clean_threads()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        panic(str(e))
