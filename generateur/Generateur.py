from generateur.input import Chargeur
from generateur.output import Exporteur
from util import AdvancedThread


class Generateur:
    def __init__(self) -> None:
        self.threads = []

    def generer(self, fichier_in: str, fichier_modele: str, fichier_out: str, annee: str, gen_fini):
        from ui import enable_bt, disable_bt

        chargeur = Chargeur(fichier_in, annee)
        exporteur = Exporteur(fichier_modele, fichier_out)

        t = AdvancedThread(
            on_quit=gen_fini,
            target=self.__thread_gen,
            args=(chargeur, exporteur)
        )

        t.start()

        self.threads.append(t)

    def __thread_gen(self, chargeur: Chargeur, exporteur: Exporteur):
        chargeur.recuperer()
        exporteur.charger()
        exporteur.exporter(chargeur.resultats)
        exporteur.sauvegarder()

    def ask_clean_threads(self):
        for t in self.threads:
            t.stop()

    def clean_threads(self):
        for t in self.threads:
            t.join()
