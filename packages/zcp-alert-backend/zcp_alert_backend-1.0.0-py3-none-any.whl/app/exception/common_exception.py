"""
Exceptions for AlertRequest

"""

from enum import Enum
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel


class Error(BaseModel):
    http_status: Optional[int]
    code: Optional[str]
    message: Optional[str]


class AlertError(Enum):
    ID_NOT_FOUND = Error(
        code="E001",
        http_status=HTTPStatus.NOT_FOUND,
        message="The item {document}:'{object_id}' was not found",
    )
    """The keyword arguments '{document}' and '{object_id}' should be present in the message string"""
    INVALID_OBJECTID = Error(
        code="E002",
        http_status=HTTPStatus.BAD_REQUEST,
        message="The input value was invalid. Details: {details}",
    )
    """The keyword argument '{details}' should be present in the message string"""
    BAD_REQUEST = Error(
        code="E003",
        http_status=HTTPStatus.BAD_REQUEST,
        message="Bad request. Details: {details}",
    )
    """The keyword argument '{details}' should be present in the message string"""
    INVALID_TOKEN = Error(
        code="E004",
        http_status=HTTPStatus.UNAUTHORIZED,
        message="Invalid token. Details: {details}",
    )
    """The keyword argument '{details}' should be present in the message string"""
    PERMISSION_DENIED = Error(
        code="E005",
        http_status=HTTPStatus.FORBIDDEN,
        message="Permission denied. Details: {details}",
    )
    """The keyword argument '{details}' should be present in the message string"""
    TOKEN_DATA_TOO_LARGE = Error(
        code="E006",
        http_status=HTTPStatus.BAD_REQUEST,
        message="The token data for the client cookie is too large. Details: {details}",
    )
    """The keyword argument '{details}' should be present in the message string"""
    SESSION_EXPIRED = Error(
        code="E007",
        http_status=HTTPStatus.UNAUTHORIZED,
        message="The session is expired. Details: {details}",
    )
    """The keyword argument '{details}' should be present in the message string"""
    OAUTH_IDP_ERROR = Error(
        code="E008",
        http_status=HTTPStatus.UNAUTHORIZED,
        message="OAuth IDP error. Details: {details}",
    )
    """The keyword argument '{details}' should be present in the message string"""
    KAKAO_CHANNEL_ERROR = Error(
        code="E101",
        http_status=HTTPStatus.BAD_REQUEST,
        message="Kakao Talk error. Details: {details}",
    )
    """The keyword argument '{details}' should be present in the message string"""
    KAKAO_TOKEN_ERROR = Error(
        code="E101",
        http_status=HTTPStatus.UNAUTHORIZED,
        message="Kakao Talk error. Details: {details}",
    )
    """The keyword argument '{details}' should be present in the message string"""
    INTERNAL_SERVER_ERROR = Error(
        code="E500",
        http_status=HTTPStatus.INTERNAL_SERVER_ERROR,
        message="Internal server error. Details: {details}",
    )
    """The keyword argument '{details}' should be present in the message string"""


class AlertBackendException(HTTPException):
    def __init__(self, error: AlertError, **kwargs):
        self.status_code = error.value.http_status
        self.code = error.value.code
        self.detail = error.value.message.format(**kwargs)
        super().__init__(status_code=self.status_code, detail=self.detail)


class OauthTokenValidationException(HTTPException):
    def __init__(self, error: AlertError, **kwargs):
        self.status_code = error.value.http_status
        self.code = error.value.code
        self.detail = error.value.message.format(**kwargs)
        super().__init__(status_code=self.status_code, detail=self.detail)
