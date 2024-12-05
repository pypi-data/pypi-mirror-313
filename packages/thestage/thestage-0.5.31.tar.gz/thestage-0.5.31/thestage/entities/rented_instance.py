from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class RentedInstanceEntity(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True
    )

    # id: Optional[int] = Field(None, alias='ID')
    status: Optional[str] = Field(None, alias='STATUS')
    title: Optional[str] = Field(None, alias='TITLE')
    slug: Optional[str] = Field(None, alias='UNIQUE ID')
    cpu_type: Optional[str] = Field(None, alias='CPU TYPE')
    cpu_cores: Optional[str] = Field(None, alias='CPU CORES')
    gpu_type: Optional[str] = Field(None, alias='GPU TYPE')
    # ram_size_gb: Optional[int] = Field(None, alias='RAM SIZE GB')
    ip_address: Optional[str] = Field(None, alias='IP ADDRESS')
    # username: Optional[str] = Field(None, alias='USERNAME')
    # created_at: Optional[str] = Field(None, alias='CREATED AT')
    # updated_at: Optional[str] = Field(None, alias='UPDATED AT')
