import logging
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.auth.oauth2_keycloak import TokenData, get_current_user
from app.model.auth_model import BasicAuthUser
from app.schema.basicauth_request_model import (
    BasicAuthUserCreateRequest,
    BasicAuthUserUpdateRequest,
)
from app.schema.response_model import ResponseModel
from app.service.alert_service import AlertService

log = logging.getLogger("appLogger")

router = APIRouter()

__service = AlertService()


@router.get(
    "/basic_auth_users",
    summary="Get basic auth users",
    response_class=JSONResponse,
    response_model=List[BasicAuthUser],
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_basic_auth_users(
    oauth_user: TokenData = Depends(get_current_user),
) -> List[BasicAuthUser]:
    """

    Parameters
    ----------
    oauth_user : TokenData, optional

    Returns
    -------
    List[BasicAuthUser]
    """
    return __service.get_basic_auth_users()


@router.post(
    "/basic_auth_users",
    summary="Create a basic auth user",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def create_basic_auth_user(
    basic_auth_user_create_request: BasicAuthUserCreateRequest,
    oauth_user: TokenData = Depends(get_current_user),
) -> ResponseModel:
    """A restful API to create a basic_auth_user

    Parameters
    ----------
    basic_auth_user : BasicAuthUser
    oauth_user : TokenData, optional

    Returns
    -------
    ResponseModel
    """
    basic_auth_user = BasicAuthUser(**basic_auth_user_create_request.model_dump())
    basic_auth_user.modifier = oauth_user.username
    return ResponseModel(
        data={"inserted_id": __service.create_basic_auth_user(basic_auth_user)}
    )


@router.get(
    "/basic_auth_users/{username}",
    summary="Get a basic auth user by username",
    response_class=JSONResponse,
    response_model=BasicAuthUser,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_basic_auth_user_by_username(
    username: str, oauth_user: TokenData = Depends(get_current_user)
) -> BasicAuthUser:
    """A restful API to get a basic_auth_user

    Parameters
    ----------
    username : str

    Returns
    -------
    BasicAuthUser
    """
    return __service.get_basic_auth_user_by_username(username)


@router.delete(
    "/basic_auth_users/{id}",
    summary="Remove a basic auth user",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def remove_basic_auth_user(
    id: str, oauth_user: TokenData = Depends(get_current_user)
) -> ResponseModel:
    """A restful API to remove a basic_auth_user

    Parameters
    ----------
    id : str

    Returns
    -------
    ResponseModel
        returns a response model like following
    ```json
    {
        "result": "success"
    }
    ```
    """
    __service.remove_basic_auth_user(id)
    return ResponseModel()


@router.put(
    "/basic_auth_users",
    summary="Modify a basic_auth_user",
    response_class=JSONResponse,
    response_model=BasicAuthUser,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def modify_basic_auth_user(
    basic_auth_user_update_request: BasicAuthUserUpdateRequest,
    oauth_user: TokenData = Depends(get_current_user),
) -> BasicAuthUser:
    """A restful API to modify a basic_auth_user

    Parameters
    ----------
    basic_auth_user : BasicAuthUser

    Returns
    -------
    BasicAuthUser
    """
    basic_auth_user = BasicAuthUser(**basic_auth_user_update_request.model_dump())
    basic_auth_user.modifier = oauth_user.username
    return __service.modify_basic_auth_user(basic_auth_user)
