from enum import Enum


class DaemonStatus(str, Enum):
    NEW: str = 'NEW'
    ONLINE: str = 'ONLINE'
    OFFLINE: str = 'OFFLINE'
    UNKNOWN: str = 'UNKNOWN'
    ALL: str = 'ALL'
