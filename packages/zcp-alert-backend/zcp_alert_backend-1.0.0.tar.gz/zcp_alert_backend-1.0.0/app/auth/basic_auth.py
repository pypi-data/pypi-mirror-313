from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.model.auth_model import BasicAuthUser
from app.service.alert_service import AlertService

_service = AlertService()

basic_security = HTTPBasic()


def verify_basic_auth_user(credentials: HTTPBasicCredentials):
    user = _service.get_basic_auth_user_by_username(credentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{credentials.username} not found",
            headers={"WWW-Authenticate": "Basic"},
        )

    if user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password is incorrect",
            headers={"WWW-Authenticate": "Basic"},
        )

    return BasicAuthUser(username=credentials.username, password=credentials.password)


def get_current_user_for_basicauth(
    credentials: HTTPBasicCredentials = Depends(basic_security),
) -> BasicAuthUser:
    return verify_basic_auth_user(credentials)
