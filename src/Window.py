import tkinter as tk
import tkinter.messagebox as messagebox
from os.path import isfile

from generateur.Generateur import Generateur
from generateur.common import GenOptions
from ui import OpenFileEntry, SaveFileEntry, disable_bt, enable_bt
from utils import panic

FICHIER_NON_SELECTIONNE = "Aucun fichier séléctionné."


class AppWindow(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.generateur = Generateur()
        self.__build_ui()

    def __check_entry(self, gen_options: GenOptions) -> bool:
        fichier_in, fichier_modele, fichier_out, annee = gen_options

        # entree
        if fichier_in == None or fichier_in == "" or fichier_in == FICHIER_NON_SELECTIONNE:
            messagebox.showerror(
                "Erreur !", "Valeur de fichier d'entrée invalide !")
            return False

        if not isfile(fichier_in):
            messagebox.showerror("Erreur !", "Fichier d'entrée inexistant !")
            return False

        # modele
        if fichier_modele == None or fichier_modele == "" or fichier_modele == FICHIER_NON_SELECTIONNE:
            messagebox.showerror(
                "Erreur !", "Valeur de fichier modèle invalide !")
            return False

        if not isfile(fichier_modele):
            messagebox.showerror("Erreur !", "Fichier modèle inexistant !")
            return False

        # sortie
        if fichier_out == None or fichier_out == "" or fichier_out == FICHIER_NON_SELECTIONNE:
            messagebox.showerror(
                "Erreur !", "Valeur de fichier de sortie invalide !")
            return False

        # annee
        try:
            annee = int(annee)
            assert annee >= 0 and annee <= 3000
        except:
            messagebox.showerror("Erreur !", "Format de l'année invalide !")
            return False

        return True

    def __generer(self):
        def gen_fini():
            enable_bt(self.bt_go)
            messagebox.showinfo("Génération terminée !",
                                "La génération du fichier s'est terminée avec succès !")

        gen_options = GenOptions(
            self.entree_in.filename,
            self.entree_mod.filename,
            self.entree_out.filename,
            self.entree_annee.get())

        if self.__check_entry(gen_options):

            gen_options = gen_options._replace(annee=int(gen_options.annee))
            disable_bt(self.bt_go)

            self.generateur.generer(gen_options, gen_fini)

    def __build_ui(self):
        self.title("Convertisseur")
        self.geometry("490x160")

        self.columnconfigure(1, weight=1)

        # entree fichier in
        self.entree_in = OpenFileEntry(
            self, "Fichier données :", exts=(('Fichier CSV', '*.csv'),), defaultext='.csv', defval=FICHIER_NON_SELECTIONNE)
        self.entree_in.grid(row=0, column=0, columnspan=2, sticky="EW")

        # entree fichier mod
        self.entree_mod = OpenFileEntry(
            self, "Fichier modèle :", exts=(('Fichier Excel', '*.xlsx'),), defaultext='.xlsx', defval=FICHIER_NON_SELECTIONNE)
        self.entree_mod.grid(row=1, column=0, columnspan=2, sticky="EW")

        # entree fichier out
        self.entree_out = SaveFileEntry(
            self, "Fichier de sortie :", exts=(('Fichier Excel', '*.xlsx'),), defaultext='.xlsx', defval=FICHIER_NON_SELECTIONNE)
        self.entree_out.grid(row=2, column=0, columnspan=2, sticky="EW")

        # entree année
        lbl_annee = tk.Label(self, text="Année sélectionnée :")
        lbl_annee.grid(row=3, column=0)
        self.entree_annee = tk.Entry(self)
        self.entree_annee.grid(row=3, column=1)

        # bouton action
        self.bt_go = tk.Button(self, text="Générer",
                               command=self.__generer)
        self.bt_go.grid(row=4, column=0, columnspan=2)

    def ask_stop(self):
        self.generateur.ask_clean_threads()

    def stop(self):
        self.generateur.clean_threads()

    def report_callback_exception(self, exc, val, tb):
        panic(str(val))
