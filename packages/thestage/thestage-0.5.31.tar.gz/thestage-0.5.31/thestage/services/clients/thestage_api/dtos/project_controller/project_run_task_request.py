from typing import Optional

from pydantic import Field, ConfigDict, BaseModel


class ProjectRunTaskRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    projectSlug: str = Field(None, alias='projectSlug')
    instanceRentedSlug: Optional[str] = Field(None, alias='instanceRentedSlug')
    selfhostedInstanceSlug: Optional[str] = Field(None, alias='selfhostedInstanceSlug')
    dockerContainerSlug: Optional[str] = Field(None, alias='dockerContainerSlug')
    commitHash: Optional[str] = Field(None, alias='commitHash')
    runCommand: str = Field(None, alias='runCommand')
    taskTitle: Optional[str] = Field(None, alias='taskTitle')
