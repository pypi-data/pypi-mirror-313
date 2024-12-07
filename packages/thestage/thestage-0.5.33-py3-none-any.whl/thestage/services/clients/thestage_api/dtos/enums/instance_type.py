from enum import Enum


class InstanceTypeEnumDto(str, Enum):
    RENTABLE: str = 'RENTABLE'
    SELF_HOSTED: str = 'SELF_HOSTED'
    UNKNOWN: str = 'UNKNOWN'
