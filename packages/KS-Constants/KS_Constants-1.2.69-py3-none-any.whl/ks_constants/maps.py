from enum import Enum
from ks_constants.devs import Developer
from ks_constants.locale import Language
import os

KS2_MAPS_DIRECTORY = "ks2-maps"

class Map(Enum):
    Classic = (0,
               {
                   Language.Chinese: '经典永存',
                   Language.English: 'Classic',
                   Language.Korean: '기본'
               },
               "CLASSIC",
               Developer.Luminous,
               [os.path.join("Base.SC2Data", "GameData", "Terrain", "Classic.xml")],
               os.path.join(KS2_MAPS_DIRECTORY, "classic.SC2Map"),
               False,
               True,
               False,
               Developer.Luminous)
    Duck_Map = (1,
                {
                    Language.Chinese: '鸭鸭',
                    Language.English: 'Duck Map',
                    Language.Korean: '오리'
                },
                "DUCK_MAP",
                Developer.Duck,
                [os.path.join("Base.SC2Data", "GameData", "Terrain", "DuckMap.xml")],
                os.path.join(KS2_MAPS_DIRECTORY, "duck_map.SC2Map"),
                False,
                True,
                False,
                None)
    Zerus_Volcanoes = (2,
                       {
                           Language.Chinese: '泽鲁斯火山',
                           Language.English: 'Zerus Volcanoes',
                           Language.Korean: '제루스 화산'
                       },
                       "ZERUS_VOLCANOES",
                       Developer.Luminous,
                       [os.path.join("Base.SC2Data", "GameData", "Terrain", "ZerusVolcanoes.xml")],
                       os.path.join(KS2_MAPS_DIRECTORY, "zerus_volcanoes.SC2Map"),
                       False,
                       False,
                       False,
                       None)
    Ruins_Of_Imladoon = (3,
                         {
                             Language.Chinese: '伊姆拉杜恩遗址',
                             Language.English: 'Ruins of Imladoon',
                             Language.Korean: '임라둔의 잔해'
                         },
                         "RUINS_OF_IMLADOON",
                         Developer.Fatline,
                         [os.path.join("Base.SC2Data", "GameData", "Terrain", "RuinsOfImladoon.xml")],
                         os.path.join(KS2_MAPS_DIRECTORY, "ruins_of_imladoon.SC2Map"),
                         False,
                         False,
                         True,
                         Developer.Templar)
    Four_Seasons = (4,
                    {
                        Language.Chinese: '四季交叠',
                        Language.English: 'Four Seasons',
                        Language.Korean: '사계절'
                    },
                    "FOUR_SEASONS",
                    Developer.Luminous,
                    [os.path.join("Base.SC2Data", "GameData", "Terrain", "FourSeasons.xml")],
                    os.path.join(KS2_MAPS_DIRECTORY, "four_seasons.SC2Map"),
                    True,
                    False,
                    False,
                    None)
    Heart_Of_Amethyst = (5,
                         {
                             Language.Chinese: '紫水晶之心',
                             Language.English: 'Heart of Amethyst',
                             Language.Korean: '자수정의 심장'},
                         "HEART_OF_AMETHYST",
                         Developer.Luminous,
                         [os.path.join("Base.SC2Data", "GameData", "Terrain", "HeartOfAmethyst.xml")],
                         os.path.join(KS2_MAPS_DIRECTORY, "heart_of_amethyst.SC2Map"),
                         False,
                         False,
                         False,
                         None)
    Vintage_Shores = (6,
                      {
                          Language.Chinese: '夏日海滩',
                          Language.English: 'Vintage Shores',
                          Language.Korean: '빈티지 해변'
                      },
                      "VINTAGE_SHORES",
                      Developer.Templar,
                      [os.path.join("Base.SC2Data", "GameData", "Terrain", "VintageShores.xml")],
                      os.path.join(KS2_MAPS_DIRECTORY, "vintage_shores.SC2Map"),
                      False,
                      False,
                      True,
                      None)
    Aiur_Fountains = (7,
                      {
                          Language.Chinese: '艾尔之泉',
                          Language.English: 'Aiur Fountains',
                          Language.Korean: '아이어 분수'
                      },
                      "AIUR_FOUNTAINS",
                      Developer.Luminous,
                      [os.path.join("Base.SC2Data", "GameData", "Terrain", "AiurFountains.xml")],
                      os.path.join(KS2_MAPS_DIRECTORY, "aiur_fountains.SC2Map"),
                      True,
                      False,
                      False,
                      None)
    Kaldir_Cliffs = (8,
                     {
                         Language.Chinese: '冰封王座',
                         Language.English: 'Kaldir Cliffs',
                         Language.Korean: '칼디르 절벽'
                     },
                     "KALDIR_CLIFFS",
                     Developer.Understudy,
                     [os.path.join("Base.SC2Data", "GameData", "Terrain", "KaldirCliffs.xml")],
                     os.path.join(KS2_MAPS_DIRECTORY, "kaldir_cliffs.SC2Map"),
                     False,
                     False,
                     False,
                     None)
    Lost_Tides = (9,
                     {
                         Language.Chinese: '失意之汐',
                         Language.English: 'Lost Tides',
                         Language.Korean: '잃어버린 강'
                     },
                     "LOST_TIDES",
                     Developer.Templar,
                     [os.path.join("Base.SC2Data", "GameData", "Terrain", "LostTides.xml")],
                     os.path.join(KS2_MAPS_DIRECTORY, "lost_tides.SC2Map"),
                     True,
                     False,
                     False,
                     Developer.Templar)
    Death_Valley = (10,
                     {
                         Language.Chinese: '死亡峡谷',
                         Language.English: 'Death Valley',
                         Language.Korean: '죽음의 골짜기'
                     },
                     "DEATH_VALLEY",
                     Developer.Fatline,
                     [os.path.join("Base.SC2Data", "GameData", "Terrain", "DeathValley.xml")],
                     os.path.join(KS2_MAPS_DIRECTORY, "death_valley.SC2Map"),
                     True,
                     True,
                     True,
                     None)                     
    Snow_Prism = (11,
                     {
                         Language.Chinese: '',
                         Language.English: 'Snow Prism',
                         Language.Korean: '눈 프리즘'
                     },
                     "SNOW_PRISM",
                     Developer.Luminous,
                     [os.path.join("Base.SC2Data", "GameData", "Terrain", "SnowPrism.xml")],
                     os.path.join(KS2_MAPS_DIRECTORY, "snow_prism.SC2Map"),
                     True,
                     False,
                     False,
                     Developer.Luminous)

    Aduns_Forgotten_Temple = (12,
                     {
                         Language.Chinese: '',
                         Language.English: "Adun's Forgotten Temple",
                         Language.Korean: "아둔의 잊혀진 사원"
                     },
                     "ADUNS_FORGOTTEN_TEMPLE",
                     Developer.Luminous,
                     [],
                     os.path.join(KS2_MAPS_DIRECTORY, "adun_temple.SC2Map"),
                     True,
                     False,
                     False,
                     Developer.Luminous)

    Maze = (13,
                     {
                         Language.Chinese: '',
                         Language.English: "Maze",
                         Language.Korean: "미로"
                     },
                     "MAZE",
                     Developer.Azaz,
                     [],
                     os.path.join(KS2_MAPS_DIRECTORY, "maze.SC2Map"),
                     True,
                     False,
                     False,
                     Developer.Luminous)
    Canal = (14,
                     {
                         Language.Chinese: '',
                         Language.English: "Canal",
                         Language.Korean: "운하"
                     },
                     "CANAL",
                     Developer.Azaz,
                     [],
                     os.path.join(KS2_MAPS_DIRECTORY, "canal.SC2Map"),
                     True,
                     False,
                     False,
                     Developer.Luminous)
    Sand_Fort = (15,
                     {
                         Language.Chinese: '',
                         Language.English: "Sand Fort",
                         Language.Korean: "모래 요새"
                     },
                     "SAND_FORT",
                     Developer.Azaz,
                     [os.path.join("Base.SC2Data", "GameData", "Terrain", "SandFort.xml")],
                     os.path.join(KS2_MAPS_DIRECTORY, "sand_fort.SC2Map"),
                     True,
                     False,
                     False,
                     Developer.Luminous)
    Mar_Sara_Wastelands = (16,
                     {
                         Language.Chinese: '',
                         Language.English: "Mar Sara Wastelands",
                         Language.Korean: "Mar Sara 황무지"
                     },
                     "MAR_SARA_WASTELANDS",
                     None,
                     [],
                     os.path.join(KS2_MAPS_DIRECTORY, "mar_sara_wastelands.SC2Map"),
                     True,
                     False,
                     False,
                     Developer.Luminous)
    Last_Sanctuary = (17,
                     {
                         Language.Chinese: '',
                         Language.English: "Last Sanctuary",
                         Language.Korean: "최후의 성소"
                     },
                     "LAST_SANCTUARY",
                     None,
                     [os.path.join("Base.SC2Data", "GameData", "Terrain", "LastSanctuary.xml")],
                     os.path.join(KS2_MAPS_DIRECTORY, "last_sanctuary.SC2Map"),
                     True,
                     True,
                     False,
                     Developer.Feanor)
    No_Hope = (18,
                     {
                         Language.Chinese: '',
                         Language.English: "No Hope",
                         Language.Korean: ""
                     },
                     "NO_HOPE",
                     None,
                     [os.path.join("Base.SC2Data", "GameData", "Terrain", "NoHope.xml")],
                     os.path.join(KS2_MAPS_DIRECTORY, "no_hope.SC2Map"),
                     False,
                     True,
                     False,
                     Developer.SmugWyrmling)
    # galaxy representation is the string value of the Preset in KS2 Galaxy
    def __init__(self,
                 index: int,
                 name_dict: dict[Language, str],
                 galaxy_representation: str,
                 original_author: Developer,
                 custom_file_list: list[str],
                 file_path: str,
                 is_disliked: bool = False, # whether community has downvoted map
                 is_active: bool = False, # whether the map is in the current pool
                 is_retired: bool = False, # whether the map SHOULD NOT APPEAR in the pool (used only for future reference/book keeping)
                 current_author: Developer = None):
        self._index = index
        self._name_dict = name_dict
        self._galaxy_representation = galaxy_representation
        self._custom_file_list = custom_file_list
        self._file_path = file_path
        self._original_author = original_author
        self._current_author = original_author if current_author is None else current_author
        self._is_disliked = is_disliked
        self._is_retired = is_retired
        self._is_active = is_active

    @classmethod
    def from_index(cls, index):
        return _maps_list[index]

    def get_index(self):
        return self._index

    def get_name(self, locale: Language):
        return self._name_dict[locale]

    def get_english_name(self):
        return self.get_name(Language.English)

    def get_galaxy_representation(self):
        return self._galaxy_representation

    def original_author(self):
        return self._original_author

    def current_author(self):
        return self._current_author

    def file_path(self):
        return self._file_path

    def is_disliked(self):
        return self._is_disliked

    def is_active(self):
        return self._is_active

    def is_retired(self):
        return self._is_retired

    def custom_file_list(self):
        return self._custom_file_list


_maps_list = list(Map)
