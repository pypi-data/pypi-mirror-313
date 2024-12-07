import logging
import sys

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from app.auth.oauth2_keycloak import (
    KEYCLOAK_AUTH_ENDPOINT,
    KEYCLOAK_CLIENT_ID,
    KEYCLOAK_CLIENT_SECRET,
    KEYCLOAK_END_SESSION_ENDPOINT,
    KEYCLOAK_REDIRECT_URI,
    KEYCLOAK_TOKEN_ENDPOINT,
    KEYCLOAK_USER_ENDPOINT,
    TokenData,
    get_current_user,
    oauth2_auth_scheme,
)
from app.exception.common_exception import AlertBackendException, AlertError
from app.settings import ALERT_API_ENDPOINT, HTTP_CLIENT_SSL_VERIFY

log = logging.getLogger("appLogger")

router = APIRouter()

# session_id_scheme = APIKeyCookie(name="session_id")
# csrf_scheme = APIKeyCookie(name="csrftoken")

# @router.get("/",
#             summary="Root page",
#             response_class=HTMLResponse)
# def root():
#     return RedirectResponse(url=f"{ALERT_API_ENDPOINT}/home")


@router.get("/home", summary="Home page", response_class=HTMLResponse)
def home(request: Request):  # , csrf_token: str = Depends(csrf_scheme)):
    # check the session_id in the cookie
    csrf_token = request.cookies.get("csrftoken")
    session_id = request.cookies.get("session_id")

    if csrf_token and session_id:
        user_info = request.session.get("user_info")
        if not user_info:
            request.session.clear()
            raise AlertBackendException(
                AlertError.SESSION_EXPIRED,
                code=401,
                details="Session data has been lost "
                "because the server has been restared."
                "Please login again",
            )
        else:
            username = user_info.get("preferred_username") if user_info else "Ooops!!"
            log.debug(f"session_data: {username}")
            return HTMLResponse(content=f"<p>Hello, {username}!!</p>")
    else:
        return RedirectResponse(url=f"{ALERT_API_ENDPOINT}/login")


@router.get("/login", summary="API to login into the keyclaok using the browser")
def login():
    return RedirectResponse(
        url=f"{KEYCLOAK_AUTH_ENDPOINT}?response_type=code"
        f"&client_id={KEYCLOAK_CLIENT_ID}"
        f"&redirect_uri={KEYCLOAK_REDIRECT_URI}"
        f"&scope=openid profile email"
    )


@router.get("/logout")
def logout(
    request: Request,
    # csrf_token: str = Depends(csrf_scheme),
    # session_id: str = Depends(session_id_scheme)
):
    csrf_token = request.cookies.get("csrftoken")
    session_id = request.cookies.get("session_id")
    if not csrf_token or not session_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No csrf token in cookie and session id in cookie",
        )

    else:
        refresh_token = request.session.get("refresh_token")

        # if not session_id and not refresh_token:
        if refresh_token:
            data = {
                "client_id": KEYCLOAK_CLIENT_ID,
                "client_secret": KEYCLOAK_CLIENT_SECRET,
                "refresh_token": refresh_token,
            }
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            idp_response = requests.post(
                KEYCLOAK_END_SESSION_ENDPOINT,
                data=data,
                headers=headers,
                verify=HTTP_CLIENT_SSL_VERIFY,
            )  # verify=False: because of the SKCC self-signed certificate

            if idp_response.status_code != 204:
                raise AlertBackendException(
                    AlertError.OAUTH_IDP_ERROR,
                    details=f"Failed to logout.({idp_response.reason})",
                )

        request.session.clear()

        redirect_response = RedirectResponse(url=f"{ALERT_API_ENDPOINT}/")
        redirect_response.delete_cookie(key="csrftoken")

        return redirect_response


