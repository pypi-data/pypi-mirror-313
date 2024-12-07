import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query, Request
from fastapi.responses import JSONResponse

from app.auth.oauth2_keycloak import TokenData, get_current_user
from app.model.channel_model import ChannelType
from app.model.integration_model import (
    Filter,
    FilterMode,
    Integration,
    IntegrationSortField,
    IntegrationStatus,
)
from app.schema.integration_request_model import (
    IntegrationCreateRequest,
    IntegrationUpdateRequest,
)
from app.schema.list_model import IntegrationList
from app.schema.response_model import ResponseModel
from app.service.alert_service import AlertService
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
    "/integrations",
    summary="Get integrations",
    response_class=JSONResponse,
    response_model=IntegrationList,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_integrations(
    request: Request,
    name: Optional[str] = Query(
        None,
        max_length=100,
        title="channel name",
        description="Search query string for name. The max length is 100",
    ),
    channel_name: Optional[str] = Query(
        None,
        max_length=100,
        title="channel name",
        description="Search query string for channel name. The max length is 100",
    ),
    channel_type: ChannelType = Query(
        None, title="channel type", description="Search query string for channel type."
    ),
    status: IntegrationStatus = Query(
        None, title="integration status", description="Search query string for status"
    ),
    sort_field: IntegrationSortField = Query(
        IntegrationSortField.NAME, title="sort field", description="Sort field name"
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
) -> IntegrationList:
    """A restful API to get integrations"""
    return IntegrationList(
        current_page=page_number,
        page_size=page_size,
        total=__service.get_integrations_count(
            name=name,
            channel_name=channel_name,
            channel_type=channel_type,
            status=status,
        ),
        data=__service.get_integrations(
            name=name,
            channel_name=channel_name,
            channel_type=channel_type,
            status=status,
            sort_field=sort_field,
            sort_direction=sort_direction,
            page_number=page_number,
            page_size=page_size,
        ),
    )


@router.get(
    "/integrations/all/combo",
    summary="Get all integrations for combo",
    response_class=JSONResponse,
    response_model=list[dict],
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_all_integrations(
    oauth_user: TokenData = Depends(get_current_user),
) -> list[dict]:
    """A restful API to get integrations"""
    return __service.get_all_integrations()


@router.post(
    "/integrations",
    summary="Create an integration",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def create_integration(
    integration_create_request: IntegrationCreateRequest,
    oauth_user: TokenData = Depends(get_current_user),
) -> ResponseModel:
    """A restful API to create an integration

    Parameters
    ----------
    integration : Integration

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
    integration = Integration(**integration_create_request.model_dump())
    integration.modifier = oauth_user.username
    return ResponseModel(
        data={"inserted_id": __service.create_integration(integration)}
    )


@router.get(
    "/integrations/{integration_id}",
    summary="Get an integration",
    response_class=JSONResponse,
    response_model=Integration,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_integration(
    integration_id: str, oauth_user: TokenData = Depends(get_current_user)
) -> Integration:
    """A restful API to get an integration

    Parameters
    ----------
    integration_id : str

    Returns
    -------
    Integration
    """
    return __service.get_integration(integration_id)


@router.delete(
    "/integrations/{integration_id}",
    summary="Remove an integration",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def remove_integration(
    integration_id: str, oauth_user: TokenData = Depends(get_current_user)
) -> ResponseModel:
    """A restful API to remove an integration

    Parameters
    ----------
    integration_id : str

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
    __service.remove_integration(integration_id)
    return ResponseModel()


@router.put(
    "/integrations",
    summary="Modify an integration",
    response_class=JSONResponse,
    response_model=Integration,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def modify_integration(
    integration_update_request: IntegrationUpdateRequest,
    oauth_user: TokenData = Depends(get_current_user),
) -> Integration:
    """A restful API to modify an integration

    Parameters
    ----------
    integration : Integration

    Returns
    -------
    Integration
    """
    integration = Integration(**integration_update_request.model_dump())
    integration.modifier = oauth_user.username
    return __service.modify_integration(integration)


@router.patch(
    "/integrations/{integration_id}/status/{status}",
    summary="Patch an integration status",
    response_class=JSONResponse,
    response_model=Integration,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def modify_integration_status(
    integration_id: str = Path(..., title="Integration id", description="Alert id"),
    status: IntegrationStatus = Path(
        ..., title="Integration status", description="Integration status"
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> Integration:
    """A restful API to patch an integration status

    Parameters
    ----------
    integration_id : str, optional
        by default Path(..., title="Integration id", description="Alert id")

    status : IntegrationStatus, optional
        by default Path(..., title="Integration status", description="Integration status")

    Returns
    -------
    Integration
    """
    return __service.patch_integration_status(
        integration_id=integration_id, status=status, modifier=oauth_user.username
    )


@router.get(
    "/integration/filters",
    summary="Get filters for integrations",
    response_class=JSONResponse,
    response_model=List[Filter],
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def get_integration_filters() -> List[Filter]:
    """A restful API to get filters for integrations

    Returns
    -------
    List[Filter]
    """
    return __service.get_integration_filters()


@router.get(
    "/integration/filters/modes",
    summary="Get filter modes for integrations",
    response_class=JSONResponse,
    response_model=List[FilterMode],
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def get_integration_filter_modes() -> List[FilterMode]:
    """A restful API to get filters for integrations

    Returns
    -------
    List[Filter]
    """
    return __service.get_integration_filter_modes()
