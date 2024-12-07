import json
import logging

from app.client.httpx_client import HTTPBaseClient
from app.model.alert_model import Action, ZcpAlert
from app.model.channel_model import AuthenticationType
from app.settings import ALERT_VIEW_URL, WEBHOOK_DEFAULT_TIMEOUT

log = logging.getLogger("appLogger")


class WebhookClient(HTTPBaseClient):
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
        super().__init__(
            url,
            authentication_type=authentication_type,
            username=username,
            password=password,
            bearer_token=bearer_token,
            tls_verify=tls_verify,
            timeout=timeout,
        )

    def _generate_payload(
        self,
        *,
        alert: ZcpAlert,
        action: Action | None = None,
        modifier: str | None = None,
    ) -> str:
        if action is not None:
            alert.action = action
            if modifier is not None:
                alert.action_modifier = modifier

        alert.detail_view_url = ALERT_VIEW_URL.format(alert_id=alert.id)

        log.debug(
            f"Generated payload: {alert.model_dump_json(exclude=['activities'], indent=2)}"
        )

        return alert.model_dump_json(exclude=["activities"])

    def _generate_test_message(self, *, modifier: str | None = None) -> str:
        payload = {
            "message": f"Test message from ZCP Alert Manager. Sent by : {modifier}"
        }

        log.debug(f"Converted payload: {json.dumps(payload, indent=2)}")

        return json.dumps(payload)
