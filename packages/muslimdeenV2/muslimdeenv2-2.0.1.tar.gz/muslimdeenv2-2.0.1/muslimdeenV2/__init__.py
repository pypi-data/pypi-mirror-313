from muslimdeenV2.config import Config
from muslimdeenV2.services import Services
from muslimdeenV2.metasurahs import MetaSurahs
from muslimdeenV2.quran_reader import QuranReader, RevelationType, QuranVersetData, QuranSourateData, QuranData
from muslimdeenV2.exception_handle import ByError
from muslimdeenV2.names_of_allah import NamesOfAllah
from muslimdeenV2.ablutions import Ablutions
from muslimdeenV2.salat import Salat
from muslimdeenV2.pillars_of_islam import PillarsOfIslam
from muslimdeenV2.zakat import Zakat
from typing import Union, Literal
from pathlib import Path

class MuslimDeen:
    """
    Classe principale pour gérer les différentes fonctionnalités du projet MuslimDeen.
    
    Attributes:
        path_database (str): Le chemin vers le répertoire de la base de données.

    Methods:
        config_url(): Renvoie l'instance de configuration contenant les URLs.
        meta_surahs(): Charge et renvoie les métadonnées des sourates du Coran.
        names_of_allah(): Charge et renvoie les 99 noms d'Allah.
        quran_reader(): Charge et renvoie le lecteur du Coran avec toutes les sourates.
        ablutions(gender): Charge et renvoie les étapes des ablutions selon le genre.
        salat(): Charge et renvoie les étapes des prières.
        pillards_of_islam(): Charge et renvoie les informations sur les 5 piliers de l'Islam.
        zakat(): Renvoie des liens vers des calculateurs de Zakat.
        setup_all(): Initialise tous les services et construit la base de données.
    """

    def __init__(self, path_database: Union[str, Path, None] = None) -> None:
        """
        Initialise la classe MuslimDeen avec un chemin vers la base de données.
        
        Args:
            path_database (Union[str, Path, None]): Chemin vers le dossier de base de données. 
            Si aucun chemin n'est fourni, le répertoire courant sera utilisé.
        """
        if isinstance(path_database, str):
            path = Path(path_database).joinpath('database')
        elif isinstance(path_database, Path):
            path = path_database.joinpath('database')
        elif path_database is None:
            path = Path().cwd().joinpath('database')

        # Créer le dossier si nécessaire
        path.mkdir(parents=True, exist_ok=True)
        self.path_database = path.as_posix()
        self.setup_all()

    def config_url(self) -> Config:
        """
        Renvoie l'instance de configuration contenant les URLs.

        Returns:
            Config: Instance de la classe Config avec les URLs du projet.
        """
        return Config()

    def meta_surahs(self) -> MetaSurahs:
        """
        Charge et renvoie les métadonnées des sourates.

        Returns:
            MetaSurahs: Instance contenant les métadonnées des sourates.
        """
        return MetaSurahs(self.path_database)

    def names_of_allah(self) -> NamesOfAllah:
        """
        Charge et renvoie les 99 noms d'Allah.

        Returns:
            NamesOfAllah: Instance contenant les 99 noms d'Allah.
        """
        return NamesOfAllah(self.path_database)

    def quran_reader(self) -> QuranReader:
        """
        Charge et renvoie un lecteur du Coran contenant toutes les sourates et leurs métadonnées.

        Returns:
            QuranReader: Instance du lecteur de données du Coran.
        """
        return QuranReader(self.path_database)

    def ablutions(self, gender: Literal['man', 'women']) -> Ablutions:
        """
        Charge et renvoie les étapes des ablutions selon le genre.

        Args:
            gender (Literal['man', 'women']): Genre pour lequel afficher les étapes des ablutions (homme ou femme).

        Returns:
            Ablutions: Instance contenant les étapes des ablutions selon le genre.
        """
        return Ablutions(self.path_database, gender)

    def salat(self) -> Salat:
        """
        Charge et renvoie les étapes des prières (Salat).

        Returns:
            Salat: Instance contenant les étapes des prières.
        """
        return Salat(self.path_database)

    def pillars_of_islam(self) -> PillarsOfIslam:
        """
        Charge et renvoie les informations sur les 5 piliers de l'Islam.

        Returns:
            PillarsOfIslam: Instance contenant les informations détaillées sur les 5 piliers de l'Islam.
        """
        return PillarsOfIslam(self.path_database)

    def zakat(self) -> Zakat:
        """
        Renvoie des liens vers des calculateurs de Zakat.

        Returns:
            Zakat: Instance contenant des liens vers des calculateurs de Zakat.
        """
        return Zakat()

    def setup_all(self) -> None:
        """
        Construit la base de données en initialisant les services et en créant les fichiers nécessaires pour les métadonnées, 
        les noms d'Allah, les sourates du Coran, les étapes des ablutions, des prières et les piliers de l'Islam.
        """
        self.meta_surahs()
        self.names_of_allah()
        self.quran_reader()
        self.ablutions("man")
        self.salat()
        self.pillars_of_islam()
        self.zakat()
