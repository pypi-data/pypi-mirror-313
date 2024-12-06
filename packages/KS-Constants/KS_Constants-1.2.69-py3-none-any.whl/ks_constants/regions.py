from enum import Enum
from .locale import Language

class Region(Enum):
    North_America = (
        1,
        {
            Language.Chinese: '北美',
            Language.English: 'NA',
            Language.Korean: '북미'
        },
        "US"
    )
    Europe = (
        2,
        {
            Language.Chinese: '欧洲',
            Language.English: 'EU',
            Language.Korean: '유럽'
        },
        "EU"
    )
    Korea = (
        3,
        {
            Language.Chinese: '韩国',
            Language.English: 'KR',
            Language.Korean: '한국'
        },
        "KR"
    )
    China = (
        5,
        {
            Language.Chinese: '中国',
            Language.English: 'CN',
            Language.Korean: '중국'
        },
        "CN"
    )

    @classmethod
    def from_index(cls, index):
        if not isinstance(index, int):
            try:
                index = int(index)
            except ValueError:
                print(f'Index provided is not an integer: {index}')
        return _region_map[index]

    # auth_code is the name of the region on the SC2Editor publish screen for authenticating into the region
    def __init__(self, region_id: int, codes: dict[Language, str], auth_code: str):
        self._region_id = region_id
        self._codes = codes
        self._auth_code = auth_code

    def get_code(self, locale: Language):
        return self._codes[locale]
    
    def get_region_id(self):
        return self._region_id

    def get_auth_code(self):
        return self._auth_code

    def get_chinese_code(self):
        return self.get_code(Language.Chinese)

    def get_english_code(self):
        return self.get_code(Language.English)

    def get_korean_code(self):
        return self.get_code(Language.Korean)

_region_map = dict([(r.get_region_id(), r) for r in Region])