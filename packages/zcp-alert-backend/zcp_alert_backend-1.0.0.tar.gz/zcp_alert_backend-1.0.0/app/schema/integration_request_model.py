from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_validator

from app.model.alert_model import Action
from app.model.integration_model import Filter, FilterMode, IntegrationStatus


class IntegrationCreateRequest(BaseModel):
    name: str = Field(max_length=300, min_length=3)
    channel: str = Field(max_length=100)
    # message_template: Optional[str] = Field(None, max_length=30000, description="Not supported yet")
    alert_actions: List[Action]
    filter_mode: FilterMode = FilterMode.ALL
    alert_filters: Optional[List[Filter]] = None
    status: Optional[IntegrationStatus] = IntegrationStatus.OFF

    @model_validator(mode="before")
    @classmethod
    def assign_type_properties(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        filter_mode = values.get("filter_mode")
        alert_filters = values.get("alert_filters")

        if filter_mode in [FilterMode.MATCH_ANY, FilterMode.MATCH_ALL]:
            if (
                alert_filters is None
                or not isinstance(alert_filters, list)
                or len(alert_filters) == 0
            ):
                raise ValueError(
                    f"alert_filters is required more than at least 1 when filter_mode is {filter_mode}"
                )

        return values


class IntegrationUpdateRequest(IntegrationCreateRequest):
    id: str
