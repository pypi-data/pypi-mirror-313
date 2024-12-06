import json
import pathlib as plib
from typing import TypedDict, List, Optional, Literal, Dict, Union
from enum import Enum

from muslimdeenV2.services import Services


class QuranVersetData(TypedDict):
    """
    Représente les informations d'un verset du Coran.

    Attributes:
        position (int): Position globale du verset dans le Coran.
        text (str): Le texte du verset en translittération.
        position_ds_sourate (int): Position du verset dans la sourate.
        juz (int): Le numéro du Juz auquel appartient le verset.
        manzil (int): Le numéro du Manzil auquel appartient le verset.
        page (int): Le numéro de page où se trouve le verset.
        ruku (int): Le numéro du Ruku auquel appartient le verset.
        hizbQuarter (int): Le quart de Hizb auquel appartient le verset.
        sajda (bool): Indique si le verset contient une prosternation (Sajda).
        text_arabe (str): Le texte du verset en arabe.
    """
    position: int
    text: str
    position_ds_sourate: int
    juz: int
    manzil: int
    page: int
    ruku: int
    hizbQuarter: int
    sajda: bool
    text_arabe: str


class QuranSourateData(TypedDict):
    """
    Représente les informations d'une sourate du Coran.

    Attributes:
        position (int): La position de la sourate dans le Coran.
        nom (str): Le nom de la sourate en arabe.
        nom_phonetique (str): La translittération du nom de la sourate.
        englishNameTranslation (str): La traduction anglaise du nom de la sourate.
        revelation (str): Le type de révélation (Medinois ou Mecquoise).
        versets (List[QuranVersetData]): La liste des versets de la sourate.
        nom_sourate (str): Le nom de la sourate en français.
    """
    position: int
    nom: str
    nom_phonetique: str
    englishNameTranslation: str
    revelation: str
    versets: List[QuranVersetData]
    nom_sourate: str


class QuranData(TypedDict):
    """
    Représente les données du Coran avec toutes les sourates.

    Attributes:
        sourates (List[QuranSouratetData]): Liste des sourates avec leurs informations.
    """
    sourates: List[QuranSourateData]


class RevelationType(Enum):
    """
    Enumération des types de révélations des sourates.

    Values:
        MEDINOIS (str): Révélée à Médine.
        MECQUOISE (str): Révélée à La Mecque.
    """
    MEDINOIS = "Medinois"
    MECQUOISE = "Mecquoise"


class QuranServices:
    def __init__(self, path_database: str) -> None:
        self.path_database = path_database
        self.__services = Services()
        self.__response = self._request_quran_json()
        self.__save()

    def _request_quran_json(self) -> dict:
        return self.__services.quran_to_json()

    def __save(self) -> None:
        with open(plib.Path(self.path_database).joinpath("quran.json"), "w") as file:
            file.write(json.dumps(self.__response, indent=4))
        return None

    @property
    def resp(self) -> QuranData:
        return self.__response


