from datetime import datetime
from typing import Optional, List, Dict

from pydantic import Field, BaseModel, ConfigDict

from thestage.services.clients.thestage_api.dtos.enums.daemon_status import DaemonStatus
from thestage.services.clients.thestage_api.dtos.frontend_status import FrontendStatusDto
from thestage.services.clients.thestage_api.dtos.instance_detected_gpus import InstanceDetectedGpusDto
from thestage.services.clients.thestage_api.dtos.enums.instance_type import InstanceTypeEnumDto
from thestage.services.clients.thestage_api.dtos.base_response import TheStageBasePaginatedResponse
from thestage.services.clients.thestage_api.dtos.paginated_entity_list import PaginatedEntityList
from thestage.services.clients.thestage_api.dtos.cloud_provider_region import CloudProviderRegionDto
from thestage.services.clients.thestage_api.dtos.enums.disk_type import DiskTypeEnumDto
from thestage.services.clients.thestage_api.dtos.enums.gpu_name import InstanceGpuType
from thestage.services.clients.thestage_api.dtos.enums.power_status import PowerStatusEnumDto
from thestage.services.clients.thestage_api.dtos.enums.instance_rented_status import InstanceRentedBusinessStatus
from thestage.services.clients.thestage_api.dtos.price_definition import PriceDefinitionDto
from thestage.services.clients.thestage_api.dtos.enums.cpu_type import InstanceCpuType


class InstanceRentedDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: Optional[int] = Field(None, alias='id')
    display_price_per_hour: Optional[PriceDefinitionDto] = Field(None, alias='displayPricePerHour')
    total_money_spent: Optional[List[PriceDefinitionDto]] = Field(default_factory=list, alias='totalMoneySpent')
    client_id: Optional[int] = Field(None, alias='clientId')
    instance_type: Optional[InstanceTypeEnumDto] = Field(InstanceTypeEnumDto.UNKNOWN, alias='instanceType', validate_default=True)
    provider_id: Optional[str] = Field(None, alias='providerId')
    cloud_provider_region_id: Optional[int] = Field(None, alias='cloudProviderRegionId')
    cloud_provider_region: Optional[CloudProviderRegionDto] = Field(None, alias='cloudProviderRegion')
    cpu_type: Optional[InstanceCpuType] = Field(InstanceCpuType.UNKNOWN, alias='cpuType')
    cpu_name: Optional[str] = Field(None, alias='cpuName')
    cpu_cores: Optional[int] = Field(None, alias='cpuCores')
    gpu_type: Optional[InstanceGpuType] = Field(Optional[InstanceGpuType.UNKNOWN], alias='gpuType')
    gpu_name: Optional[str] = Field(None, alias='gpuName')
    gpu_memory_gb: Optional[int] = Field(None, alias='gpuMemoryGb')
    gpu_count: Optional[int] = Field(None, alias='gpuCount')
    disk_type: Optional[DiskTypeEnumDto] = Field(DiskTypeEnumDto.UNKNOWN, alias='diskType')
    disk_size_gb: Optional[int] = Field(None, alias='diskSizeGb')
    ram_size_gb: Optional[int] = Field(None, alias='ramSizeGb')
    average_renting_time_minutes: Optional[int] = Field(None, alias='averageRentingTimeMinutes')

    business_status: InstanceRentedBusinessStatus = Field(InstanceRentedBusinessStatus.UNKNOWN, alias='businessStatus')
    frontend_status: Optional[FrontendStatusDto] = Field(None, alias='frontendStatus')

    slug: Optional[str] = Field(None, alias='slug')
    title: Optional[str] = Field(None, alias='title')
    power_status: PowerStatusEnumDto = Field(PowerStatusEnumDto.UNKNOWN, alias='powerStatus')
    created_at: Optional[datetime] = Field(None, alias='createdAt')
    updated_at: Optional[datetime] = Field(None, alias='updatedAt')
    ip_address: Optional[str] = Field(None, alias='ipAddress')
    host_username: Optional[str] = Field(None, alias='hostUsername')
    detected_gpus: Optional[InstanceDetectedGpusDto] = Field(None, alias='detectedGpus')
    daemon_status: Optional[DaemonStatus] = Field(DaemonStatus.UNKNOWN, alias='daemonStatus')


class InstanceRentedListResponse(TheStageBasePaginatedResponse):
    paginated_list: Optional[PaginatedEntityList[InstanceRentedDto]] = Field(None, alias='paginatedEntityList')


class InstanceRentedItemResponse(TheStageBasePaginatedResponse):
    model_config = ConfigDict(use_enum_values=True)

    instance_rented: Optional[InstanceRentedDto] = Field(None, alias='instanceRented')


class InstanceRentedBusinessStatusMapperResponse(TheStageBasePaginatedResponse):
    model_config = ConfigDict(use_enum_values=True)

    instance_rented_business_status_map: Dict[str, str] = Field(default=dict, alias='instanceRentedBusinessStatusMap')
