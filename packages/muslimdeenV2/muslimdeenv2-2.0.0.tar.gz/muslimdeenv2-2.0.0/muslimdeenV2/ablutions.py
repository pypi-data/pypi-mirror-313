import pathlib as plib
import pandas as pd
from typing import Literal, TypedDict, List

class TypedAblution(TypedDict):
    step:str
    description:str
    nb_repetion:int
    references:str
    img:str


ListTypedAblutions = List[TypedAblution]

DATAFRAME:ListTypedAblutions = [
    {"step": "Intention (Niyya)", "description": "L'intention de faire les ablutions dans le cœur", "nb_repetition": 1, "references": "Sunna", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"},
    {"step": "Bismillah", "description": 'Prononcer "Bismillah"', "nb_repetition": 1, "references": "Sunna", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"},
    {"step": "Lavage des mains", "description": "Laver les deux mains jusqu'aux poignets", "nb_repetition": 3, "references": "Sunna", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"},
    {"step": "Rinçage de la bouche", "description": "Prendre de l'eau et la rincer", "nb_repetition": 3, "references": "Sunna", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"},
    {"step": "Rinçage du nez", "description": "Aspirer de l'eau dans les narines puis la rejeter", "nb_repetition": 3, "references": "Sunna", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"},
    {"step": "Lavage du visage", "description": "Laver le visage du front au menton", "nb_repetition": 3, "references": "Sourate Al-Mâ'ida (5:6)", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"},
    {"step": "Lavage des bras", "description": "Laver les bras jusqu'aux coudes", "nb_repetition": 3, "references": "Sourate Al-Mâ'ida (5:6), Sunna", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"},
    {"step": "Essuyer la tête", "description": "Passer les mains mouillées sur toute la tête", "nb_repetition": 3, "references": "Sourate Al-Mâ'ida (5:6), Sunna", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"},
    {"step": "Essuyer les oreilles", "description": "Essuyer l'intérieur et l'extérieur des oreilles", "nb_repetition": 3, "references": "Sunna", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"},
    {"step": "Lavage des pieds", "description": "Laver les pieds jusqu'aux chevilles", "nb_repetition": 3, "references": "Sourate Al-Mâ'ida (5:6)", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"},
    {"step": "Dua après ablutions", "description": "Réciter la supplication", "nb_repetition": 1, "references": "Sunna", "img_women": "https://lmdecoboutique.com/3026-thickbox_default/stickers-ablutions.jpg", "img_man": "https://lmdecoboutique.com/3025-thickbox_default/stickers-ablutions.jpg"}
]



class AblutionsParser:
    """
    Classe permettant de créer et sauvegarder un DataFrame des étapes d'ablution à partir d'une liste de dictionnaires.

    Attributes:
        path_database (str): Le chemin vers le dossier de base de données.
        path_csv (Path): Le chemin complet vers le fichier CSV où les données seront sauvegardées.
        __df (pd.DataFrame): Le DataFrame contenant les données des étapes d'ablution.
    """
    def __init__(self, path_database: str) -> None:
        """
        Initialise la classe AblutionsParser et crée le DataFrame.

        Args:
            path_database (str): Le chemin vers le dossier de base de données.
        """
        self.path_database = path_database
        self.path_csv = plib.Path(path_database).joinpath("ablutions.csv")
        self.__df = self.__create_df()

    def __create_df(self) -> pd.DataFrame:
        """
        Crée un DataFrame à partir de la liste de données, le sauvegarde en CSV et le retourne.

        Returns:
            pd.DataFrame: Le DataFrame des étapes d'ablution.
        """
        df = pd.DataFrame(DATAFRAME)
        df.to_csv(self.path_csv.as_posix(), index=False)
        return df

    @property
    def df(self) -> pd.DataFrame:
        """
        Retourne le DataFrame des étapes d'ablution.

        Returns:
            pd.DataFrame: Le DataFrame des étapes d'ablution.
        """
        return self.__df


class Ablutions:
    """
    Classe permettant de gérer les étapes d'ablution avec des images spécifiques pour homme ou femme.

    Attributes:
        path_database (str): Le chemin vers le dossier de base de données.
        gender (Literal["man", "women"]): Le genre pour lequel récupérer les images d'ablution.
        __df (pd.DataFrame): Le DataFrame contenant les données des étapes d'ablution après traitement.
    """
    def __init__(self, path_database: str, gender: Literal["man", "women"]) -> None:
        """
        Initialise la classe Ablutions, charge les données depuis un CSV ou les génère si le fichier n'existe pas.

        Args:
            path_database (str): Le chemin vers le dossier de base de données.
            gender (Literal["man", "women"]): Le genre pour lequel récupérer les images d'ablution.
        """
        self.path_database = path_database
        path = plib.Path(path_database).joinpath("ablutions.csv")
        self.gender: Literal['women', 'man'] = gender
        if not path.exists():
            self.__df = AblutionsParser(path_database).df
        else:
            self.__df = self.__read_df(path.as_posix())
        self.__parser_gender()

    @property
    def df(self) -> pd.DataFrame:
        """
        Retourne le DataFrame des étapes d'ablution après traitement par genre.

        Returns:
            pd.DataFrame: Le DataFrame filtré des étapes d'ablution.
        """
        return self.__df

    def __read_df(self, path_csv: str) -> pd.DataFrame:
        """
        Lit les données depuis un fichier CSV.

        Args:
            path_csv (str): Le chemin vers le fichier CSV contenant les étapes d'ablution.

        Returns:
            pd.DataFrame: Le DataFrame des étapes d'ablution.
        """
        df = pd.read_csv(path_csv)
        return df

    def __parser_gender(self) -> None:
        """
        Modifie le DataFrame en fonction du genre choisi, en gardant les images spécifiques pour homme ou femme.
        """
        df = self.__df.copy()

        if self.gender == "man":
            df.drop(columns="img_women", inplace=True)
            df.rename(columns={'img_man': "img"}, inplace=True)
        else:
            df.drop(columns="img_man", inplace=True)
            df.rename(columns={"img_women": "img"}, inplace=True)
        self.__df = df

    def data(self, respapi: bool = True) -> ListTypedAblutions:
        """
        Retourne les données des étapes d'ablution sous forme de liste de dictionnaires ou de DataFrame brut.

        Args:
            respapi (bool): Si True, retourne les données sous forme de liste de dictionnaires pour API.

        Returns:
            ListTypedAblutions: Les données des étapes d'ablution sous forme de liste de dictionnaires.
        """
        return self.df.to_dict(orient='records') if respapi else self.df
