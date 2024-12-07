from enum import Enum


class DriveTypeEnumDto(str, Enum):
    SSD: str = 'SSD'
    HDD: str = 'HDD'
    UNKNOWN: str = 'UNKNOWN'
