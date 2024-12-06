class Config:
    
    @staticmethod
    def url_metada_surahs_v1() -> str:
        """
        Retourne l'URL de l'API pour les métadonnées des sourates.
        
        Returns:
            str: URL de l'API pour les métadonnées des sourates.
        """
        return "https://api.alquran.cloud/v1/meta"

    @staticmethod
    def url_data_quran() -> str:
        """
        Retourne l'URL pour les données du Coran.

        Returns:
            str: URL de l'API ou du dépôt pour les données du Coran.
        """
        return "https://raw.githubusercontent.com/mehdi-stark/Coran-Quran/refs/heads/master/quran.json"
        


    @staticmethod
    def author_quran_github() -> str:
        return "https://github.com/mehdi-stark"

    @staticmethod
    def url_99_names_of_allah() -> str:
        return "https://myislam.org/fr/99-noms-dallah/"
