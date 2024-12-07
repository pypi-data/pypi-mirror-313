import logging

import jwt
import requests
from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import ExpiredSignatureError, InvalidIssuedAtError, InvalidKeyError, PyJWTError

import app.settings as settings
from app.exception.common_exception import AlertError, OauthTokenValidationException
from app.model.auth_model import TokenData

log = logging.getLogger("appLogger")

# KeyCloak Configuration using the settings
KEYCLOAK_SERVER_URL = settings.KEYCLOAK_SERVER_URL
KEYCLOAK_REALM = settings.KEYCLOAK_REALM
KEYCLOAK_CLIENT_ID = settings.KEYCLOAK_CLIENT_ID
KEYCLOAK_CLIENT_SECRET = settings.KEYCLOAK_CLIENT_SECRET
ALGORITHM = "RS256"
KEYCLOAK_REDIRECT_URI = settings.KEYCLOAK_REDIRECT_URI

HTTP_CLIENT_SSL_VERIFY = settings.HTTP_CLIENT_SSL_VERIFY

# KeyCloak Endpoints
KEYCLOAK_REALM_ROOT_URL = (
    f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect"
)
KEYCLOAK_JWKS_ENDPOINT = f"{KEYCLOAK_REALM_ROOT_URL}/certs"
KEYCLOAK_AUTH_ENDPOINT = f"{KEYCLOAK_REALM_ROOT_URL}/auth"
KEYCLOAK_TOKEN_ENDPOINT = KEYCLOAK_REFRESH_ENDPOINT = f"{KEYCLOAK_REALM_ROOT_URL}/token"
KEYCLOAK_USER_ENDPOINT = f"{KEYCLOAK_REALM_ROOT_URL}/userinfo"
KEYCLOAK_END_SESSION_ENDPOINT = f"{KEYCLOAK_REALM_ROOT_URL}/logout"


def get_public_key():
    response = requests.get(
        KEYCLOAK_JWKS_ENDPOINT, verify=HTTP_CLIENT_SSL_VERIFY
    )  # verify=False: because of the SKCC self-signed certificate
    jwks = response.json()

    public_key = None
    try:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks["keys"][0])
    except InvalidKeyError as ike:
        log.error(f"InvalidKeyError: {ike}")

    return public_key


PUBLIC_KEY = get_public_key()
# oauth2_token_scheme = OAuth2PasswordBearer(tokenUrl=KEYCLOAK_TOKEN_ENDPOINT)

oauth2_auth_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=KEYCLOAK_AUTH_ENDPOINT,
    tokenUrl=KEYCLOAK_TOKEN_ENDPOINT,
    refreshUrl=KEYCLOAK_USER_ENDPOINT,
    # scopes={"openid": "openid", "profile": "profile", "email": "email"}
)


def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            jwt=token,
            key=PUBLIC_KEY,
            algorithms=[ALGORITHM],
            audience=KEYCLOAK_CLIENT_ID,
            options={"verify_aud": False, "verify_iat": False},
            leeway=60,
        )
        """
            # if not options["verify_signature"]:
            # options.setdefault("verify_exp", False)
            # options.setdefault("verify_nbf", False)
            # options.setdefault("verify_iat", False)
            # options.setdefault("verify_aud", False)
            # options.setdefault("verify_iss", False)
        """
        if payload is None:
            raise OauthTokenValidationException(
                AlertError.INVALID_TOKEN, details="jwt docode failed"
            )

        token_data = TokenData(username=payload.get("preferred_username"), **payload)
    except ExpiredSignatureError as ese:
        log.error(f"ExpiredSignatureError: {ese}")
        raise OauthTokenValidationException(AlertError.INVALID_TOKEN, details=str(ese))
    except InvalidIssuedAtError as iiae:
        log.error(f"InvalidIssuedAtError: {iiae}")
        raise OauthTokenValidationException(AlertError.INVALID_TOKEN, details=str(iiae))
    except PyJWTError as jwte:
        log.error(f"JWTError: {jwte}")
        raise OauthTokenValidationException(AlertError.INVALID_TOKEN, details=str(jwte))

    return token_data


async def get_current_user(token: str = Depends(oauth2_auth_scheme)) -> TokenData:
    return verify_token(token)