class QuranReader:
    """
    Classe permettant de lire et d'interroger les données du Coran depuis un fichier JSON.

    Attributes:
        path_database (str): Le chemin vers le dossier contenant les données du Coran.
        path_quran (Path): Le chemin complet vers le fichier quran.json.
    """

    def __init__(self, path_database: str) -> None:
        """
        Initialise le lecteur du Coran avec le chemin vers la base de données.

        Args:
            path_database (str): Chemin vers le dossier de la base de données.
        """
        self.path_database = path_database
        self.path_quran = plib.Path(path_database).joinpath("quran.json")

        if not self.path_quran.exists():
            quran_services = QuranServices(path_database)
            self.__quran = quran_services.resp
        else:
            self.__quran = self.__read_init()

        self.__sourate_by_number: Optional[Dict[int, QuranSourateData]] = None
        self.__sourate_by_name_fr: Optional[Dict[str, QuranSourateData]] = None
        self.__sourate_by_name_arabic: Optional[Dict[str,
                                                     QuranSourateData]] = None

    @staticmethod
    def revelation_type_enum() -> RevelationType:
        """
        Retourne l'énumération des types de révélation (Medinois ou Mecquoise).

        Returns:
            RevelationType: L'énumération des types de révélation.
        """
        return RevelationType

    def __read_init(self) -> QuranData:
        """
        Lit le fichier quran.json et initialise les données du Coran.

        Returns:
            QuranData: Les données du Coran sous forme de dictionnaire.

        Raises:
            Exception: En cas d'erreur lors de la lecture du fichier quran.json.
        """
        try:
            with open(self.path_quran, "r") as file:
                buffer = file.read()
                parser_json = json.loads(buffer)
                return parser_json
        except Exception as e:
            raise Exception(f'Error reading file quran.json {str(e)}')

    @property
    def quran(self) -> QuranData:
        """
        Retourne les données complètes du Coran.

        Returns:
            QuranData: Les données du Coran.
        """
        return self.__quran

    @property
    def sourate_by_number(self) -> Dict[int, QuranSourateData]:
        """
        Retourne un dictionnaire des sourates indexées par leur numéro de position.

        Returns:
            Dict[int, QuranSouratetData]: Les sourates indexées par position.
        """
        if self.__sourate_by_number is None:
            self.__sourate_by_number = {
                s['position']: s for s in self.quran['sourates']}
        return self.__sourate_by_number

    @property
    def sourate_by_name_fr(self) -> Dict[str, QuranSourateData]:
        """
        Retourne un dictionnaire des sourates indexées par leur nom en français.

        Returns:
            Dict[str, QuranSouratetData]: Les sourates indexées par nom en français.
        """
        if self.__sourate_by_name_fr is None:
            self.__sourate_by_name_fr = {
                s['nom_sourate']: s for s in self.quran['sourates']}
        return self.__sourate_by_name_fr

    @property
    def sourate_by_name_arabic(self) -> Dict[str, QuranSourateData]:
        """
        Retourne un dictionnaire des sourates indexées par leur nom en arabe.

        Returns:
            Dict[str, QuranSouratetData]: Les sourates indexées par nom en arabe.
        """
        if self.__sourate_by_name_arabic is None:
            self.__sourate_by_name_arabic = {
                s['nom']: s for s in self.quran['sourates']}
        return self.__sourate_by_name_arabic

    def search_by_number(self, number: int) -> Optional[QuranSourateData]:
        """
        Recherche une sourate par son numéro de position.

        Args:
            number (int): Le numéro de la sourate.

        Returns:
            Optional[QuranSouratetData]: Les informations de la sourate, ou None si non trouvée.
        """
        return self.sourate_by_number.get(number, None)

    def search_by_name_fr(self, namefr: str) -> Optional[QuranSourateData]:
        """
        Recherche une sourate par son nom en français.

        Args:
            namefr (str): Le nom de la sourate en français.

        Returns:
            Optional[QuranSouratetData]: Les informations de la sourate, ou None si non trouvée.
        """
        return self.sourate_by_name_fr.get(namefr, None)

    def search_by_name_arabic(self, namearabic: str) -> Optional[QuranSourateData]:
        """
        Recherche une sourate par son nom en arabe.

        Args:
            namearabic (str): Le nom de la sourate en arabe.

        Returns:
            Optional[QuranSouratetData]: Les informations de la sourate, ou None si non trouvée.
        """
        return self.sourate_by_name_arabic.get(namearabic, None)

    def get_all_by_type_revelation(self, type_of_revelation: Union[RevelationType, Literal["Medinois", "Mecquoise"]]) -> List[QuranSourateData]:
        """
        Retourne toutes les sourates correspondant au type de révélation spécifié.

        Args:
            type_of_revelation (Union[RevelationType, Literal["Medinois", "Mecquoise"]]): Le type de révélation (Medinois ou Mecquoise).

        Returns:
            List[QuranSouratetData]: Liste des sourates correspondant au type de révélation.
        """
        if isinstance(type_of_revelation, RevelationType):
            return [sourate for sourate in self.quran['sourates'] if sourate['revelation'] == type_of_revelation.value]
        else:
            return [sourate for sourate in self.quran['sourates'] if sourate['revelation'] == type_of_revelation]
