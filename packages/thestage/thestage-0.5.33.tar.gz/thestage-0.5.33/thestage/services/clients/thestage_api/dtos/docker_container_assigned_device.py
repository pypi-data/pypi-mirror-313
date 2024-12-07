from typing import Optional, List

from pydantic import Field, BaseModel, ConfigDict


class DockerContainerAssignedDeviceDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    assigned_cpus: List[int] = Field(default_factory=list, alias='assignedCpusIds')
    assigned_gpu_ids: List[int] = Field(default_factory=list, alias='assignedGpuIds')
