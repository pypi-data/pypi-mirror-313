from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SelfHostedInstanceEntity(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
    )

    status: Optional[str] = Field(None, alias='STATUS')
    title: Optional[str] = Field(None, alias='TITLE')
    slug: Optional[str] = Field(None, alias='SLUG')
    cpu_type: Optional[str] = Field(str, alias='CPU_TYPE')
    cpu_cores: Optional[int] = Field(None, alias='CPU_CORES')
    gpu_type: Optional[str] = Field(str, alias='GPU_TYPE')
    ip_address: Optional[str] = Field(None, alias='IP_ADDRESS')
    # created_at: Optional[str] = Field(None, alias='CREATED_AT')
    # updated_at: Optional[str] = Field(None, alias='UPDATED_AT')
