import logging

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.schema.response_model import ResponseModel

log = logging.getLogger("appLogger")

router = APIRouter()


@router.get(
    "/healthz",
    summary="Health Check",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def healthz() -> ResponseModel:
    """A restful API to check the health of the service

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
    return ResponseModel()
