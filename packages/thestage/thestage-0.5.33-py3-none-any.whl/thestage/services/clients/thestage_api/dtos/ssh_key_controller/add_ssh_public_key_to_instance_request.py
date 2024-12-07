from pydantic import Field, ConfigDict, BaseModel


class AddSshPublicKeyToInstanceRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    instanceRentedId: int = Field(None, alias='instanceRentedId')
    sshPublicKeyId: int = Field(None, alias='sshPublicKeyId')
