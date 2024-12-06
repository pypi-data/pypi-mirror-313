from typing import Optional, List

from pydantic import Field, BaseModel, ConfigDict

from thestage.services.clients.thestage_api.dtos.base_response import TheStageBaseResponse
from thestage.services.clients.thestage_api.dtos.selfhosted_instance_response import SelfHostedInstanceDto
from thestage.services.clients.thestage_api.dtos.instance_rented_response import InstanceRentedDto


class ProjectDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: Optional[int] = Field(None, alias='id')
    client_id: Optional[int] = Field(None, alias='сlientId')
    ssh_key_deploy_id: Optional[int] = Field(None, alias='sshKeyDeployId')
    name: Optional[str] = Field(None, alias='name')
    slug: Optional[str] = Field(None, alias='slug')
    description: Optional[str] = Field(None, alias='description')
    github_username: Optional[str] = Field(None, alias='githubCollaboratorUsername')
    last_commit_hash: Optional[str] = Field(None, alias='lastCommitHash')
    last_commit_description: Optional[str] = Field(None, alias='lastCommitDescription')
    git_repository_url: Optional[str] = Field(None, alias='gitRepositoryUrl')
    git_repository_name: Optional[str] = Field(None, alias='gitRepositoryName')
    task_count: Optional[int] = Field(None, alias='taskCount')
    favourite_task_count: Optional[int] = Field(None, alias='favouriteTaskCount')
    last_task_run_date: Optional[str] = Field(None, alias='lastTaskRunDate')
    created_at: Optional[str] = Field(None, alias='createdAt')
    updated_at: Optional[str] = Field(None, alias='updatedAt')
    instance_rented_list: List[InstanceRentedDto] = Field(default_factory=list, alias='instanceRentedList')
    selfhosted_instance_list: List[SelfHostedInstanceDto] = Field(default_factory=list, alias='selfhostedInstanceList')


class ProjectViewResponse(TheStageBaseResponse):
    project: Optional[ProjectDto] = Field(None, alias='project')
