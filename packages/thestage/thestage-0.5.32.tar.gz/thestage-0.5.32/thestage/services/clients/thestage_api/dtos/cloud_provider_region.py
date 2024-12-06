from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from thestage.services.clients.thestage_api.dtos.enums.location_region import LocationRegionEnumDto
from thestage.services.clients.thestage_api.dtos.enums.provider_name import ProviderNameEnumDto


class CloudProviderRegionDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: Optional[int] = Field(None, alias='id')
    region_key: Optional[str] = Field(None, alias='regionKey')
    provider_name: ProviderNameEnumDto = Field(ProviderNameEnumDto.UNKNOWN, alias='providerName')
    location_region: LocationRegionEnumDto = Field(LocationRegionEnumDto.UNKNOWN, alias='locationRegion')
    location_country: Optional[str] = Field(None, alias='locationCountry')
    location_detail: Optional[str] = Field(None, alias='locationDetail')
    is_active_for_storages: Optional[bool] = Field(False, alias='isActiveForStorages')
    is_active_for_instances: Optional[bool] = Field(False, alias='isActiveForInstances')
