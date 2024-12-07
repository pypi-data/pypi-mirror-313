import json
import logging
from typing import Dict, Tuple
from zoneinfo import ZoneInfo

import requests

from app.model.alert_model import Action, AlertStatus, ZcpAlert
from app.model.kakaotalk_model import KakaoTalkFriend, KakaoTalkToken
from app.settings import (
    ALERT_VIEW_URL,
    KAKAO_API_ENDPOINT,
    KAKAO_AUTH_ENDPOINT,
    KAKAO_FRIENDS_LIMIT,
    WEBHOOK_DEFAULT_TIMEOUT,
)

# _DISPLAY_TIMEZONE = DEFAULT_TIME_ZONE
_DISPLAY_TIMEZONE = ZoneInfo("Asia/Seoul")

log = logging.getLogger("appLogger")


class KakaoTalkClient:
    def __init__(
        self,
        *,
        access_token: str | None = None,
        tls_verify: bool | None = False,
        timeout: int | None = WEBHOOK_DEFAULT_TIMEOUT,
    ):
        self._tls_verify = tls_verify
        self._timeout = timeout

        self._headers = {
            # "Content-Type": "application/json",
            "accept": "application/json",
        }

        self._access_token = access_token
        if self._access_token is not None:
            self._headers.update({"Authorization": f"Bearer {self._access_token}"})

    def _generate_payload(
        self,
        *,
        alert: ZcpAlert,
        action: Action | None = None,
        modifier: str | None = None,
    ) -> str:
        status_info = ""
        if action is None:
            if alert.status == AlertStatus.OPEN:
                if alert.repeated_count > 0:
                    status_info = (
                        f"Triggered the alert repeatedly {alert.repeated_count} times"
                    )
                else:
                    status_info = "Triggered the alert"
            else:
                status_info = f"{alert.status.value} the alert"
        else:
            status_tilte = ""
            if action == Action.UNACK:
                status_tilte = "Unacked"
            elif action == Action.WAKEUP:
                status_tilte = "Woken"
            else:
                status_tilte = alert.status.value

            status_info = f"{status_tilte if status_tilte else 'N/A'} alert"

        snoozed_info = (
            f"until at {alert.snoozed_until_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds')}"
            if alert.status == AlertStatus.SNOOZED
            and alert.snoozed_until_at is not None
            else ""
        )

        user_info = modifier if modifier else alert.sender.value

        action_text = ""
        action_text += f"{status_info}"
        action_text += f" {snoozed_info}" if snoozed_info else ""
        action_text += f" by {user_info}"

        message_text = ""
        message_text += f"{action_text}"
        message_text += f"\n\n{alert.annotations['summary'] if alert.annotations.get('summary') else ""}"
        message_text += f"\n\n{alert.annotations['description'] if alert.annotations.get('description') else ""}"
        message_text += f"\n\n{self.get_labels_text(alert)}"

        template_object = {
            "object_type": "text",
            "text": f"{message_text}",
            "link": {
                "web_url": f"{ALERT_VIEW_URL.format(alert_id=alert.id)}",
                "mobile_web_url": f"{ALERT_VIEW_URL.format(alert_id=alert.id)}",
            },
            "button_title": "Go to alert",
        }

        log.debug(
            f"Generated KakaoTalk payload: {json.dumps(template_object, indent=2)}"
        )

        return json.dumps(template_object)

    def get_labels_text(self, zcp_alert: ZcpAlert) -> str:
        labels_text = ""
        if zcp_alert.labels.get("priority"):
            labels_text += f"* Priority: {zcp_alert.labels['priority']}\n"
        if zcp_alert.labels.get("severity"):
            labels_text += f"* Severity: {zcp_alert.labels['severity']}\n"
        if zcp_alert.labels.get("cluster"):
            labels_text += f"* Cluster: {zcp_alert.labels['cluster']}\n"
        if zcp_alert.labels.get("namespace"):
            labels_text += f"* Namespace: {zcp_alert.labels['namespace']}\n"
        if zcp_alert.starts_at:
            labels_text += (
                f"* Occured At: {zcp_alert.starts_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds')}\n"
                if zcp_alert.starts_at
                else ""
            )
        if zcp_alert.created_at:
            labels_text += (
                f"* Triggered At: {zcp_alert.created_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds')}\n"
                if zcp_alert.created_at
                else ""
            )
        if zcp_alert.sender:
            labels_text += (
                f"* Sender: {zcp_alert.sender.value}\n" if zcp_alert.sender else ""
            )
        if zcp_alert.id:
            labels_text += f"* ID: {zcp_alert.id}"
        return labels_text

    def generate_kakaotalk_token(
        self, *, code: str, client_id: str, client_secret: str | None = None
    ) -> KakaoTalkToken:
        """Generate Kakao token

        https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#request-token

        Parameters
        ----------
        code : str
            the code which is returned from the Kakao OAuth2.0 during the authorization
        client_id : str
            the API key of the Kakao application
        client_secret : str | None, optional
            the API secret key of the Kakao application, by default None

        Returns
        -------
        KakaoToken
            the tokens which are returned from the Kakao OAuth2.0

        Raises
        ------
        Exception
            if failed to generate the Kakao token
        """
        data = {}
        data["grant_type"] = "authorization_code"
        data["client_id"] = client_id
        data["client_secret"] = client_secret
        data["code"] = code

        response = requests.post(f"{KAKAO_AUTH_ENDPOINT}/oauth/token", data=data)

        token = {}
        if response.ok:
            token = response.json()
        else:
            log.error(f"Failed to generate Kakao token: {response.text}")
            raise Exception(f"Failed to generate Kakao token: {response.text}")

        log.info("Kakao token generated successfully")

        return KakaoTalkToken(**token)

    def kakao_refresh_token(
        self, *, client_id: str, client_secret: str, refresh_token: str
    ) -> KakaoTalkToken:
        """Refresh Kakao token

        https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#refresh-token
        """
        data = {}
        data["grant_type"] = "refresh_token"
        data["client_id"] = client_id
        data["client_secret"] = client_secret
        data["refresh_token"] = refresh_token

        response = requests.post(f"{KAKAO_AUTH_ENDPOINT}/oauth/token", data=data)
        new_token = {}
        if response.ok:
            new_token = response.json()
        else:
            log.error(f"Failed to refresh Kakao token: {response.text}")
            raise Exception(f"Failed to refresh Kakao token: {response.text}")

        log.info("Kakao token refreshed successfully")

        return KakaoTalkToken(**new_token)

    def send_message_to_me(
        self,
        *,
        alert: ZcpAlert,
        action: Action | None = None,
        modifier: str | None = None,
    ) -> Tuple[Dict, str]:
        data = {
            "template_object": self._generate_payload(
                alert=alert, action=action, modifier=modifier
            )
        }

        response = requests.post(
            f"{KAKAO_API_ENDPOINT}/v2/api/talk/memo/default/send",
            headers=self._headers,
            data=data,
        )

        if response.ok:
            log.debug(
                f"Sent message successfully to me: {json.dumps(response.json(), indent=2)}"
            )
            return {"result": "success"}, None
        else:
            if (
                response.status_code == 401
                and response.reason == "Unauthorized"
                and response.json().get("code") == -401
                and response.json().get("msg") == "this access token deos not exist"
            ):
                return {"result": "failed"}, response.text

            else:
                return {"result": "failed"}, response.text

    def send_message_to_friends(
        self,
        *,
        alert: ZcpAlert,
        action: Action | None = None,
        modifier: str | None = None,
    ) -> Tuple[Dict, str]:
        friends = self.get_kakaotalk_friends()
        receiver_uuids = [f'"{friend.uuid}"' for friend in friends]

        data = {
            "receiver_uuids": f'[{','.join(receiver_uuids)}]',
            "template_object": self._generate_payload(
                alert=alert, action=action, modifier=modifier
            ),
        }

        response = requests.post(
            f"{KAKAO_API_ENDPOINT}/v1/api/talk/friends/message/default/send",
            headers=self._headers,
            data=data,
        )

        if response.ok:
            log.debug(
                f"Sent message successfully to friends: {json.dumps(response.json(), indent=2)}"
            )
            return {"result": "success"}, None
        else:
            return {"result": "failed"}, response.text

    def send_message_to_all(
        self,
        *,
        alert: ZcpAlert,
        action: Action | None = None,
        modifier: str | None = None,
    ) -> Tuple[Dict, str]:
        # 1. send message to me
        response, message = self.send_message_to_me(
            alert=alert, action=action, modifier=modifier
        )
        if response.get("result") == "failed":
            log.warning(f"Failed to send message to me because of: {message}")

        # 2. send message to friends
        response, message = self.send_message_to_friends(
            alert=alert, action=action, modifier=modifier
        )
        if response.get("result") == "failed":
            log.warning(f"Failed to send message to friends because of: {message}")
        else:
            return response, message

    def get_kakaotalk_friends(self) -> list[KakaoTalkFriend]:
        response = requests.get(
            f"{KAKAO_API_ENDPOINT}/v1/api/talk/friends?limit={KAKAO_FRIENDS_LIMIT}",
            headers=self._headers,
        )

        if response.ok:
            friends = response.json()
            return [KakaoTalkFriend(**friend) for friend in friends.get("elements", [])]
        else:
            raise Exception(f"Failed to generate Kakao token: {response.text}")
