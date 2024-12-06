from ks_constants.devs import Developer
from ks_constants.locale import Language


from enum import Enum


class Team(Enum):
    Survivor = (0, 8)
    Kerrigan = (1, 2)

    def __init__(self, _id: int, max_players: int):
        self._id = _id
        self._max_team_size = max_players

    def get_max_size(self):
        return self._max_team_size

    def to_int(self):
        return self._id

    @classmethod
    def from_index(cls, index):
        if not isinstance(index, int):
            try:
                index = int(index)
            except ValueError:
                print(f'Index provided is not an integer: {index}')
        return Team.Survivor if index == 0 else Team.Kerrigan


class RoleType(Enum):
    Builder = (0, Team.Survivor)
    Support = (1, Team.Survivor)
    Defender = (2, Team.Kerrigan)
    Hunter = (3, Team.Kerrigan)

    def __init__(self, _id: int, team: Team):
        self._id = _id
        self._team = team

    def get_team(self) -> Team:
        return self._team

    def to_int(self):
        return self._id

class Role(Enum):
    Kerrigan = (0, RoleType.Hunter, {Language.Chinese: '凯瑞甘', Language.English: 'Kerrigan', Language.Korean: '케리건'}, Developer.Geo, Developer.Luminous, True)
    Scientist = (1, RoleType.Builder, {Language.Chinese: '科学家', Language.English: 'Scientist', Language.Korean: '과학자'}, Developer.Geo, Developer.Luminous, True)
    Dark_Templar = (2, RoleType.Support, {Language.Chinese: '黑暗圣堂武士', Language.English: 'Dark Templar', Language.Korean: '암흑기사'}, Developer.Geo, Developer.Luminous, True)
    Ascendant = (3, RoleType.Builder, {Language.Chinese: '晋升者', Language.English: 'Ascendant', Language.Korean: '승천자'}, Developer.Luminous, None, True)
    Spirit = (4, RoleType.Builder, {Language.Chinese: '灵魂', Language.English: 'Spirit', Language.Korean: '혼령'}, Developer.Luminous, None, True)
    Ares = (5, RoleType.Builder, {Language.Chinese: '阿瑞斯', Language.English: 'Ares', Language.Korean: '아레스'}, Developer.Luminous, None, True)
    Prophet = (6, RoleType.Support, {Language.Chinese: '先知', Language.English: 'Prophet', Language.Korean: '선지자'}, Developer.Luminous, None, True)
    Stukov = (7, RoleType.Builder, {Language.Chinese: '斯托科夫', Language.English: 'Stukov', Language.Korean: '스투코프'}, Developer.Luminous, None, True)
    Artanis = (8, RoleType.Builder, {Language.Chinese: '无敌的大主教', Language.English: 'Artanis', Language.Korean: '아르타니스'}, Developer.Luminous, None, True)
    Zagara = (9, RoleType.Defender, {Language.Chinese: '扎加拉', Language.English: 'Zagara', Language.Korean: '자가라'}, Developer.Luminous, None, True)
    Engineer = (10, RoleType.Builder, {Language.Chinese: '工程师', Language.English: 'Engineer', Language.Korean: '공학자'}, Developer.Luminous, None, True)
    Team_Nova = (11, RoleType.Support, {Language.Chinese: '诺娃团队', Language.English: 'Team Nova', Language.Korean: '팀노바'}, Developer.Luminous, None, True)
    Nomad = (12, RoleType.Builder, {Language.Chinese: '游牧民', Language.English: 'Nomad', Language.Korean: '유랑선'}, Developer.Luminous, None, True)
    Dehaka = (13, RoleType.Hunter, {Language.Chinese: '德哈卡', Language.English: 'Dehaka', Language.Korean: '데하카'}, Developer.Luminous, None, True)
    Helios = (14, RoleType.Builder, {Language.Chinese: '赫利俄斯', Language.English: 'Helios', Language.Korean: '헬리오스'}, Developer.Luminous, None, True)
    Random = (15, None, {Language.Chinese: '整点乐子', Language.English: 'Random', Language.Korean: '무작위'}, Developer.Luminous, None, True)
    Thakras = (16, RoleType.Hunter, {Language.Chinese: '塔克拉斯', Language.English: 'Thakras', Language.Korean: '타크라스'}, Developer.Luminous, None, True)
    Swann = (17, RoleType.Builder, {Language.Chinese: '斯旺', Language.English: 'Swann', Language.Korean: '스완'}, Developer.Luminous, None, True)
    Warden = (18, RoleType.Support, {Language.Chinese: '监管者', Language.English: 'Warden', Language.Korean: '수호자'}, Developer.Luminous, None, True)
    Selendis = (19, RoleType.Builder, {Language.Chinese: '塞兰迪斯', Language.English: 'Selendis', Language.Korean: '셀렌디스'}, Developer.Hex, Developer.Hex, True)
    Niadra = (20, RoleType.Defender, {Language.Chinese: '尼亚德拉', Language.English: 'Niadra', Language.Korean: '니아드라'}, Developer.Luminous, None, True)
    Mira = (21, RoleType.Builder, {Language.Chinese: '米拉', Language.English: 'Mira', Language.Korean: '미라'}, Developer.Luminous, None, True)
    Scion = (22, RoleType.Support, {Language.Chinese: '赛恩', Language.English: 'Scion', Language.Korean: '후계자'}, Developer.Luminous, None, True)
    Technician = (23, RoleType.Builder, {Language.Chinese: '技术员', Language.English: 'Technician', Language.Korean: '기술자'}, Developer.Fatline, Developer.Gcloud, True)
    Warfield = (24, RoleType.Builder, {Language.Chinese: '沃菲尔德', Language.English: 'Warfield', Language.Korean: '워필드'}, Developer.Fatline, Developer.Understudy, True)
    Champion = (25, RoleType.Builder, {Language.Chinese: '冠军', Language.English: 'Champion', Language.Korean: '챔피언'}, Developer.Luminous, None, True)
    Elementalist = (26, RoleType.Support, {Language.Chinese: '元素使', Language.English: 'Elementalist', Language.Korean: '원소술사'}, Developer.Fatline, Developer.Sox, True)
    Brakk = (27, RoleType.Hunter, {Language.Chinese: '巴拉克', Language.English: 'Brakk', Language.Korean: '브라크'}, Developer.Fatline, Developer.Gcloud, True)
    Glevig = (28, RoleType.Defender, {Language.Chinese: '格里维格', Language.English: 'Glevig', Language.Korean: '글레빅'}, Developer.Fatline, Developer.Understudy, True)
    Delta_Squad = (29, RoleType.Support, {Language.Chinese: '三角洲小队', Language.English: 'Delta Squad', Language.Korean: '델타 특공대'}, Developer.Luminous, None, True)
    Phaegore = (30, RoleType.Defender, {Language.Chinese: '菲戈尔', Language.English: 'Phaegore', Language.Korean: '파에고르'}, Developer.Templar, None, True)
    Alarak = (31, RoleType.Builder, {Language.Chinese: '阿拉纳克', Language.English: 'Alarak', Language.Korean: '알라라크'}, Developer.Luminous, None, True)
    Izsha = (32, RoleType.Defender, {Language.Chinese: '伊兹莎', Language.English: 'Izsha', Language.Korean: '이즈샤'}, Developer.Susu, None, True)
    Malus = (33, RoleType.Hunter, {Language.Chinese: '马吕斯', Language.English: 'Malus', Language.Korean: '말러스'}, Developer.Susu, None, True)
    Kraith = (34, RoleType.Hunter, {Language.Chinese: '克雷斯', Language.English: 'Kraith', Language.Korean: '크레이스'}, Developer.Templar, None, True)
    Energizer = (35, RoleType.Builder, {Language.Chinese: '激励者', Language.English: 'Energizer', Language.Korean: '에너자이저'}, Developer.Fatline, Developer.Sox, True)
    Andor = (36, RoleType.Builder, {Language.Chinese: '亚顿', Language.English: 'Andor', Language.Korean: '안도르'}, Developer.Korneel, None, True)
    DJ = (37, RoleType.Builder, {Language.Chinese: '', Language.English: 'DJ', Language.Korean: '디제이'}, Developer.Sox, None, True)
    Rattlesnake = (38, RoleType.Support, {Language.Chinese: '凯文', Language.English: 'Rattlesnake', Language.Korean: '방울뱀'}, Developer.Legacy, Developer.Gcloud, True)
    SgtHammer = (39, RoleType.Builder, {Language.Chinese: '重锤军士', Language.English: 'SgtHammer', Language.Korean: '해머 상사'}, Developer.Archlei, Developer.Hex, True)
    Chew = (40, RoleType.Support, {Language.Chinese: '秋伊', Language.English: 'Chew', Language.Korean: '추'}, Developer.Sox, None, True)
    Aewyn = (41, RoleType.Builder, {Language.Chinese: '”先驱者“艾尔文', Language.English: 'Aewyn', Language.Korean: '애윈'}, Developer.Luminous, None, True)
    Critter_Lord = (42, RoleType.Builder, {Language.Chinese: '小动物主宰', Language.English: 'Critter Lord', Language.Korean: '곤충 왕'}, Developer.Korneel, None, True)
    Nightingale = (43, RoleType.Support, {Language.English: 'Nightingale'}, Developer.Luminous, None, True)
    Sjlerk = (44, RoleType.Support, {Language.English :'Sjlerk'}, Developer.Korneel, None, True)
    Sophia = (45, RoleType.Builder, {Language.English :'Sophia'}, Developer.Korneel, None, True)
    Jinara = (46, RoleType.Builder, {Language.English :'Jinara'}, Developer.Fern, None, True)

    def __init__(self,
                 _id: int,
                 role_type: RoleType,
                 name: dict,
                 original_author: Developer,
                 current_author: Developer,
                 available: bool
                 ):
        self._index = _id
        self._name = name
        self._role_type = role_type
        self._original_author = original_author
        self._current_author = original_author if current_author is None else current_author
        self._available = available

    @classmethod
    def from_index(cls, index):
        if not isinstance(index, int):
            try:
                index = int(index)
            except ValueError:
                print(f'Index provided is not an integer: {index}')
        return _roles_list[index]

    @classmethod
    def from_name(cls, name):
        for role in Role:
            if role.name == name:
                return role
        return None

    def get_index(self):
        return self._index

    def get_team(self) -> Team:
        if self == Role.Random:
            raise TypeError("Random does not have a team")
        return self._role_type.get_team()

    def get_role_type(self) -> RoleType:
        return self._role_type

    def get_name(self, locale: Language = Language.English) -> str:
        return self._name[locale]
    
    def get_english_name(self):
        return self.get_name(Language.English)

    def get_original_author(self) -> Developer:
        return self._original_author

    def get_current_author(self):
        return self._current_author

    def is_available(self):
        return self._available

_roles_list = list(Role)
