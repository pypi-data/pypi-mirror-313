import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from app.auth.oauth2_keycloak import TokenData, get_current_user
from app.model.silence_model import Silence, SilenceSortField, SilenceStatus
from app.schema.list_model import SilenceList
from app.schema.response_model import ResponseModel
from app.schema.silence_request_model import SilenceCreateRequest, SilenceUpdateRequest
from app.service.alert_service import AlertService
from app.utils.list_utils import (
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    SortDirection,
)
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")

router = APIRouter()

__service = AlertService()


@router.get(
    "/silences",
    summary="Get silences",
    response_class=JSONResponse,
    response_model=SilenceList,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_silences(
    name: Optional[str] = Query(
        None,
        max_length=100,
        title="silence name",
        description="Search query string for name. The max length is 100",
    ),
    statuses: list[SilenceStatus] = Query(
        None, title="silence type", description="Search query string for status"
    ),
    integration_id: Optional[str] = Query(
        None,
        max_length=100,
        title="integration id",
        description="Search query string for integration id. The max length is 100",
    ),
    sort_field: SilenceSortField = Query(
        SilenceSortField.NAME, title="sort field", description="Sort field name"
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
) -> SilenceList:
    """A restful API to get silences

    Returns
    -------
    SilenceList
        Returns a silence list which filtered by the parameters
    """
    return SilenceList(
        current_page=page_number,
        page_size=page_size,
        total=__service.get_silences_count(
            name=name, statuses=statuses, integration_id=integration_id
        ),
        data=__service.get_silences(
            name=name,
            statuses=statuses,
            integration_id=integration_id,
            sort_field=sort_field,
            sort_direction=sort_direction,
            page_number=page_number,
            page_size=page_size,
        ),
    )


@router.post(
    "/silences",
    summary="Create a silence",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def create_silence(
    silence_create_request: SilenceCreateRequest,
    oauth_user: TokenData = Depends(get_current_user),
) -> ResponseModel:
    """A restful API to create a silence

    Parameters
    ----------
    silence : Silence

    Returns
    -------
    ResponseModel
        returns a response model like following
    ```json
    {
        "result": "success",
        "data": {
            "inserted_id": "5f0a0e5e6d1e6f0001e4b4f3"
        }
    }
    ```
    """
    silence = Silence(**silence_create_request.model_dump())
    silence.modifier = oauth_user.username
    silence.starts_at = (
        datetime.fromisoformat(silence_create_request.starts_at).astimezone(
            DEFAULT_TIME_ZONE
        )  # .isoformat()
        if silence_create_request.starts_at
        else silence_create_request.starts_at
    )
    silence.ends_at = (
        datetime.fromisoformat(silence_create_request.ends_at).astimezone(
            DEFAULT_TIME_ZONE
        )  # .isoformat()
        if silence_create_request.ends_at
        else silence_create_request.ends_at
    )

    return ResponseModel(data={"inserted_id": __service.create_silence(silence)})


@router.get(
    "/silences/{silence_id}",
    summary="Get a silence",
    response_class=JSONResponse,
    response_model=Silence,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_silence(
    silence_id: str, oauth_user: TokenData = Depends(get_current_user)
) -> Silence:
    """A restful API to get a silence

    Parameters
    ----------
    silence_id : str

    Returns
    -------
    Silence
    """
    return __service.get_silence(silence_id)


@router.delete(
    "/silences/{silence_id}",
    summary="Remove a silence",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def remove_silence(
    silence_id: str, oauth_user: TokenData = Depends(get_current_user)
) -> ResponseModel:
    """A restful API to remove a silence

    Parameters
    ----------
    silence_id : str

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
    __service.remove_silence(silence_id)
    return ResponseModel()


@router.put(
    "/silences",
    summary="Modify a silence",
    response_class=JSONResponse,
    response_model=Silence,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def modify_silence(
    silence_update_request: SilenceUpdateRequest,
    oauth_user: TokenData = Depends(get_current_user),
) -> Silence:
    """A restful API to modify a silence

    Parameters
    ----------
    silence : Silence

    Returns
    -------
    Silence
    """
    silence = Silence(**silence_update_request.model_dump())
    silence.modifier = oauth_user.username
    silence.starts_at = (
        datetime.fromisoformat(silence_update_request.starts_at).astimezone(
            DEFAULT_TIME_ZONE
        )  # .isoformat()
        if silence_update_request.starts_at
        else silence_update_request.starts_at
    )
    silence.ends_at = (
        datetime.fromisoformat(silence_update_request.ends_at).astimezone(
            DEFAULT_TIME_ZONE
        )  # .isoformat()
        if silence_update_request.ends_at
        else silence_update_request.ends_at
    )

    return __service.modify_silence(silence)
