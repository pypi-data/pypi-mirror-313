import logging

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.auth.oauth2_keycloak import TokenData, get_current_user
from app.model.user_notification_settings import UserNotificationSettings
from app.schema.user_notification_settings_request_model import (
    UserNotificationSettingsRequest,
)
from app.service.alert_service import AlertService

log = logging.getLogger("appLogger")

router = APIRouter()

__service = AlertService()


@router.get(
    "/notification_settings",
    summary="Get notification settings of logged in user",
    response_class=JSONResponse,
    response_model=UserNotificationSettings,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_user_notification_settings(
    oauth_user: TokenData = Depends(get_current_user),
) -> UserNotificationSettings:
    """Get notification settings of logged in user.
    The information of the logged in user is retrieved from the token data.

    If the user notification settings exists, it will be returned.
    Otherwise, it will return an default user notification settings.

    It has the following default values:
    - username: logged in user name
    - priorities: [P1, P2, P3]

    Parameters
    ----------

    Returns
    -------
    UserNotificationSettings
    """
    return __service.get_user_notification_settins(oauth_user.username)


@router.post(
    "/notification_settings",
    summary="Create or update a notification settings of logged in user",
    response_class=JSONResponse,
    response_model=UserNotificationSettings,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def update_user_notification_settings(
    user_notification_setttngs_request: UserNotificationSettingsRequest,
    oauth_user: TokenData = Depends(get_current_user),
) -> UserNotificationSettings:
    """Create or update a user notification settings.

    If the user notification settings already exist, it will be updated.

    Otherwise, it will be created.

    Parameters
    ----------
    user_notification_setttngs_request : UserNotificationSettingsRequest

    Returns
    -------
    UserNotificationSettings
    """
    user_notification_setttngs = UserNotificationSettings(
        username=oauth_user.username, **user_notification_setttngs_request.model_dump()
    )

    return __service.update_user_notification_settings(user_notification_setttngs)
