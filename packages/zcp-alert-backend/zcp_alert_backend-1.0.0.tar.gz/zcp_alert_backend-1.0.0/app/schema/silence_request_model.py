from typing import List

from pydantic import BaseModel, Field


class SilenceCreateRequest(BaseModel):
    name: str = Field(max_length=300)
    integrations: List[str]
    starts_at: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$"
    )
    ends_at: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$"
    )


class SilenceUpdateRequest(SilenceCreateRequest):
    id: str
