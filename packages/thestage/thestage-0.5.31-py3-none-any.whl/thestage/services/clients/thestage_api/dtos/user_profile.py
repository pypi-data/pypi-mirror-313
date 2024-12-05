from typing import Optional

from pydantic import BaseModel, Field


class UserProfileResponse(BaseModel):
    name: Optional[str] = Field(None, alias='name')
    email: Optional[str] = Field(None, alias='email')
    metamask_wallet: Optional[str] = Field(None, alias='metamaskWallet')
