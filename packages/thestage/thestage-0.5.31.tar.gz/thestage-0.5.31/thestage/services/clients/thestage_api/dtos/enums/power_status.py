from enum import Enum


class PowerStatusEnumDto(str, Enum):
    ON: str = 'ON'
    OFF: str = 'OFF'
    POWERING_ON: str = 'POWERING_ON'
    POWERING_OFF: str = 'POWERING_OFF'
    REBOOTING: str = 'REBOOTING'
    UNKNOWN: str = 'UNKNOWN'
