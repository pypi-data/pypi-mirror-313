from typing import List

from pydantic import BaseModel, ConfigDict, Field

from app.model.alert_model import AlertActivity, ZcpAlert
from app.model.channel_model import Channel
from app.model.integration_model import Integration
from app.model.silence_model import Silence
from app.utils.list_utils import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


class BaseListModel(BaseModel):
    """Base list model for alert"""

    current_page: int = Field(DEFAULT_PAGE_NUMBER, ge=DEFAULT_PAGE_NUMBER)
    page_size: int = Field(DEFAULT_PAGE_SIZE, ge=DEFAULT_PAGE_SIZE, le=MAX_PAGE_SIZE)
    total: int = Field(0, ge=0)

    model_config = ConfigDict(exclude_none=True)


class ZcpAlertList(BaseListModel):
    """Zcp alert list model for alert"""

    data: List[ZcpAlert]


class ActivityList(BaseListModel):
    """Activity list model for alert"""

    data: List[AlertActivity]


class ChannelList(BaseListModel):
    """Channel list model for alert"""

    data: List[Channel]


class IntegrationList(BaseListModel):
    """Integration list model for alert"""

    data: List[Integration]


class SilenceList(BaseListModel):
    """Silence list model for alert"""

    data: List[Silence]
