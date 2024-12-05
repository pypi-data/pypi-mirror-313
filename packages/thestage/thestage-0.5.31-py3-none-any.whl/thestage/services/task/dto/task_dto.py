from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto
from thestage.services.clients.thestage_api.dtos.frontend_status import FrontendStatusDto
from thestage.services.clients.thestage_api.dtos.instance_rented_response import InstanceRentedDto
from thestage.services.clients.thestage_api.dtos.selfhosted_instance_response import SelfHostedInstanceDto


class TaskDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: Optional[int] = Field(None, alias='id')
    instance_rented_id: Optional[int] = Field(None, alias='instanceRentedId')
    selfhosted_instance_id: Optional[int] = Field(None, alias='selfhostedInstanceId')
    docker_container_id: Optional[int] = Field(None, alias='dockerContainerId')
    description: Optional[str] = Field(None, alias='description')
    title: Optional[str] = Field(None, alias='title')
    source_path: Optional[str] = Field(None, alias='sourcePath')
    source_target_path: Optional[str] = Field(None, alias='sourceTargetPath')
    data_path: Optional[str] = Field(None, alias='dataPath')
    result_destination_path: Optional[str] = Field(None, alias='resultDestinationPath')
    run_command: Optional[str] = Field(None, alias='runCommand')
    commit_hash: Optional[str] = Field(None, alias='commitHash')
    ordinal_number_for_sketch: Optional[int] = Field(None, alias='ordinalNumberForSketch')
    user_id: Optional[int] = Field(None, alias='userId')
    frontend_status: FrontendStatusDto = Field(None, alias='frontendStatus')
    created_at: Optional[str] = Field(None, alias='createdAt')
    updated_at: Optional[str] = Field(None, alias='updatedAt')
    started_at: Optional[str] = Field(None, alias='startedAt')
    finished_at: Optional[str] = Field(None, alias='finishedAt')
    client_id: Optional[int] = Field(None, alias='clientId')

    instance_rented: Optional[InstanceRentedDto] = Field(None, alias='instanceRented')
    selfhosted_instance: Optional[SelfHostedInstanceDto] = Field(None, alias='selfhostedInstance')
    docker_container: Optional[DockerContainerDto] = Field(None, alias='dockerContainer')

    exit_code: Optional[int] = Field(None, alias='exitCode')
    failure_reason: Optional[str] = Field(None, alias='failureReason')
