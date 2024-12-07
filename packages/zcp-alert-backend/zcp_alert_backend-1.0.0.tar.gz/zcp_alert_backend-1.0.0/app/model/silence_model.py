from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import ConfigDict, computed_field, field_serializer

from app.model.alert_model import AlertBaseModel
from app.model.integration_model import Integration
from app.utils.time_utils import DEFAULT_TIME_ZONE


class SilenceStatus(str, Enum):
    """Silence status model"""

    PLANNED = "planed"
    EXPIRED = "expired"
    ACTIVE = "active"
    # INVALID = 'invalid'


class SilenceSortField(str, Enum):
    NAME = "name"
    STATUS = "status"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class Silence(AlertBaseModel):
    name: str = None
    integrations: Union[Optional[List[str]], Optional[List[Integration]]] = None
    """ Integration ID list
    Case 1) When the silence is created, the integrations are set as the list of string
    Case 2) When the silence is retrieved, the integrations are set as the list of Integration
    """
    starts_at: datetime
    ends_at: datetime
    modifier: Optional[str] = None
    # _progress_status: Optional[SilenceStatus] = None

    model_config = ConfigDict(
        extra="allow",
    )

    @field_serializer("starts_at", "ends_at")
    def _serialize_starts_ends_at(self, dt: Optional[datetime]) -> Optional[str]:
        return dt.isoformat(timespec="milliseconds") if dt else None

    @computed_field
    @property
    def progress_status(self) -> str:
        now = datetime.now(DEFAULT_TIME_ZONE)
        status = None
        if self.starts_at <= now and self.ends_at >= now:
            status = SilenceStatus.ACTIVE
        elif self.starts_at > now:
            status = SilenceStatus.PLANNED
        elif self.ends_at < now:
            status = SilenceStatus.EXPIRED
        # else:
        #     status = SilenceStatus.INVALID
        return status
