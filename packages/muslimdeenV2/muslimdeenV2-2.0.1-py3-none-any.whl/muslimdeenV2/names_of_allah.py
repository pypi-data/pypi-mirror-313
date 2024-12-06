import bs4
import re
import pandas as pd
import pathlib as plib
from muslimdeenV2.services import Services
from muslimdeenV2.exception_handle import ByError
from typing import TypedDict, List, Union, Any, Tuple, Optional

class TypedNameOfAllah(TypedDict):
    number: Union[str, int]
    arabic_name_img: str
    name_phonetic: str
    name_french: str
    more_info_link: str
    description: str

ListNamesOfAllah = List[TypedNameOfAllah]

class ParserNamesOfAllah:
    def __init__(self, path_database: str) -> None:
        self.path_database = path_database
        self.__services = Services()
        self.__response_request = self._request_services()
        self.__parser = self.__parser_data()
        self.__df = self._transform_of_df()

    def _request_services(self) -> str:
        """
        Effectue une requête pour récupérer la page HTML contenant les 99 noms d'Allah.
        
        Returns:
            str: Le contenu HTML de la page.
        """
        return self.__services.names_of_allah()

    @property
    def df(self) -> pd.DataFrame:
        """
        Retourne le DataFrame contenant les 99 noms d'Allah.

        Returns:
            pd.DataFrame: Le DataFrame des noms d'Allah.
        """
        return self.__df

    def __extract_description(self, t_meaning: bs4.element.Tag) -> str:
        """
        Extrait la description d'une balise t_meaning.

        Args:
            t_meaning (bs4.element.Tag): La balise contenant la description.

        Returns:
            str: La description extraite.
        """
        description_parts = []
        for sibling in t_meaning.br.next_siblings:
            if isinstance(sibling, str):
                description_parts.append(sibling.strip())
            
        description = " ".join(description_parts)
        return description.strip()
        
    def get_arabic_name_image(self, img_tag: bs4.element.Tag) -> str:
        """
        Récupère l'image du nom en arabe à partir du tag <img>.
        Si 'data-lazy-src' existe, l'utilise. Sinon, vérifie l'attribut 'src'.

        Args:
            img_tag (bs4.element.Tag): Le tag <img> contenant les attributs 'data-lazy-src' ou 'src'.

        Returns:
            str: L'URL de l'image en arabe ou une chaîne vide si aucune image valide n'est trouvée.
        """
        if img_tag.has_attr('data-lazy-src'):
            return img_tag['data-lazy-src']
        elif img_tag.has_attr('src'):
            return img_tag['src']
        return ""

    def __parser_data(self) -> ListNamesOfAllah:
        """
        Parse les données des 99 noms d'Allah depuis le HTML.

        Returns:
            ListNamesOfAllah: Une liste de dictionnaires contenant les informations des noms d'Allah.
        """
        parser_soup = bs4.BeautifulSoup(self.__response_request, "html.parser")
        names_data: ListNamesOfAllah = []

        for tr in parser_soup.select('table tbody tr'):
            try:
                img_tag = tr.select_one('td.names-arabic img')
                arabic_name_img = self.get_arabic_name_image(img_tag)

                names_data.append({
                    "number": tr.select_one('td.names-numbering').get_text(strip=True),
                    "arabic_name_img": arabic_name_img,  
                    "name_phonetic": tr.select_one('td.transliteration').get_text(strip=True),
                    "name_french": re.sub(r'\((.*?)\)', r'\1', tr.select_one('td.t-meaning span.names-bolding').get_text(strip=True)).replace('(', '').replace(')', ''),
                    "more_info_link": tr.select_one('td.t-meaning a')['href'],
                    "description": self.__extract_description(tr.select_one('td.t-meaning'))
                })
            except (AttributeError, TypeError, KeyError) as e:
                print(f"Error parsing row: {e}")
        
        return names_data


    def _transform_of_df(self, save_in: bool = True) -> pd.DataFrame:
        """
        Transforme les données des noms d'Allah en DataFrame et les sauvegarde si nécessaire.
        La traduction de la phrase spécifique est appliquée avant la sauvegarde.

        Args:
            save_in (bool): Si True, sauvegarde les données dans un fichier CSV.

        Returns:
            pd.DataFrame: Le DataFrame des noms d'Allah.
        """
        df = pd.DataFrame(self.__parser)
        df.drop_duplicates(inplace=True)
        df = translate_specific_description(df)
        if save_in:
            path = plib.Path(self.path_database).joinpath("names_of_allah.csv")
            df.to_csv(index=False, path_or_buf=path.as_posix())
        return df

