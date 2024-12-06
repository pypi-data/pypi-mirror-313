from typing import Optional

from pydantic import Field, ConfigDict, BaseModel


class ProjectPushInferenceSimulatorModelRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    slug: Optional[str] = Field(None, alias='slug')