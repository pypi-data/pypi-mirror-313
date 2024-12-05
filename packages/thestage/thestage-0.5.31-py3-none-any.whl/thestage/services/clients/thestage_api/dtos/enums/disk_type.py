from enum import Enum


class DiskTypeEnumDto(str, Enum):
    SSD: str = 'SSD'
    HDD: str = 'HDD'
    UNKNOWN: str = 'UNKNOWN'
