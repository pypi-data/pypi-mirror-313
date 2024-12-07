from enum import Enum
from typing import Any, Dict, Optional, Type, TypeVar, Union

from pydantic import BaseModel, Field, model_validator
from typing_extensions import deprecated

from app.model.alert_model import AlertBaseModel


class ChannelType(str, Enum):
    """Channel Type model for alert"""

    WEBHOOK = "Webhook"
    SLACK = "Slack"
    MSTEAMS = "MSTeams"
    GOOGLECHAT = "GoogleChat"
    KAKAOTALK = "Kakaotalk"
    EMAIL = "Email"


class AuthenticationType(str, Enum):
    """Authentication type model"""

    NONE = "None"
    BASIC = "Basic"
    BEARER = "Bearer"


class NotificationChannel(BaseModel):
    """Notification Channel Base model
    This is a parent class for all notification channel models
    """


class WebhookChannel(NotificationChannel):
    """Webhook Channel Config model"""

    webhook_url: str = Field(max_length=1000)
    authentication_type: AuthenticationType = Field(default=AuthenticationType.NONE)
    username: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, max_length=100)
    bearer_token: Optional[str] = Field(None)
    tls_verify: bool = Field(default=False)


class SlackChannel(NotificationChannel):
    """Slack Channel Config model"""

    api_url: str = Field(max_length=1000)
    channel_name: str = Field(max_length=100)
    # send_resolved: Optional[bool] = True


class MSTeamsChannel(NotificationChannel):
    """MSTeams Channel Config model"""

    api_url: str = Field(max_length=1000)
    channel_name: str = Field(max_length=100)


class GoogleChatChannel(NotificationChannel):
    """Google Chat Channel Config model"""

    api_url: str = Field(max_length=1000)
    space_name: str = Field(max_length=100)


class KakaoTalkChannel(NotificationChannel):
    """Kakao Channel Config model"""

    # api_url: Optional[HttpUrl] = Field(None, max_length=1000)
    auth_code: str = Field(max_length=500)
    app_name: str = Field(max_length=100)
    client_id: str = Field(max_length=300)
    """ Kakao developer > app key > REST API key """
    client_secret: Optional[str] = Field(None, max_length=300)
    """ Kakao developer > Kakao Login > Security > Client Secret (Optional) """


class EmailChannel(NotificationChannel):
    """Email Channel Config model"""

    smtp_server: str = Field(max_length=300)
    smtp_port: int = Field(ge=1, le=65535, default=587)
    smtp_user: str = Field(max_length=100)
    smtp_password: str = Field(max_length=100)
    smtp_tls: bool = Field(default=True)
    smtp_ssl: bool = Field(default=False)
    from_email: str = Field(max_length=100)
    from_display_name: Optional[str] = Field(None, max_length=100)
    to_emails: list[str] = Field()

    @model_validator(mode="before")
    @classmethod
    def check_encryption_type(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        smtp_tls = bool(values.get("smtp_tls"))
        smtp_ssl = bool(values.get("smtp_ssl"))

        if smtp_tls and smtp_ssl:
            raise ValueError("Both TLS and SSL cannot be enabled at the same time")

        return values


class ChannelSortField(str, Enum):
    NAME = "name"
    TYPE = "type"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


T = TypeVar("T", bound="NotificationChannel")


class Channel(AlertBaseModel):
    """Alert Channel model"""

    name: str
    type: ChannelType
    type_properties: Optional[
        Union[
            Dict[str, str],  # should be set to it in first type, because of the query
            WebhookChannel,
            SlackChannel,
            MSTeamsChannel,
            GoogleChatChannel,
            KakaoTalkChannel,
            EmailChannel,
        ]
    ]
    modifier: Optional[str] = None

    @deprecated(
        "Do not use this method because the type_properties is instanciated in the root_validator"
    )
    def get_notification_channel(self, channel_type: Type[T]) -> T:
        if isinstance(self.type_properties, dict):
            return channel_type(**self.type_properties)
        else:
            return self.type_properties

    @model_validator(mode="before")
    @classmethod
    def assign_type_properties(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        channel_type = values.get("type")
        type_properties = values.get("type_properties")

        if isinstance(type_properties, dict):
            if channel_type == ChannelType.WEBHOOK:
                values["type_properties"] = WebhookChannel(**type_properties)
            elif channel_type == ChannelType.SLACK:
                values["type_properties"] = SlackChannel(**type_properties)
            elif channel_type == ChannelType.MSTEAMS:
                values["type_properties"] = MSTeamsChannel(**type_properties)
            elif channel_type == ChannelType.GOOGLECHAT:
                values["type_properties"] = GoogleChatChannel(**type_properties)
            elif channel_type == ChannelType.KAKAOTALK:
                values["type_properties"] = KakaoTalkChannel(**type_properties)
            elif channel_type == ChannelType.EMAIL:
                values["type_properties"] = EmailChannel(**type_properties)

        return values
