from typing import Optional, List

from pydantic import Field, BaseModel, ConfigDict

from thestage.services.clients.thestage_api.dtos.enums.container_pending_action import DockerContainerAction

class DockerContainerActionRequestDto(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    container_id: Optional[int] = Field(None, alias='dockerContainerId')
    action: DockerContainerAction = Field(None, alias='action')