def translate_specific_description(df: pd.DataFrame) -> pd.DataFrame:
    """
    Traduit une phrase spécifique dans la colonne 'description' de la DataFrame des noms d'Allah.

    Args:
        df (pd.DataFrame): La DataFrame contenant les descriptions en anglais.

    Returns:
        pd.DataFrame: La DataFrame mise à jour avec la traduction en français.
    """

    phrase_english = "The Englarger, The One who constricts the sustenance by His wisdom and expands and widens it with His Generosity and Mercy."
    phrase_french = "L'Extenseur, Celui qui restreint la subsistance par Sa sagesse et l'élargit par Sa Générosité et Sa Miséricorde."
    name_english = "The Extender"
    name_french = "L'Extenseur"

    df['description'] = df['description'].replace(phrase_english, phrase_french)
    df['name_french'] = df['name_french'].replace(name_english, name_french)
    
    return df


class NamesOfAllah:
    def __init__(self, path_database: str) -> None:
        path = plib.Path(path_database).joinpath("names_of_allah.csv")
        if path.exists():
            df = pd.read_csv(path.as_posix())
        else:
            parser = ParserNamesOfAllah(path_database)
            df = parser.df
        self.__df = df

    @property
    def df(self) -> pd.DataFrame:
        return self.__df

    @property
    def columns_names(self) -> List[str]:
        return list(self.df.columns)

    def get_all(self, respapi: bool = True) -> Union[List[TypedNameOfAllah], pd.DataFrame]:
        """
        Récupère tous les enregistrements. Retourne un DataFrame si respapi=False,
        sinon un dictionnaire de type List[TypedNameOfAllah].

        Args:
            respapi (bool): Si True, retourne un dictionnaire JSON.

        Returns:
            Union[List[TypedNameOfAllah], pd.DataFrame]: Les données sous forme de dictionnaire ou de DataFrame.
        """
        return self.df if not respapi else self.df.to_dict(orient='records')


    def get_by(self, by: str, value: Union[Any, Tuple, List, None], respapi: bool = True) -> Optional[Union[List[TypedNameOfAllah], pd.DataFrame]]:
        """
        Récupère les enregistrements filtrés par une colonne spécifique et une valeur.
        Si value est None, retourne toutes les données de la colonne 'by'.
        Convertit les valeurs en chaînes de caractères pour éviter les erreurs de typage.

        Args:
            by (str): Le nom de la colonne sur laquelle filtrer.
            value (Union[Any, Tuple, List, None]): La valeur ou les valeurs à filtrer, ou None pour récupérer toutes les données de la colonne.
            respapi (bool): Si True, retourne un dictionnaire JSON.

        Returns:
            Optional[Union[List[TypedNameOfAllah], pd.DataFrame]]: Les données filtrées ou None si aucune donnée.
        """
        if by not in self.columns_names:
            raise ByError(f"Column name invalid {by}")
        if value is None:
            data = self.df[[by]]  
        elif isinstance(value, (tuple, list)):
            value = [str(v) for v in value] 
            data = self.df[self.df[by].astype(str).isin(value)]
        else:
            value = str(value)  
            data = self.df[self.df[by].astype(str) == value]
        if data.empty:
            return None
        return data.to_dict(orient='records') if respapi else data