@router.post("/oauth2/logout")
def logout_only_oauth(
    refresh_token: str | None, access_token: str = Depends(oauth2_auth_scheme)
):
    data = {
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
        "refresh_token": refresh_token,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "*/*"}
    idp_response = requests.post(
        KEYCLOAK_END_SESSION_ENDPOINT,
        data=data,
        headers=headers,
        verify=HTTP_CLIENT_SSL_VERIFY,
    )  # verify=False: because of the SKCC self-signed certificate

    if idp_response.status_code != 204:
        raise AlertBackendException(
            AlertError.OAUTH_IDP_ERROR,
            details=f"Failed to logout.({idp_response.reason})",
        )

    return {"result": "success"}


@router.get("/oauth2/callback", summary="Keycloak OAuth2 callback for the redirect URI")
def callback(request: Request, code: str):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": KEYCLOAK_REDIRECT_URI,
        "client_id": KEYCLOAK_CLIENT_ID,
        "client_secret": KEYCLOAK_CLIENT_SECRET,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    idp_response = requests.post(
        KEYCLOAK_TOKEN_ENDPOINT,
        data=data,
        headers=headers,
        verify=HTTP_CLIENT_SSL_VERIFY,
    )  # verify=False: because of the SKCC self-signed certificate

    if idp_response.status_code != 200:
        raise AlertBackendException(
            AlertError.OAUTH_IDP_ERROR,
            details=f"Failed to obtain token.({idp_response.reason})",
        )

    tokens = idp_response.json()

    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")
    # id_token = tokens.get("id_token")

    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    idp_response = requests.get(
        KEYCLOAK_USER_ENDPOINT, headers=headers, verify=HTTP_CLIENT_SSL_VERIFY
    )  # verify=False: because of the SKCC self-signed certificate
    if idp_response.status_code != 200:
        raise AlertBackendException(
            AlertError.OAUTH_IDP_ERROR,
            details=f"Failed to fetch user info.({idp_response.reason})",
        )
    user_info = idp_response.json()

    log.debug(f"user_info: {user_info}")

    # because the max size of the cookie is 4kb, the session middleware saves the session data in the client side cookie in default
    # so, if the session data size is over than 4kb, the session data will be lost or occur the error in client side
    # request.session['access_token'] = access_token
    # request.session['id_token'] = id_token
    request.session["refresh_token"] = refresh_token
    request.session["user_info"] = user_info

    total_bytes = _get_size(request.session)

    if total_bytes > 4096:
        log.debug(f"Total bytes: {total_bytes}")
        log.warning(f"The session data size({total_bytes}) is over than 4kb.")
        raise AlertBackendException(
            AlertError.TOKEN_DATA_TOO_LARGE,
            details=f"The session data size is {total_bytes} bytes. It is over than 4kb.",
        )

    # If the same-site of cookie is 'lax', the cookie will be sent only if the request is same-site request
    # If the same-site of cookie is 'strict', the cookie will not be sent
    # return RedirectResponse(url=f"{ALERT_SERVICE_ENDPOINT}/home")

    return tokens


def _get_size(obj, seen=None):
    """Recursively find the size of objects including nested objects."""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Mark as seen
    seen.add(obj_id)
    # Recursively add sizes of referred objects
    if isinstance(obj, dict):
        size += sum([_get_size(v, seen) for v in obj.values()])
        size += sum([_get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, "__dict__"):
        size += _get_size(obj.__dict__, seen)
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([_get_size(i, seen) for i in obj])
    return size


@router.get("/users/me", summary="Get the current user info from IDP(Keycloak)")
def read_users_me(token: str = Depends(oauth2_auth_scheme)):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    idp_response = requests.get(
        KEYCLOAK_USER_ENDPOINT, headers=headers, verify=HTTP_CLIENT_SSL_VERIFY
    )  # verify=False: because of the SKCC self-signed certificate
    if idp_response.status_code != 200:
        raise AlertBackendException(
            AlertError.OAUTH_IDP_ERROR,
            details=f"Failed to fetch user info: {idp_response.reason}",
        )
    return idp_response.json()


@router.get("/users/oauth_user", summary="Get the current user info from Token")
def read_oauth_user(oauth_user: TokenData = Depends(get_current_user)):
    return oauth_user
