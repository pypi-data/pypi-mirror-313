from typing import Optional

from pydantic import Field, ConfigDict, BaseModel


class UserLogsQueryRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    containerRunId: Optional[int] = Field(None, alias='containerRunId')
    containerId: Optional[int] = Field(None, alias='containerId')
    message: Optional[str] = Field(None, alias='message')
    instanceId: Optional[int] = Field(None, alias='instanceId')
    instanceType: Optional[str] = Field(None, alias='instanceType') # ENUM
    taskId: Optional[int] = Field(None, alias='taskId')
    fromTimestamp: Optional[str] = Field(None, alias='fromTimestamp')
    toTimestamp: Optional[str] = Field(None, alias='toTimestamp')
    logType: Optional[str] = Field(None, alias='logType') # ENUM
    offset: Optional[int] = Field(None, alias='offset')
    limit: Optional[int] = Field(None, alias='limit')
    ascendingOrder: Optional[bool] = Field(None, alias='ascendingOrder')
