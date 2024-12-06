from enum import IntEnum
from enum import unique


@unique
class StatusCode(IntEnum):
    """Код для статуса (statusCode) атрибута orgCode."""

    CODE_110: int = 110
    CODE_120: int = 120
    CODE_130: int = 130
    CODE_140: int = 140
    CODE_150: int = 150
    CODE_160: int = 160
    CODE_170: int = 170
    CODE_180: int = 180
    CODE_190: int = 190
    CODE_210: int = 210
    CODE_220: int = 220
    CODE_230: int = 230
    CODE_240: int = 240
    CODE_250: int = 250


@unique
class StatusTechCode(IntEnum):
    """Код для статуса (statusCode) атрибута techCode."""

    CODE_1: int = 1
    CODE_3: int = 3
    CODE_4: int = 4
