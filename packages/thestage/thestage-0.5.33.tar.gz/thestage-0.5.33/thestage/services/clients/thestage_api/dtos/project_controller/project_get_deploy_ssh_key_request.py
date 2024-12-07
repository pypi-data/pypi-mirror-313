from pydantic import Field, ConfigDict, BaseModel


class ProjectGetDeploySshKeyRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    projectSlug: str = Field(None, alias='projectSlug')
