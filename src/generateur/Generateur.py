from generateur.common import GenOptions
from generateur.input import Chargeur
from generateur.output import Exporteur
from utils import AdvancedThread


class Generateur:
    def __init__(self) -> None:
        self.threads = []

    def generer(self, gen_options: GenOptions, gen_fini):
        chargeur = Chargeur(gen_options)
        exporteur = Exporteur(gen_options)

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
