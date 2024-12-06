from typing import TypedDict, List, Union


class TypedPillardOfIslam(TypedDict):
    number: Union[int, str]
    name: str
    description: str
    sources: List[str]
    more_infos: List[str]




class PillardsOfIslam:
    def __init__(self, path_database: str):
        self.path_database = path_database

    @property
    def shahada(self) -> TypedPillardOfIslam:
        return {
            "number": 1,
            "name": "Shahada",
            "description": """La Shahada, ou l'attestation de foi, est le premier pilier de l'Islam. 
            Elle consiste à témoigner qu'il n'y a nulle divinité digne d'être adorée en dehors d'Allah, 
            et que Muhammad est le Messager d'Allah. Cette déclaration est une affirmation 
            fondamentale de la foi islamique et distingue le croyant du non-croyant. 
            La Shahada doit être prononcée avec sincérité et conviction, car elle englobe 
            la soumission totale à Allah, le rejet de toute forme d'associationnisme 
            (shirk), et l'acceptation que Muhammad est le dernier prophète envoyé à l'humanité.""",
            "sources": [
                "Sourate Al-Ikhlas (112:1-4)",
                "Sourate Al-Baqarah (2:163)",
                "Sourate Muhammad (47:19)",
                "Sourate An-Nahl (16:36)",
                "Sourate Al-Anbiya (21:25)",
                "Sourate Al-Ma'idah (5:72)",
                "Sourate Az-Zumar (39:65)",
                "Sourate Al-Fath (48:29)",
                "Sahih Muslim, Hadith 8",
                "Sahih Muslim, Hadith 25",
                "Sahih Al-Bukhari, Hadith 50",
                "Sahih Al-Bukhari, Hadith 5837",
                "Sunan At-Tirmidhi, Hadith 2640",
                "Sunan Ibn Majah, Hadith 3797"
            ],
            "more_infos": [
                "La Shahada est un témoignage essentiel, elle est la base sur laquelle repose la foi musulmane. Elle implique également de suivre les enseignements de Muhammad et de respecter ses recommandations (Sunna).",
                "Le Prophète ﷺ a dit : 'Quiconque témoigne qu'il n'y a pas de divinité digne d'adoration à part Allah, et que Muhammad est Son serviteur et Messager, qu'Isa (Jésus) est le serviteur et messager d'Allah... sera accepté au paradis.' (Sahih Al-Bukhari)",
                "Le Tawhid (unicité d'Allah) est un élément central dans l'attestation de foi, il se divise en trois parties : l'unicité dans la seigneurie d'Allah (Tawhid ar-Rububiyyah), l'unicité dans l'adoration d'Allah (Tawhid al-Uluhiyyah), et l'unicité dans les noms et attributs d'Allah (Tawhid al-Asma' wa Sifat).",
                "La Shahada est une responsabilité et un engagement à vivre conformément aux principes de l'Islam, à adorer Allah seul et à suivre la voie du Prophète Muhammad ﷺ."
            ]
        }
    @property
    def salat(self) -> TypedPillardOfIslam:
        return {
            "number": 2,
            "name": "Salat",
            "description": """La Salat est la prière rituelle et obligatoire des musulmans, elle est le deuxième pilier de l'Islam. 
            Elle est une connexion directe entre le serviteur et Allah et doit être accomplie cinq fois par jour : à l'aube (Fajr), 
            au milieu de la journée (Dhuhr), dans l'après-midi (Asr), au coucher du soleil (Maghrib) et la nuit (Isha). 
            Ces prières servent à purifier le cœur, renforcer la foi, et se rappeler constamment d'Allah.""",
            "sources": [
                "Sourate Al-Baqarah (2:43)",
                "Sourate Al-Baqarah (2:238)",
                "Sourate Al-Ma'idah (5:55)",
                "Sourate Al-Mu’minun (23:2)",
                "Sourate Al-Mu’minun (23:9)",
                "Sourate An-Nisa (4:103)",
                "Sourate Al-Ankabut (29:45)",
                "Sourate Al-Jumu'ah (62:9)",
                "Sahih Muslim, Hadith 657",
                "Sahih Muslim, Hadith 85",
                "Sahih Al-Bukhari, Hadith 8",
                "Sahih Al-Bukhari, Hadith 520",
                "Sunan Abu Dawood, Hadith 393",
                "Sunan An-Nasa'i, Hadith 459"
            ],
            "more_infos": [
                "La Salat est une obligation quotidienne et l'un des actes les plus importants de l'adoration en Islam. Le Prophète ﷺ a dit : 'La différence entre nous et eux est la prière. Celui qui l'abandonne a mécru.' (Sahih Muslim)",
                "La prière est également une protection contre le mal et les actes honteux, comme mentionné dans le Coran (Sourate Al-Ankabut, 29:45).",
                "La Salat se compose de plusieurs positions, dont le Takbir, le Ruku' (inclinaison), le Sujud (prosternation), et le Tashahhud (attestation), et elle doit être accomplie avec concentration et humilité."
            ]
        }


    @property
    def zakat(self) -> TypedPillardOfIslam:
        return {
            "number": 3,
            "name": "Zakat",
            "description": """La Zakat est le troisième pilier de l'Islam. 
            Il s'agit d'une aumône obligatoire que chaque musulman possédant une certaine richesse 
            doit verser pour purifier ses biens et soutenir les personnes dans le besoin. 
            Elle vise à promouvoir la solidarité, à purifier l'âme de l'attachement excessif aux biens matériels 
            et à instaurer l'équité économique au sein de la communauté. 
            Le taux de la Zakat est généralement de 2,5 % des économies annuelles pour les musulmans qui atteignent 
            un certain seuil de richesse, appelé 'nisab'. Elle est un droit des pauvres et un droit d'Allah sur les biens des musulmans.""",
            "sources": [
                "Sourate Al-Baqarah (2:110)",
                "Sourate At-Tawbah (9:60)",
                "Sourate Al-Ma'un (107:1-7)",
                "Sourate Al-Baqarah (2:177)",
                "Sourate Al-Baqarah (2:267)",
                "Sourate Al-Hashr (59:7)",
                "Sahih Muslim, Hadith 987",
                "Sahih Al-Bukhari, Hadith 1400",
                "Sunan Abu Dawood, Hadith 1568",
                "Sunan An-Nasa'i, Hadith 2478"
            ],
            "more_infos": [
                "La Zakat est une obligation qui incombe à tout musulman possédant la richesse nécessaire pour atteindre le seuil du 'nisab'.",
                "Elle est versée pour aider les pauvres, les nécessiteux, ceux qui collectent la Zakat, les endettés, pour libérer les captifs, et pour soutenir les causes justes en Islam, notamment dans le chemin d'Allah, ainsi que les voyageurs en difficulté.",
                "Le Prophète ﷺ a dit : 'L'aumône ne diminue pas la richesse.' (Sahih Muslim)",
                "Ne pas s'acquitter de la Zakat est un péché grave en Islam, comme mentionné dans plusieurs hadiths, où le Prophète ﷺ met en garde contre les conséquences de la négligence de cet acte de culte."
            ]
        }

    @property
    def sawm(self) -> TypedPillardOfIslam:
        return {
            "number": 4,
            "name": "Sawm",
            "description": """Le Sawm, ou le jeûne du mois de Ramadan, est le quatrième pilier de l'Islam. 
            Il consiste à s'abstenir de manger, de boire, et d'autres actes invalidant le jeûne, 
            de l'aube (Fajr) au coucher du soleil (Maghrib). Le jeûne est une forme de purification 
            spirituelle, morale et physique. Son objectif est de rapprocher le musulman d'Allah en renforçant 
            sa foi, sa piété (taqwa), et sa capacité de résilience face aux épreuves. Le jeûne ne se limite 
            pas à l'abstinence physique, mais implique également l'abstinence des paroles et des comportements 
            nuisibles, ainsi qu'une augmentation des actes de bienfaisance, de prière, et de lecture du Coran.""",
            "sources": [
                "Sourate Al-Baqarah (2:183)",
                "Sourate Al-Baqarah (2:185)",
                "Sahih Al-Bukhari, Hadith 1901",
                "Sahih Muslim, Hadith 1151",
                "Sahih Al-Bukhari, Hadith 38",
                "Sourate Al-Qadr (97:1-5)"
            ],
            "more_infos": [
                "Le jeûne du Ramadan est une obligation pour tout musulman adulte, sain d'esprit, en bonne santé, et qui n'est ni en voyage ni dans une condition qui lui permettrait d'en être exempté (comme les femmes enceintes ou en période de menstruation).",
                "Le Prophète ﷺ a dit : 'Quiconque jeûne le mois de Ramadan avec foi et en espérant la récompense d’Allah, ses péchés antérieurs lui seront pardonnés.' (Sahih Al-Bukhari).",
                "Les nuits du Ramadan, en particulier la nuit du Destin (Laylat al-Qadr), sont des moments de prière intense et de supplication, car cette nuit est meilleure que mille mois.",
                "Le Sawm enseigne la patience, la maîtrise de soi, la gratitude envers les bienfaits d'Allah, et la solidarité envers les plus démunis. C’est un moyen de purification du cœur et du corps, ainsi qu’une occasion de renouveler son engagement spirituel.",
                "Le jeûne n'est pas seulement une obligation rituelle mais aussi un moyen de se rappeler l'importance de la piété (taqwa), car Allah dit : 'Ô vous qui avez cru! On vous a prescrit le jeûne comme on l'a prescrit à ceux avant vous, ainsi atteindrez-vous la piété.' (Sourate Al-Baqarah, 2:183)."
            ]
        }

    @property
    def hajj(self) -> TypedPillardOfIslam:
        return {
            "number": 5,
            "name": "Hajj",
            "description": """Le Hajj, ou pèlerinage à la Mecque, est le cinquième et dernier pilier de l'Islam. 
            Il est obligatoire pour tout musulman capable physiquement et financièrement de l'accomplir au moins 
            une fois dans sa vie. Le Hajj se déroule chaque année durant le mois de Dhou al-Hijja, le douzième mois 
            du calendrier islamique. Ce voyage spirituel inclut plusieurs rites importants, tels que le Tawaf autour 
            de la Kaaba, la station à Arafat (où les musulmans implorent Allah pour le pardon), le Sa’i entre Safa et 
            Marwa, et le sacrifice d'un animal en commémoration du sacrifice du prophète Ibrahim (Abraham). 
            Le Hajj est une manifestation de l'unité des musulmans et de leur soumission totale à Allah.""",
            "sources": [
                "Sourate Al-Imran (3:97)",
                "Sourate Al-Hajj (22:27)",
                "Sahih Al-Bukhari, Hadith 1510",
                "Sahih Muslim, Hadith 1218",
                "Sahih Al-Bukhari, Hadith 1444"
            ],
            "more_infos": [
                "Le Hajj est un acte d'adoration qui réunit les musulmans du monde entier, sans distinction de race ou de classe sociale, affirmant l'égalité devant Allah.",
                "Le Prophète ﷺ a dit : 'Accomplissez le Hajj car il efface les péchés comme le feu élimine les impuretés du fer.' (Sahih Al-Bukhari).",
                "Il est recommandé de préparer le Hajj spirituellement et financièrement, en s'assurant de n'avoir aucune dette et de chercher le pardon des autres avant d'entreprendre ce voyage.",
                "Les rites du Hajj rappellent la vie et les épreuves des prophètes Ibrahim (Abraham) et Ismaël, et leur soumission totale à la volonté d'Allah.",
                "Le Hajj est une occasion pour les musulmans de renouveler leur foi, d'implorer le pardon, et de revenir purifiés de leurs péchés. Le Prophète ﷺ a dit : 'Le pèlerinage purifié n’a d’autre récompense que le Paradis.' (Sahih Muslim)."
            ]
        }
