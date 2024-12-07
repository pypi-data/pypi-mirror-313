import logging
from typing import Dict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.auth.oauth2_keycloak import TokenData, get_current_user
from app.exception.common_exception import AlertBackendException, AlertError
from app.model.integration_model import Integration
from app.model.result_model import Result
from app.schema.response_model import ResponseModel
from app.service.alert_service import AlertService

log = logging.getLogger("appLogger")

router = APIRouter()

__service = AlertService()


@router.get(
    "/admin/integration/cache",
    summary="Get cached integrations",
    response_class=JSONResponse,
    response_model=Dict[str, Integration],
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def get_cached_integrations(
    oauth_user: TokenData = Depends(get_current_user),
) -> Dict[str, Integration]:
    """A restful API to get cached integrations

    Parameters
    ----------

    Returns
    -------
    Dict[str, Integration]

    Raises
    ------
    AlertBackendException
    """
    if oauth_user.is_platform_admin() or oauth_user.is_alert_admin():
        return __service._get_cached_integrations()
    else:
        raise AlertBackendException(
            AlertError.PERMISSION_DENIED,
            details="You don't have permission to access this resource",
        )


@router.put(
    "/admin/integration/cache/refresh",
    summary="Refresh cached integrations",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def refresh_cached_integrations(
    oauth_user: TokenData = Depends(get_current_user),
) -> ResponseModel:
    """A restful API to refresh cached integrations

    Parameters
    ----------

    Returns
    -------
    ResponseModel
        returns a response model like following
    ```json
    {
        "result": "success"
    }
    ```

    Raises
    ------
    AlertBackendException
    """
    if oauth_user.is_platform_admin() or oauth_user.is_alert_admin():
        result = (
            Result.SUCCESS
            if __service._refresh_cached_integrations()
            else Result.FAILURE
        )
        return ResponseModel(
            result=result,
        )
    else:
        raise AlertBackendException(
            AlertError.PERMISSION_DENIED,
            details="You don't have permission to access this resource",
        )
