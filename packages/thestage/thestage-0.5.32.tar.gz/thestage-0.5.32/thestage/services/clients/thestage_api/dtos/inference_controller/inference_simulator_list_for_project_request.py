from typing import Optional, List

from pydantic import Field, ConfigDict, BaseModel

from thestage.services.clients.thestage_api.dtos.entity_filter_request import EntityFilterRequest


class InferenceSimulatorListForProjectRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    entityFilterRequest: EntityFilterRequest = Field(None, alias='entityFilterRequest')
    projectSlug: str = Field(None, alias='projectSlug')
    statuses: Optional[List[str]] = Field(None, alias='statuses')

