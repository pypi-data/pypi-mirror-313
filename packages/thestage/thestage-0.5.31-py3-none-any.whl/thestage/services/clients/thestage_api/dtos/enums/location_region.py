from enum import Enum


class LocationRegionEnumDto(str, Enum):
    NORTH_AMERICA: str = 'NORTH_AMERICA'
    EUROPE: str = 'EUROPE'
    ASIA: str = 'ASIA'
    AFRICA: str = 'AFRICA'
    OCEANIA: str = 'OCEANIA'
    SOUTH_AMERICA: str = 'SOUTH_AMERICA'
    UNKNOWN: str = 'UNKNOWN'
