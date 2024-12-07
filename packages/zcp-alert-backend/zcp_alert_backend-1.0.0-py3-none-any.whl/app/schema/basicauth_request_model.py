from typing import Optional

from pydantic import BaseModel, Field


class BasicAuthUserCreateRequest(BaseModel):
    username: Optional[str] = Field(max_length=100, min_length=3)
    password: Optional[str] = Field(max_length=100, min_length=8)


class BasicAuthUserUpdateRequest(BasicAuthUserCreateRequest):
    id: str
