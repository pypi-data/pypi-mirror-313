from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class InferenceSimulatorDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: Optional[int] = Field(None, alias="id")
    client_id: Optional[int] = Field(None, alias="clientId")
    title: Optional[str] = Field(None, alias="title")
    slug: Optional[str] = Field(None, alias="slug")
    docker_container_id: Optional[int] = Field(None, alias="dockerContainerId")
    instance_rented_id: Optional[int] = Field(None, alias="instanceRentedId")
    selfhosted_instance_id: Optional[int] = Field(None, alias="selfhostedInstanceId")
    project_id: Optional[int] = Field(None, alias="projectId")
    status: Optional[str] = Field(None, alias="status")
    commit_hash: Optional[str] = Field(None, alias="commitHash")
    http_endpoint: Optional[str] = Field(None, alias="httpEndpoint")
    grpc_endpoint: Optional[str] = Field(None, alias="grpcEndpoint")
    metrics_endpoint: Optional[str] = Field(None, alias="metricsEndpoint")
    inference_metadata: Optional[str] = Field(None, alias="inferenceMetadata")
    qlip_serve_metadata: Optional[str] = Field(None, alias="qlipServeMetadata")
    created_at: Optional[str] = Field(None, alias="createdAt")
    updated_at: Optional[str] = Field(None, alias="updatedAt")