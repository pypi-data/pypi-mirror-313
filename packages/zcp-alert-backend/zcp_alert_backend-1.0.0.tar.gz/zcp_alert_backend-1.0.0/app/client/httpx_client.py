import logging
from abc import abstractmethod
from typing import Optional, Tuple

from httpx import AsyncClient, BasicAuth, Client, Response

from app.model.alert_model import Action, ZcpAlert
from app.model.channel_model import AuthenticationType
from app.settings import WEBHOOK_DEFAULT_TIMEOUT

log = logging.getLogger("appLogger")


class HTTPBaseClient:
    def __init__(
        self,
        url: str,
        /,
        *,
        authentication_type: AuthenticationType | None = AuthenticationType.NONE,
        username: str | None = None,
        password: str | None = None,
        bearer_token: str | None = None,
        tls_verify: bool | None = False,
        timeout: int | None = WEBHOOK_DEFAULT_TIMEOUT,
    ):
        self._url = url
        self._authentication_type = authentication_type
        self._username = username
        self._password = password
        self._bearer_token = bearer_token
        self._tls_verify = tls_verify
        self._timeout = timeout

        self._auth = (
            BasicAuth(username=username, password=password)
            if authentication_type == AuthenticationType.BASIC
            else None
        )

        self._headers = {
            "Content-Type": "application/json",
        }
        if (
            self._authentication_type == AuthenticationType.BEARER
            and self._bearer_token is not None
        ):
            self._headers.update({"Authorization": f"Bearer {self._bearer_token}"})

    async def async_request(
        self,
        *,
        alert: ZcpAlert,
        action: Action | None = None,
        headers: dict | None = None,
        modifier: str | None = None,
    ) -> Tuple[Response, Optional[str]]:
        """
        Request to the webhook URL with headers and data in asyncronous way
        """
        self._headers.update(headers or {})

        payload = self._generate_payload(alert=alert, action=action, modifier=modifier)

        log.debug(
            f"Async request {self._url}\n"
            f"headers: {self._headers}\n"
            f"payload: {payload}"
        )

        async with AsyncClient(auth=self._auth, verify=self._tls_verify) as client:
            try:
                response = await client.post(
                    url=self._url,
                    headers=self._headers,
                    data=payload,
                    timeout=self._timeout,
                )
            except Exception as e:
                log.error(f"Error while calling {self._url}: {str(e)}")
                return None, str(e)

            return response, "success"

    def sync_request(
        self,
        *,
        alert: ZcpAlert,
        action: Action | None = None,
        headers: dict | None = None,
        modifier: str | None = None,
    ) -> Tuple[Response, Optional[str]]:
        """
        Request to the webhook URL with headers and data in synchronous way
        """
        self._headers.update(headers or {})

        payload = self._generate_payload(alert=alert, action=action, modifier=modifier)

        log.debug(
            f"Sync request URL: {self._url}\n"
            f"headers: {self._headers}\n"
            f"payload: {payload}"
        )

        with Client(auth=self._auth, verify=self._tls_verify) as client:
            try:
                response = client.post(
                    url=self._url,
                    headers=self._headers,
                    data=payload,
                    timeout=self._timeout,
                )
            except Exception as e:
                log.error(f"Error while calling {self._url}: {str(e)}")
                return None, str(e)

            return response, "success"

    @abstractmethod
    def _generate_payload(
        self,
        *,
        alert: ZcpAlert,
        action: Action | None = None,
        modifier: str | None = None,
    ) -> str:
        """Generate payload for the request in child class"""
        ...

    def send_test_message(
        self, *, headers: dict | None = None, modifier: str | None = None
    ) -> Tuple[Response, Optional[str]]:
        """send test message to the webhook URL in synchronous way

        Parameters
        ----------
        headers : dict | None, optional
        modifier : str | None, optional

        Returns
        -------
        Tuple[Response, Optional[str]]
        """
        self._headers.update(headers or {})

        payload = self._generate_test_message(modifier=modifier)

        log.debug(
            f"Sync request URL: {self._url}\n"
            f"headers: {self._headers}\n"
            f"payload: {payload}"
        )

        with Client(auth=self._auth, verify=self._tls_verify) as client:
            try:
                response = client.post(
                    url=self._url,
                    headers=self._headers,
                    data=payload,
                    timeout=self._timeout,
                )
            except Exception as e:
                log.error(f"Error while calling {self._url}: {str(e)}")
                return None, str(e)

            return response, "success"

    @abstractmethod
    def _generate_test_message(self, *, modifier: str | None = None) -> str:
        """Generate payload for the request in child class"""
        ...
