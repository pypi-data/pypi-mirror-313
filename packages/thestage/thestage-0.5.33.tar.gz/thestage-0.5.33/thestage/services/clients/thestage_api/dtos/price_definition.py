from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from thestage.services.clients.thestage_api.dtos.enums.currency_type import CurrencyTypeEnumDto


class PriceDefinitionDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    currency: CurrencyTypeEnumDto = Field(CurrencyTypeEnumDto.UNKNOWN, alias='currency')
    cents_amount_in_unit: Optional[int] = Field(None, alias='centsAmountInUnit')
    cents_value: Optional[str] = Field(None, alias='centsValue')
    decimal_value: Optional[str] = Field(None, alias='decimalValue')
