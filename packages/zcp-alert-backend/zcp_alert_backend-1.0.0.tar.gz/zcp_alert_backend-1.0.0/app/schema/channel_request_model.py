from typing import Any, Dict, Union

from pydantic import BaseModel, Field, model_validator

from app.model.channel_model import (
    ChannelType,
    EmailChannel,
    GoogleChatChannel,
    KakaoTalkChannel,
    MSTeamsChannel,
    SlackChannel,
    WebhookChannel,
)


class ChannelCreateRequest(BaseModel):
    """Channel request model for the restful api"""

    name: str = Field(max_length=300, min_length=3)
    type: ChannelType
    type_properties: Union[
        Dict[str, str],
        WebhookChannel,
        SlackChannel,
        MSTeamsChannel,
        GoogleChatChannel,
        KakaoTalkChannel,
        EmailChannel,
    ]

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


class ChannelUpdateRequest(ChannelCreateRequest):
    id: str
