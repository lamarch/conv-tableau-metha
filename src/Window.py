import tkinter as tk
import tkinter.messagebox as messagebox
from os.path import isfile
from datetime import datetime


from generateur.Generateur import Generateur
from generateur.common import GenOptions
from ui import OpenFileEntry, SaveFileEntry, disable_bt, enable_bt
from utils import panic, is_devenv

FICHIER_NON_SELECTIONNE = "Aucun fichier séléctionné."
FORMAT_DATE = "%d/%m/%y"

DEFAUT_FICHIER_IN = ""
DEFAUT_FICHIER_MOD = "C:\\Users\\Xavier\\Sync\\trav\\290521\\donnees\\modele 5.xlsx"
DEFAUT_FICHIER_OUT = "C:\\Users\\Xavier\\Sync\\trav\\290521\\donnees\\out 9.xlsx"
DEFAUT_TEMPS_DEBUT = "1/1/21"
DEFAUT_TEMPS_FIN = "1/1/22"


class AppWindow(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.generateur = Generateur()
        self.__build_ui()

    def __check_entry(self, gen_options: GenOptions) -> bool:
        fichier_in, fichier_modele, fichier_out, filtre_temps_debut, filtre_temps_fin = gen_options

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

        # filtre temps debut
        if filtre_temps_debut:
            try:
                filtre_temps_debut = datetime.strptime(
                    filtre_temps_debut, FORMAT_DATE)
            except ValueError:
                messagebox.showerror(
                    "Erreur !", "Format du filtre de temps de début invalide !\n Le format doit être : 'dd/mm/yy' .")
                return False
        else:
            filtre_temps_debut = datetime.min

        # filtre temps fin
        if filtre_temps_fin:
            try:
                filtre_temps_fin = datetime.strptime(
                    filtre_temps_fin, FORMAT_DATE)
            except ValueError:
                messagebox.showerror(
                    "Erreur !", "Format du filtre de temps de fin invalide !\n Le format doit être : 'dd/mm/yy' .")
                return False
        else:
            filtre_temps_fin = datetime.max

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
            self.entree_ftemps_debut.get(),
            self.entree_ftemps_fin.get())

        if self.__check_entry(gen_options):

            gen_options = gen_options._replace(
                filtre_temps_debut=datetime.strptime(
                    gen_options.filtre_temps_debut, FORMAT_DATE),
                filtre_temps_fin=datetime.strptime(gen_options.filtre_temps_fin, FORMAT_DATE))

            disable_bt(self.bt_go)

            self.generateur.generer(gen_options, gen_fini)

    def __build_ui(self):
        self.title("Convertisseur")
        self.geometry("490x160")

        self.columnconfigure(0, weight=1)

        # entree fichier in
        self.entree_in = OpenFileEntry(
            self, "Fichier données :", exts=(('Fichier CSV', '*.csv'),), defaultext='.csv', defval=FICHIER_NON_SELECTIONNE)
        self.entree_in.grid(row=0, column=0, sticky="EW")

        # entree fichier mod
        self.entree_mod = OpenFileEntry(
            self, "Fichier modèle :", exts=(('Fichier Excel', '*.xlsx'),), defaultext='.xlsx', defval=FICHIER_NON_SELECTIONNE)
        self.entree_mod.grid(row=1, column=0, sticky="EW")

        # entree fichier out
        self.entree_out = SaveFileEntry(
            self, "Fichier de sortie :", exts=(('Fichier Excel', '*.xlsx'),), defaultext='.xlsx', defval=FICHIER_NON_SELECTIONNE)
        self.entree_out.grid(row=2, column=0, sticky="EW")

        # conteneur filtre temporel
        frame_filtre_temp = tk.Frame(self)
        frame_filtre_temp.grid(row=3, column=0, sticky='W')
        frame_filtre_temp.columnconfigure(1, weight=1)
        frame_filtre_temp.columnconfigure(2, weight=1)

        # filtre temporel
        lbl_ftemp_de = tk.Label(
            frame_filtre_temp, text="Filtre temporel, de (inclus) :")
        lbl_ftemp_de.grid(row=0, column=0, sticky='W')

        # debut
        self.entree_ftemps_debut = tk.Entry(frame_filtre_temp)
        self.entree_ftemps_debut.grid(row=0, column=1)

        lbl_ftemp_a = tk.Label(frame_filtre_temp, text=" à (exclus) :")
        lbl_ftemp_a.grid(row=0, column=2)

        # fin
        self.entree_ftemps_fin = tk.Entry(frame_filtre_temp)
        self.entree_ftemps_fin.grid(row=0, column=3)

        # bouton action
        self.bt_go = tk.Button(self, text="Générer",
                               command=self.__generer)
        self.bt_go.grid(row=4, column=0, columnspan=2)

        if is_devenv():
            self.entree_in.var.set(DEFAUT_FICHIER_IN)
            self.entree_mod.var.set(DEFAUT_FICHIER_MOD)
            self.entree_out.var.set(DEFAUT_FICHIER_OUT)
            self.entree_ftemps_debut.insert(0, DEFAUT_TEMPS_DEBUT)
            self.entree_ftemps_fin.insert(0, DEFAUT_TEMPS_FIN)

    def ask_stop(self):
        self.generateur.ask_clean_threads()

    def stop(self):
        self.generateur.clean_threads()

    def report_callback_exception(self, exc, val, tb):
        import traceback
        l = traceback.format_tb(tb)
        panic(str(val))
