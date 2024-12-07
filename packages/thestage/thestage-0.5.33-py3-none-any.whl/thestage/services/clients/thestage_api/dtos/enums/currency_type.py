from enum import Enum


class CurrencyTypeEnumDto(str, Enum):
    ETH: str = 'ETH'
    STAGI: str = 'STAGI'
    USD: str = 'USD'
    EUR: str = 'EUR'
    USDT: str = 'USDT'
    UNKNOWN: str = 'UNKNOWN'
