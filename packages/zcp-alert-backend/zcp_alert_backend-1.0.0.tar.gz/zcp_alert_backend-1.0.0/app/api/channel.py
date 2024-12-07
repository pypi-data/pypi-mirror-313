import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from app.auth.oauth2_keycloak import TokenData, get_current_user
from app.exception.common_exception import AlertBackendException, AlertError
from app.model.channel_model import Channel, ChannelSortField, ChannelType
from app.model.kakaotalk_model import KakaoTalkFriend
from app.model.result_model import Result
from app.schema.channel_request_model import ChannelCreateRequest, ChannelUpdateRequest
from app.schema.list_model import ChannelList
from app.schema.response_model import ResponseModel
from app.service.alert_service import AlertService
from app.settings import (
    ALERT_CONSOLE_ENDPOINT,
    KAKAO_AUTH_ENDPOINT,
    KAKAO_AUTH_REDIRECT_URI,
)
from app.utils.list_utils import (
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    SortDirection,
)

log = logging.getLogger("appLogger")

router = APIRouter()

__service = AlertService()


@router.get(
    "/channels",
    summary="Get channels",
    response_class=JSONResponse,
    response_model=ChannelList,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_channels(
    name: Optional[str] = Query(
        None,
        max_length=100,
        title="channel name",
        description="Search query string for name. The max length is 100",
    ),
    types: list[ChannelType] = Query(
        None, title="channel type", description="Search query string for type"
    ),
    sort_field: ChannelSortField = Query(
        ChannelSortField.NAME, title="sort field", description="Sort field name"
    ),
    sort_direction: SortDirection = Query(
        SortDirection.ASC, title="sort direction", description="Sort direction"
    ),
    page_number: Optional[int] = Query(
        DEFAULT_PAGE_NUMBER,
        ge=DEFAULT_PAGE_NUMBER,
        title="page number",
        description=f"Page number. Default is {DEFAULT_PAGE_NUMBER} and it should be greater than 0",
    ),
    page_size: Optional[int] = Query(
        DEFAULT_PAGE_SIZE,
        ge=DEFAULT_PAGE_SIZE,
        le=MAX_PAGE_SIZE,
        title="page size",
        description=f"Page size. Default is {DEFAULT_PAGE_SIZE} and it should be greater than 10 and less than {MAX_PAGE_SIZE}",
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> ChannelList:
    """A restful API to get channels

    Returns
    -------
    ChannelList
    """
    return ChannelList(
        current_page=page_number,
        page_size=page_size,
        total=__service.get_channels_count(name=name, types=types),
        data=__service.get_channels(
            name=name,
            types=types,
            sort_field=sort_field,
            sort_direction=sort_direction,
            page_number=page_number,
            page_size=page_size,
        ),
    )


@router.get(
    "/channels/all/combo",
    summary="Get channels for combo box",
    response_class=JSONResponse,
    response_model=list[dict],
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_all_channels(
    oauth_user: TokenData = Depends(get_current_user),
) -> list[dict]:
    """A restful API to get all channels

    Returns
    -------
    ChannelList
    """

    return __service.get_all_channels()


@router.post(
    "/channels",
    summary="Create a channel",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def create_channel(
    channel_create_request: ChannelCreateRequest,
    oauth_user: TokenData = Depends(get_current_user),
) -> ResponseModel:
    """A restful API to create a channel

    Parameters
    ----------
    channel_create_request : ChannelCreateRequest

    Returns
    -------
    ResponseModel
        Returns a response model like following
    ```json
    {
        "result": "success",
        "data": {
            "inserted_id": "5f0b5b8b-2f7e-4e4b-9c9d-5a4f9b8e2c3d"
        }
    }
    ```
    """
    if not channel_create_request.type_properties:
        raise AlertBackendException(
            AlertError.BAD_REQUEST, details="type_properties should not be empty"
        )

    channel = Channel(**channel_create_request.model_dump())
    channel.modifier = oauth_user.username
    return ResponseModel(data={"inserted_id": __service.create_channel(channel)})


@router.post(
    "/channels/send_test_message",
    summary="Send a test message to the channel",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def send_test_message(
    channel_create_request: ChannelCreateRequest,
    oauth_user: TokenData = Depends(get_current_user),
) -> ResponseModel:
    """A restful API to create a channel

    Parameters
    ----------
    channel_create_request : ChannelCreateRequest

    Returns
    -------
    ResponseModel
        Returns a response model like following
    ```json
    {
        "result": "success"
    }
    ```
    """
    if not channel_create_request.type_properties:
        raise AlertBackendException(
            AlertError.BAD_REQUEST, details="type_properties should not be empty"
        )

    channel = Channel(**channel_create_request.model_dump())
    channel.modifier = oauth_user.username

    return ResponseModel(
        result=Result.SUCCESS
        if __service.send_test_notification(channel)
        else Result.FAILED
    )


@router.get(
    "/channels/{channel_id}",
    summary="Get a channel",
    response_class=JSONResponse,
    response_model=Channel,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_channel(
    channel_id: str, oauth_user: TokenData = Depends(get_current_user)
) -> Channel:
    """A restful API to get a channel

    Parameters
    ----------
    channel_id : str

    Returns
    -------
    Channel
    """
    return __service.get_channel(channel_id)


@router.delete(
    "/channels/{channel_id}",
    summary="Remove a channel",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def remove_channel(
    channel_id: str, oauth_user: TokenData = Depends(get_current_user)
) -> ResponseModel:
    """A restful API to remove a channel

    Parameters
    ----------
    channel_id : str

    Returns
    -------
    ResponseModel
        Returns a response model like following
    ```json
    {
        "result": "success"
    }
    ```
    """
    __service.remove_channel(channel_id)

    return ResponseModel()


@router.put(
    "/channels",
    summary="Modify a channel",
    response_class=JSONResponse,
    response_model=Channel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def modify_channel(
    channel_update_request: ChannelUpdateRequest,
    oauth_user: TokenData = Depends(get_current_user),
) -> Channel:
    """A restful API to modify a channel

    Parameters
    ----------
    channel_update_request : ChannelUpdateRequest

    Returns
    -------
    Channel
    """
    if not channel_update_request.type_properties:
        raise AlertBackendException(
            AlertError.BAD_REQUEST, details="type_properties should not be empty"
        )

    channel = Channel(**channel_update_request.model_dump())
    channel.modifier = oauth_user.username
    return __service.modify_channel(channel)


@router.get(
    "/channels/external/kakao/oauth/callback",
    summary="The redirect URI after the Kakao OAuth login",
)
async def kakao_oauth_callback(
    request: Request,
    code: str = Query(title="code", description="The code from the Kakao OAuth login"),
) -> HTMLResponse:
    """
    The redirect URI after the Kakao OAuth login

    Parameters
    ----------
    request : Request
        The request object

    code : str
        The code from the Kakao OAuth login

    Returns
    -------
    HTMLResponse
    """

    log.debug(f"code: {code}")

    return HTMLResponse(
        content=f"""
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    text-align: center;
                    margin: 0;
                    background-color: #f5f5f5;
                }}

                p {{
                    margin: 20px 0;
                }}

                button {{
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    border-radius: 5px;
                }}

                button:hover {{
                    background-color: #0056b3;
                }}

                .container {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
            </style>
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    var container = document.createElement('div');
                    container.className = 'container';

                    /* because of the CORS policy, the following code is not working
                    if (window.opener) {{
                        window.opener.document.getElementById('auth_code').value='{code}';
                    }}
                    */

                    var p = document.createElement('p');
                    p.innerHTML='Logged in successfully.<br><br>Please copy and paste this Auth Code <br><br> <b>{code}</b>';
                    p.style.align = 'center';
                    container.appendChild(p);

                    var closeButton = document.createElement('button');
                    closeButton.textContent = 'Close';
                    closeButton.style.align = 'center';
                    closeButton.addEventListener('click', function() {{
                        window.close();
                    }});
                    container.appendChild(closeButton);

                    document.body.appendChild(container);
                }});
            </script>
        """
    )


@router.get(
    "/channels/kakao/oauth/login",
    summary="Redirect to the Kakao OAuth login page",
    response_class=RedirectResponse,
)
async def kakao_oauth_login(
    client_id: str = Query(
        max_length=300,
        title="client_id is the REST API KEY of Kakao Developer App",
        description="Search query string for client_id. The max length is 300",
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> RedirectResponse:
    """Redirect to the Kakao OAuth login page

    Parameters
    ----------
    client_id : str, optional
        by default Query( max_length=300,
        title="client_id is the REST API KEY of Kakao Developer App",
        description="Search query string for client_id. The max length is 300" )

    Returns
    -------
    RedirectResponse
    """
    return RedirectResponse(
        url=f"{KAKAO_AUTH_ENDPOINT}/oauth/authorize?"
        f"client_id={client_id}"
        f"&redirect_uri={KAKAO_AUTH_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20friends%20profile_nickname%20profile_image%20talk_message%20account_email"
    )


@router.get(
    "/channels/kakao/friends",
    summary="Get Kakao friends of the code owner",
    response_class=JSONResponse,
    response_model=List[KakaoTalkFriend],
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_kakao_friends(
    channel_id: str = Query(
        None, title="channel_id", description="Search query string for channel_id"
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> List[KakaoTalkFriend]:
    """Get Kakao friends of the code owner

    Parameters
    ----------
    kakao_friends_request : KakaoFriendsRequest

    Returns
    -------
    List[KakaoFriend]
    """
    return __service.get_kakao_friends(channel_id=channel_id)


@router.get(
    "/channel/supported",
    summary="Get channel types",
    response_class=JSONResponse,
    response_model=List[ChannelType],
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def get_supported_channel_types() -> List[ChannelType]:
    """A restful API to get channel types"""
    return __service.get_channel_types()


@router.get(
    "/channel/kakao/urls",
    summary="Get related domains for Kakao",
    response_class=JSONResponse,
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def get_related_domains_for_kakao() -> dict:
    """A restful API to get related domains for Kakao"""
    return {
        "console_domain": ALERT_CONSOLE_ENDPOINT,
        "redirect_url": KAKAO_AUTH_REDIRECT_URI,
    }
