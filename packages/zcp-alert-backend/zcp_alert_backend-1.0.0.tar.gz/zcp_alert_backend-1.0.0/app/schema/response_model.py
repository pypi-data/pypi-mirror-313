from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from app.model.result_model import Result


class ResponseModel(BaseModel):
    """Result model for alert"""

    result: Result = Result.SUCCESS
    message: Optional[str] = None
    code: Optional[str] = None
    data: Optional[Any] = None

    model_config = ConfigDict(exclude_none=True)
