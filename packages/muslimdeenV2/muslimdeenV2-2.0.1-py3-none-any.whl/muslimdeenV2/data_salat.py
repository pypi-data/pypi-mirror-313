from typing import TypedDict, List, Optional, Union, Mapping



class TypedStepSalat(TypedDict):
    step:str
    description:str
    img:Union[str, None]



class TypedSalat(TypedDict):
    number:int
    name:str
    nb_rakat:int
    description_salat:str
    link_video:str
    step_salat: List[TypedStepSalat]




class StepInSalat:

    def introdiuce() -> TypedStepSalat:
        return {
            "step": "Se diriger vers la 'qiblah'",
            "description": "Il te faudra un tapis (ou le sol, ou autre) propre orienté vers la 'qiblah', c'est à dire la direction de la Ka'bah (Kaaba).",
            "img": None
            }

    
    def niya(name_salat:str) -> TypedStepSalat:
        data:TypedStepSalat = {
            "step": "Intention (Niyya)",
            "description" : f"Avoir l'intention dans son cœur d'accomplir la prière du {name_salat}",
            "img": None
            }
        return data
    
    def takbir_al_ihram() -> TypedStepSalat:
        data:TypedStepSalat = {
            "step": "Takbir (Takbirat al-Ihram)",
            "description": "Dire 'Allahu Akbar' en levant les mains à la hauteur des oreilles.",
            "img": "https://www.nospetitsmusulmans.com/pages/islam/images/takbirah.jpg",
            }
        return data

    def al_fatihaa() -> TypedStepSalat:
        return {
            "step": "Position debout (Qiyam)",
            "description": "Placer les mains sur la poitrine et réciter la sourate Al-Fatiha, suivie d'une autre sourate (sunnah).",
            "img": "https://www.nospetitsmusulmans.com/pages/islam/images/tilewah_fetiha.jpg",
            }

    def rukuh() -> TypedStepSalat:
        return {
            "step": "Ruku (Inclinaison)",
            "description": "S'incliner en disant 'Allahu Akbar', jusqu'à ce que tu arrives à avoir le dos parallèle au sol, en étant bien droit, en posant tes mains sur les genoux. puis réciter trois fois 'Subhana Rabbiyal Azeem'",
            "img": "https://www.nospetitsmusulmans.com/pages/islam/images/roukou3oun.jpg"
            }

    def itidal() -> TypedStepSalat:
        return {
            "step": "Revenir à la position debout (I'tidal)",
            "description": "Se redresser en disant 'Sami' Allahu liman hamidah' puis dire 'Rabbana wa lakal-hamd'.",
            "img": None
            }

    def sujud() -> TypedStepSalat:
        return {
            "step": "Sujud (Prosternation)",
            "description": "Se prosterner en disant 'Allahu Akbar',en position de prosternation le front et le nez, ainsi que les dos de tes orteils, les genoux et les paumes des mains touchent le sol. Tu poses tes mains au même niveau que ta tête, les doigts non-écartés les pieds se touchent, et tu dis trois fois 'Subhana Rabbiyal A'la'",
            "img": "https://www.nospetitsmusulmans.com/pages/islam/images/assoujoud.jpg"
            }

    def jalsa() -> TypedStepSalat:
        return {
            "step": "S'asseoir entre les deux prosternations (Jalsa)",
            "description": "Ensuite, tout en disant 'Allâhou Akbar' tu te relèves vers une position assise, tu t'assieds sur ta jambe gauche, que tu gardes bien plate, la jambe droite sort du côté droit de ton corps, de dos de ses orteils touchant le sol. Le pied gauche vient un peu en dessous du creux du pied droit, puis dire 'Rabbighfir li'",
            "img": None
        }

    def serevler(nb_rakat:int) -> TypedStepSalat:
        return {
            "step": "Se relever pour la deuxième rakat",
            "description": "Se relever en disant 'Allahu Akbar', puis réciter de nouveau la sourate Al-Fatiha suivie d'une autre sourate." if nb_rakat > 2 else "Se relever en disant 'Allahu Akbar', puis réciter de nouveau la sourate Al-Fatiha ",
            "img": "https://www.nospetitsmusulmans.com/pages/islam/images/tilewah_fetiha.jpg",
            }

    def tashahhud(first:bool) -> TypedStepSalat:
        return {
            "step": "Tashahhud (Attestation)",
            "description": "Rester en position assise, puis reciter le premier Tashahhud : 'At-tahiyyatoulillah, wa as-salawatou wa tayyibat, assalamou ‘alayka ayyouha nabiyyou wa rahmatoullahi wa barakatouh, assalamou ‘alayna wa ‘ala ‘ibadillahi assalihin, ashhadou an la ilaha illallah wa ashhadou anna mouhammadan ‘abdouhou wa rasoulouh." if first else "Rester en postion assise puis reciter le deuxème Tashahhud 'At-tahiyyatoulillah, wa as-salawatou wa tayyibat, assalamou ‘alayka ayyouha nabiyyou wa rahmatoullahi wa barakatouh, assalamou ‘alayna wa ‘ala ‘ibadillahi assalihin, ashhadou an la ilaha illallah wa ashhadou anna mouhammadan ‘abdouhou wa rasoulouh.', puis ensuite reciter 'Al-Lāhumma ṣalli ‘alā Muhammad wa ´alā āli Muhammad, kamā ṣallayta ‘alā Ibrāhīm wa ´alā āli Ibrāhīm innaka hamīdun Madjīd, Al-Lāhumma barik ‘alā Muhammad wa ´alā āli Muhammad, kamā barakata ‘alā Ibrāhīm wa ´alā āli Ibrāhīm innaka hamīdun Madjīd'",
            "img": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlmFqn14xny7qIPEWl4c1s2e9W9M3O4XeXUA&s"
            }

    def taslim() -> TypedStepSalat:
        return {
            "step": "Salutations finales (Taslim)",
            "description": "Tourner la tête vers la droite en disant 'Assalamu 'alaykum wa rahmatullah', puis vers la gauche en répétant la même phrase.",
            "img": "https://www.nospetitsmusulmans.com/pages/islam/images/taslim.jpg"
            }




