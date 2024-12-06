import pandas as pd
import pathlib as plib
from muslimdeenV2.services import Services
from muslimdeenV2.quran_reader import QuranReader
from muslimdeenV2.exception_handle import ByError
from typing import List, Any, Optional, Union, TypedDict, Tuple

class TypedMetaSurah(TypedDict):
    position: int
    name_arabic: str
    name_phonetic: str
    name_english: str
    name_french: str
    revelation_type: str
    number_of_ayahs: int
    sajdas_recommended: bool
    sajdas_obligatory: bool

ListMetaSurahs = List[TypedMetaSurah]

class ParserMetaSurahs:
    def __init__(self, path_database: str) -> None:
        """
        Initialise la classe ParserMetaSurahs qui gère le parsing des métadonnées des sourates.
        
        Args:
            path_database (str): Le chemin vers la base de données.
        """
        self.path_database = path_database
        self.__services = Services()
        self.__response_api = self._request_response_api()
        self.__quran_reader = QuranReader(path_database)

    def _request_response_api(self) -> dict:
        """
        Récupère les données de l'API des métadonnées des sourates.

        Returns:
            dict: La réponse de l'API sous forme de dictionnaire.
        """
        return self.__services.metadata_off_surahs()

    def parser_response_api(self) -> pd.DataFrame:
        """
        Parse les métadonnées des sourates provenant de l'API.

        Returns:
            pd.DataFrame: Un DataFrame contenant les métadonnées des sourates et les informations sur les sajdas.
        """
        responseapi = self.__response_api
        data_response = responseapi['data']
        surahs = data_response["surahs"]["references"]
        sajdas = data_response["sajdas"]["references"]
        df_surahs = pd.DataFrame(surahs)
        df_sajdas = pd.DataFrame(sajdas)
        df_merged = pd.merge(df_surahs, df_sajdas, how="left", left_on=['number'], right_on=["surah"])
        df_merged.drop(columns=['surah', 'ayah'], inplace=True)
        df_merged['sajdas_recommended'] = df_merged['recommended'].apply(lambda x: False if pd.isna(x) else x).astype(bool)
        df_merged['sajdas_obligatory'] = df_merged['obligatory'].apply(lambda x: False if pd.isna(x) else x).astype(bool)
        df_merged.drop(columns=['recommended', 'obligatory'], inplace=True)
        df_merged.drop_duplicates(inplace=True)
        return df_merged

    def parser_quran_reader(self) -> pd.DataFrame:
        """
        Parse les données des sourates du Coran (sans versets).

        Returns:
            pd.DataFrame: Un DataFrame contenant les informations des sourates (nom, traduction, type de révélation, etc.).
        """
        quran = self.__quran_reader.quran
        sourates_data = [
            {
                "position": sourate['position'],
                "name_arabic": sourate['nom'],
                "name_phonetic": sourate['nom_phonetique'],
                "name_english": sourate['englishNameTranslation'],
                "name_french": sourate['nom_sourate'],
                "revelation_type": sourate['revelation']
            }
            for sourate in quran['sourates']
        ]
        df = pd.DataFrame(sourates_data)
        df.drop_duplicates(inplace=True)
        return df

    def parser_meta_surahs(self, save_in: bool = True) -> pd.DataFrame:
        """
        Fusionne les données des sourates provenant de l'API et du fichier du Coran pour créer un DataFrame complet.

        Args:
            save_in (bool): Si True, sauvegarde le DataFrame résultant dans un fichier CSV.

        Returns:
            pd.DataFrame: Un DataFrame contenant toutes les métadonnées des sourates fusionnées.
        """
        parser_quran_reader = self.parser_quran_reader()
        parser_response_api = self.parser_response_api()

        merged_df = pd.merge(parser_response_api, parser_quran_reader, left_on='number', right_on='position', how='left')

        merged_df = merged_df[[
            "number", "name_arabic", "name_phonetic", "name_english", "name_french",
            "revelation_type", "numberOfAyahs", "sajdas_recommended", "sajdas_obligatory"
        ]]
        merged_df.rename(columns={
            "number": "position",
            "name_arabic": "name_arabic",
            "name_phonetic": "name_phonetic",
            "name_english": "name_english",
            "name_french": "name_french",
            "revelation_type": "revelation_type",
            "numberOfAyahs": "number_of_ayahs"
        }, inplace=True)

        merged_df.drop_duplicates(inplace=True)
        if save_in:
            path = plib.Path(self.path_database).joinpath('metasurahs.csv')
            merged_df.to_csv(index=False, path_or_buf=path.as_posix())
        return merged_df


class MetaSurahs:
    def __init__(self, path_database: str) -> None:
        """
        Initialise la classe MetaSurahs en chargeant les données des sourates depuis un fichier CSV
        ou en les générant via le ParserMetaSurahs si le fichier n'existe pas.

        Args:
            path_database (str): Le chemin vers la base de données.
        """
        path = plib.Path(path_database).joinpath("metasurahs.csv")
        if path.exists():
            df = pd.read_csv(path.as_posix())
        else:
            parser = ParserMetaSurahs(path_database)
            df = parser.parser_meta_surahs()
        self.__df = df

    @property
    def df(self) -> pd.DataFrame:
        """
        Retourne le DataFrame contenant les métadonnées des sourates.
        
        Returns:
            pd.DataFrame: Le DataFrame des sourates.
        """
        return self.__df
    
    @property
    def columns_names(self) -> List[str]:
        """
        Retourne la liste des noms de colonnes dans le DataFrame.

        Returns:
            List[str]: La liste des noms de colonnes.
        """
        return list(self.df.columns)

    def get_by(self, by: str, value: Union[Any, Tuple, List, None], respapi: bool = True) -> Optional[Union[ListMetaSurahs, pd.DataFrame]]:
        """
        Récupère les enregistrements filtrés par une colonne spécifique et une valeur.
        Si value est None, retourne toutes les données de la colonne 'by'.
        Convertit les valeurs en chaînes de caractères pour éviter les erreurs de typage.

        Args:
            by (str): Le nom de la colonne sur laquelle filtrer.
            value (Union[Any, Tuple, List, None]): La valeur ou les valeurs à filtrer, ou None pour récupérer toutes les données de la colonne.
            respapi (bool): Si True, retourne un dictionnaire JSON.

        Returns:
            Optional[Union[ListMetaSurahs, pd.DataFrame]]: Les données filtrées ou None si aucune donnée.
        """
        if by not in self.columns_names:
            raise ByError(f"Column name invalid {by}")
        if value is None:
            data = self.df[[by]]  
        elif isinstance(value, (tuple, list)):
            value = [str(v) for v in value]  # Convertir toutes les valeurs en chaînes de caractères
            data = self.df[self.df[by].astype(str).isin(value)]
        else:
            value = str(value)  # Convertir la valeur en chaîne de caractères
            data = self.df[self.df[by].astype(str) == value]
        if data.empty:
            return None
        return data.to_dict(orient="records") if respapi else data

    def get_all(self, respapi: bool = True) -> Union[ListMetaSurahs, pd.DataFrame]:
        """
        Retourne toutes les données.

        Args:
            respapi (bool): Si True, retourne les données formatées pour une API (sous forme de liste de dictionnaires).
                            Si False, retourne les données sous forme brute (DataFrame).

        Returns:
            Union[List[dict], pd.DataFrame]: Toutes les données sous forme de dictionnaire (API) ou DataFrame (brut).
        """
        return self.df.to_dict(orient='records') if respapi else self.df
