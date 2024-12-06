import requests
from muslimdeenV2.config import Config
from requests.exceptions import HTTPError, Timeout, RequestException
from typing import Union

class Services:
    def __init__(self) -> None:
        pass

    def request_services(self, url: str, to_json: bool = False, to_text: bool = False) -> Union[dict, str, requests.Response]:
        """
        Envoie une requête GET vers l'URL spécifiée et gère les erreurs HTTP.
        
        Args:
            url (str): L'URL de l'API vers laquelle la requête doit être envoyée.
            to_json (bool): Si True, retourne la réponse sous forme de JSON.
            to_text (bool): Si True, retourne la réponse sous forme de texte brut.
        
        Returns:
            Union[dict, str, requests.Response]: Retourne la réponse JSON, texte ou brute selon les options.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            if to_json:
                return response.json()
            elif to_text:
                return response.text
            else:
                return response  

        except HTTPError as http_err:
            raise Exception(f"HTTPError: {http_err}")
        except Timeout:
            raise Exception("Request timeout")
        except RequestException as req_err:
            raise Exception(f"RequestException: {req_err}")
        except Exception as e:
            raise Exception(f"General error: {e}")

    def metadata_off_surahs(self) -> dict:
        """
        Récupère les métadonnées des sourates via une API externe.

        Returns:
            dict: Les métadonnées des sourates sous forme de dictionnaire.
        """
        return self.request_services(Config.url_metada_surahs_v1(), to_json=True)

    def names_of_allah(self) -> str:
        """
        Récupère les 99 noms d'Allah via une API externe.

        Returns:
            str: Les 99 noms d'Allah sous forme de texte brut.
        """
        return self.request_services(Config.url_99_names_of_allah(), to_text=True)


    def quran_to_json(self) -> dict:
        return self.request_services(Config.url_data_quran(), to_json=True)