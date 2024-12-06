from muslimdeenV2.data_salat import Prayer,TypedSalat

import pandas as pd
import pathlib as plib
from typing import TypedDict, List

class TypedInfosSalat(TypedDict):
    number:int
    name:str
    nb_rakat:int
    description_salat:str
    link_video:str
    
ListTypedInfosSalat = List[TypedInfosSalat]


class ParserSalat:
    def __init__(self, path_database:str) -> None:
        self.path_database = path_database
        self.__file_salat = plib.Path(path_database).joinpath("salat.csv")
        self.__df = self.__create_df_infos()
        

    def __create_df_infos(self) -> pd.DataFrame:
        data_frame:ListTypedInfosSalat = []
        for salat in Prayer.parse_list_prayer():
            data_frame.append({
                "number": salat["number"],
                "name": salat['name'],
                "nb_rakat": salat['nb_rakat'],
                "description_salat": salat['description_salat'],
                "link_video": salat["link_video"]

                })
        df = pd.DataFrame(data_frame)
        df.to_csv(self.__file_salat, index=False)
        return df

    @property
    def df(self) -> pd.DataFrame:
        return self.__df
        

class Salat:
    def __init__(self, path_database:str) -> None:
        path = plib.Path(path_database).joinpath('salat.csv')
        if not path.exists():
            self.__df = ParserSalat(path_database).df
        else:
            self.__df = pd.read_csv(path.as_posix())

    @property
    def df(self) -> pd.DataFrame:
        return self.__df

    
    @property
    def fajr(self) -> TypedSalat:
        return Prayer.FAJR

    @property
    def dohr(self) -> TypedSalat:
        return Prayer.DOHR

    @property
    def asr(self) -> TypedSalat:
        return Prayer.ASR

    @property
    def maghrib(self) -> TypedSalat:
        return Prayer.MAGHRIB

    @property
    def isha(self) -> TypedSalat:
        return Prayer.ISHA