class Prayer:    
    FAJR: TypedSalat = {
        "name": 'Fajr (Sobh)',
        "description_salat": "La prière du Fajr (Sobh) est constituée de 2 rakats. Elle se prie avant l'aube et est l'une des cinq prières obligatoires de la journée.",
        "nb_rakat": 2,
        "number": 1,
        "link_video": "https://youtu.be/tZFCbqRtTzk?si=yElvbkLU-buXaJvr",
        "step_salat": [
            StepInSalat.introdiuce(),           
            StepInSalat.niya("Fajr"),           
            StepInSalat.takbir_al_ihram(),      
            StepInSalat.al_fatihaa(),           
            StepInSalat.rukuh(),                
            StepInSalat.itidal(),               
            StepInSalat.sujud(),                
            StepInSalat.jalsa(),                
            StepInSalat.sujud(),                
            StepInSalat.serevler(2),            
            StepInSalat.al_fatihaa(),           
            StepInSalat.rukuh(),                
            StepInSalat.itidal(),               
            StepInSalat.sujud(),                
            StepInSalat.jalsa(),                
            StepInSalat.sujud(),                
            StepInSalat.tashahhud(first=False), 
            StepInSalat.taslim()          
        ]
    }

    DOHR: TypedSalat = {
        "name": 'Dohr (Dhuhr)',
        "description_salat": "La prière du Dohr (Dhuhr) est constituée de 4 rakats. Elle se prie après le zénith (midi) et est l'une des cinq prières obligatoires de la journée.",
        "nb_rakat": 4,
        "number": 2,
        "link_video": "https://youtu.be/X2aJcTFbmUg?si=0HPj5pwNdVMmJ8WV",
        "step_salat": [
            StepInSalat.introdiuce(),           # 1
            StepInSalat.niya("Dohr"),           # 2
            StepInSalat.takbir_al_ihram(),      # 3
            StepInSalat.al_fatihaa(),           # 4
            StepInSalat.rukuh(),                # 5
            StepInSalat.itidal(),               # 6
            StepInSalat.sujud(),                # 7
            StepInSalat.jalsa(),                # 8
            StepInSalat.sujud(),                # 9
            StepInSalat.serevler(4),            # 10
            StepInSalat.al_fatihaa(),           # 11
            StepInSalat.rukuh(),                # 12
            StepInSalat.itidal(),               # 13
            StepInSalat.sujud(),                # 14
            StepInSalat.jalsa(),                # 15
            StepInSalat.sujud(),                # 16
            StepInSalat.tashahhud(first=True),  # 17
            StepInSalat.serevler(4),            # 18
            StepInSalat.al_fatihaa(),           # 19
            StepInSalat.rukuh(),                # 20
            StepInSalat.itidal(),               # 21
            StepInSalat.sujud(),                # 22
            StepInSalat.jalsa(),                # 23
            StepInSalat.sujud(),                # 24
            StepInSalat.serevler(4),            # 25
            StepInSalat.al_fatihaa(),           # 26
            StepInSalat.rukuh(),                # 27
            StepInSalat.itidal(),               # 28
            StepInSalat.sujud(),                # 29
            StepInSalat.jalsa(),                # 30
            StepInSalat.sujud(),                # 31
            StepInSalat.tashahhud(first=False), # 32
            StepInSalat.taslim()             #33 
        ]
    }
    
    ASR: TypedSalat = {
        "name": 'Asr (Al-‘Asr)',
        "description_salat": "La prière de Asr (Al-‘Asr) est constituée de 4 rakats. Elle se prie en fin d'après-midi et est l'une des cinq prières obligatoires de la journée.",
        "nb_rakat": 4,
        "number": 3,
        "link_video": "https://youtu.be/fK_29jqmavA?si=nspDImx4MHG6Y4k9",
        "step_salat": [
            StepInSalat.introdiuce(),           # 1
            StepInSalat.niya("Asr"),            # 2
            StepInSalat.takbir_al_ihram(),      # 3
            StepInSalat.al_fatihaa(),           # 4
            StepInSalat.rukuh(),                # 5
            StepInSalat.itidal(),               # 6
            StepInSalat.sujud(),                # 7
            StepInSalat.jalsa(),                # 8
            StepInSalat.sujud(),                # 9
            StepInSalat.serevler(4),            # 10
            StepInSalat.al_fatihaa(),           # 11
            StepInSalat.rukuh(),                # 12
            StepInSalat.itidal(),               # 13
            StepInSalat.sujud(),                # 14
            StepInSalat.jalsa(),                # 15
            StepInSalat.sujud(),                # 16
            StepInSalat.tashahhud(first=True),  # 17
            StepInSalat.serevler(4),            # 18
            StepInSalat.al_fatihaa(),           # 19
            StepInSalat.rukuh(),                # 20
            StepInSalat.itidal(),               # 21
            StepInSalat.sujud(),                # 22
            StepInSalat.jalsa(),                # 23
            StepInSalat.sujud(),                # 24
            StepInSalat.serevler(4),            # 25
            StepInSalat.al_fatihaa(),           # 26
            StepInSalat.rukuh(),                # 27
            StepInSalat.itidal(),               # 28
            StepInSalat.sujud(),                # 29
            StepInSalat.jalsa(),                # 30
            StepInSalat.sujud(),                # 31
            StepInSalat.tashahhud(first=False), # 32
            StepInSalat.taslim()                # 33
        ]
    }

    MAGHRIB: TypedSalat = {
        "name": 'Maghrib',
        "description_salat": "La prière du Maghrib est constituée de 3 rakats. Elle se prie juste après le coucher du soleil et est l'une des cinq prières obligatoires de la journée.",
        "nb_rakat": 3,
        "number": 4,
        "link_video": "https://youtu.be/VmEm-H7-KnI?si=TwX3DllVaU-7JEuB",
        "step_salat": [
            StepInSalat.introdiuce(),           # 1. Se diriger vers la qiblah
            StepInSalat.niya("Maghrib"),        # 2. Intention (Niyya)
            StepInSalat.takbir_al_ihram(),      # 3. Takbir (Takbirat al-Ihram)
            StepInSalat.al_fatihaa(),           # 4. Position debout (Qiyam) avec Al-Fatiha et une autre sourate
            StepInSalat.rukuh(),                # 5. Ruku (Inclinaison)
            StepInSalat.itidal(),               # 6. Revenir à la position debout (I'tidal)
            StepInSalat.sujud(),                # 7. Sujud (Prosternation)
            StepInSalat.jalsa(),                # 8. S'asseoir entre les deux prosternations (Jalsa)
            StepInSalat.sujud(),                # 9. Deuxième Sujud
            StepInSalat.serevler(3),            # 10. Se relever pour la deuxième rakat
            StepInSalat.al_fatihaa(),           # 11. Al-Fatiha dans la deuxième rakat
            StepInSalat.rukuh(),                # 12. Ruku dans la deuxième rakat
            StepInSalat.itidal(),               # 13. Revenir à la position debout (I'tidal)
            StepInSalat.sujud(),                # 14. Sujud dans la deuxième rakat
            StepInSalat.jalsa(),                # 15. S'asseoir entre les deux prosternations (Jalsa)
            StepInSalat.sujud(),                # 16. Deuxième Sujud
            StepInSalat.tashahhud(first=True),  # 17. Premier Tashahhud
            StepInSalat.serevler(3),            # 18. Se relever pour la troisième rakat
            StepInSalat.al_fatihaa(),           # 19. Al-Fatiha dans la troisième rakat
            StepInSalat.rukuh(),                # 20. Ruku dans la troisième rakat
            StepInSalat.itidal(),               # 21. Revenir à la position debout (I'tidal)
            StepInSalat.sujud(),                # 22. Sujud dans la troisième rakat
            StepInSalat.jalsa(),                # 23. S'asseoir entre les deux prosternations (Jalsa)
            StepInSalat.sujud(),                # 24. Deuxième Sujud
            StepInSalat.tashahhud(first=False), # 25. Tashahhud final
            StepInSalat.taslim()                # 26. Salutations finales (Taslim)
        ]
    }


    ISHA: TypedSalat = {
        "name": 'Isha',
        "description_salat": "La prière du Isha est constituée de 4 rakats. Elle se prie après la tombée de la nuit et est l'une des cinq prières obligatoires de la journée.",
        "nb_rakat": 4,
        "number": 5,
        "link_video": "https://youtu.be/tZFCbqRtTzk?si=B0qUF3encDf-41vZ",
        "step_salat": [
            StepInSalat.introdiuce(),           # 1. Se diriger vers la qiblah
            StepInSalat.niya("Isha"),           # 2. Intention (Niyya)
            StepInSalat.takbir_al_ihram(),      # 3. Takbir (Takbirat al-Ihram)
            StepInSalat.al_fatihaa(),           # 4. Position debout (Qiyam) avec Al-Fatiha et une autre sourate
            StepInSalat.rukuh(),                # 5. Ruku (Inclinaison)
            StepInSalat.itidal(),               # 6. Revenir à la position debout (I'tidal)
            StepInSalat.sujud(),                # 7. Sujud (Prosternation)
            StepInSalat.jalsa(),                # 8. S'asseoir entre les deux prosternations (Jalsa)
            StepInSalat.sujud(),                # 9. Deuxième Sujud
            StepInSalat.serevler(4),            # 10. Se relever pour la deuxième rakat
            StepInSalat.al_fatihaa(),           # 11. Al-Fatiha dans la deuxième rakat
            StepInSalat.rukuh(),                # 12. Ruku dans la deuxième rakat
            StepInSalat.itidal(),               # 13. Revenir à la position debout (I'tidal)
            StepInSalat.sujud(),                # 14. Sujud dans la deuxième rakat
            StepInSalat.jalsa(),                # 15. S'asseoir entre les deux prosternations (Jalsa)
            StepInSalat.sujud(),                # 16. Deuxième Sujud
            StepInSalat.tashahhud(first=True),  # 17. Premier Tashahhud
            StepInSalat.serevler(4),            # 18. Se relever pour la troisième rakat
            StepInSalat.al_fatihaa(),           # 19. Al-Fatiha dans la troisième rakat
            StepInSalat.rukuh(),                # 20. Ruku dans la troisième rakat
            StepInSalat.itidal(),               # 21. Revenir à la position debout (I'tidal)
            StepInSalat.sujud(),                # 22. Sujud dans la troisième rakat
            StepInSalat.jalsa(),                # 23. S'asseoir entre les deux prosternations (Jalsa)
            StepInSalat.sujud(),                # 24. Deuxième Sujud
            StepInSalat.serevler(4),            # 25. Se relever pour la quatrième rakat
            StepInSalat.al_fatihaa(),           # 26. Al-Fatiha dans la quatrième rakat
            StepInSalat.rukuh(),                # 27. Ruku dans la quatrième rakat
            StepInSalat.itidal(),               # 28. Revenir à la position debout (I'tidal)
            StepInSalat.sujud(),                # 29. Sujud dans la quatrième rakat
            StepInSalat.jalsa(),                # 30. S'asseoir entre les deux prosternations (Jalsa)
            StepInSalat.sujud(),                # 31. Deuxième Sujud
            StepInSalat.tashahhud(first=False), # 32. Tashahhud final
            StepInSalat.taslim()                # 33. Salutations finales (Taslim)
        ]
    }

    def parse_list_prayer() -> List[TypedSalat]:
        return [Prayer.FAJR, Prayer.DOHR, Prayer.ASR, Prayer.MAGHRIB, Prayer.ISHA]
