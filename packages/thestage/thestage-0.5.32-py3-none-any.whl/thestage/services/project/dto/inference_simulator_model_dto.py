from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class InferenceSimulatorModelDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: Optional[int] = Field(None, alias='id')
    client_id: Optional[int] = Field(None, alias='clientId')
    instance_rented_id: Optional[int] = Field(None, alias='instanceRentedId')
    selfhosted_instance_id: Optional[int] = Field(None, alias='selfhostedInstanceId')
    project_id: Optional[int] = Field(None, alias='projectId')
    status: Optional[str] = Field(None, alias='status')
    commit_hash: Optional[str] = Field(None, alias='commitHash')
    cpu_architecture: Optional[str] = Field(None, alias='cpuArchitecture')
    gpu_model: Optional[str] = Field(None, alias='gpuModel')
    ecr_image_url: Optional[str] = Field(None, alias='ecrImageUrl')
    s3_artifacts_url: Optional[str] = Field(None, alias='s3ArtifactsUrl')
    created_at: Optional[str] = Field(None, alias='createdAt')
    updated_at: Optional[str] = Field(None, alias='updatedAt')