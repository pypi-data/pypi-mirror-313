from typing import Optional, List

from pydantic import Field, ConfigDict, BaseModel

from thestage.services.clients.thestage_api.dtos.entity_filter_request import EntityFilterRequest


class GetInferenceSimulatorRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    slug: Optional[str] = Field(None, alias='slug')