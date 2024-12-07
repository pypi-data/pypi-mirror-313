import json
import logging
from typing import Any, Dict
from zoneinfo import ZoneInfo

from app.client.httpx_client import HTTPBaseClient
from app.model.alert_model import Action, AlertStatus, ZcpAlert
from app.model.channel_model import AuthenticationType
from app.settings import ALERT_VIEW_URL, HTTP_CLIENT_SSL_VERIFY, WEBHOOK_DEFAULT_TIMEOUT

# _DISPLAY_TIMEZONE = DEFAULT_TIME_ZONE
_DISPLAY_TIMEZONE = ZoneInfo("Asia/Seoul")

log = logging.getLogger("appLogger")


class GoogleChatClient(HTTPBaseClient):
    def __init__(self, url: str):
        super().__init__(
            url,
            authentication_type=AuthenticationType.NONE,
            tls_verify=HTTP_CLIENT_SSL_VERIFY,
            timeout=WEBHOOK_DEFAULT_TIMEOUT,
        )

    def _generate_payload(
        self,
        *,
        alert: ZcpAlert,
        action: Action | None = None,
        modifier: str | None = None,
    ) -> str:
        if action is None:
            """ when the alert is coming from the alertmanager or any other source """
            if alert.status == AlertStatus.OPEN:
                """ when the alert is coming with the status is open"""
                if alert.repeated_count > 0:
                    payload = self._convert_to_massage_for_repeated(alert=alert)
                else:
                    payload = self._convert_to_massage_for_new(
                        alert=alert,
                    )
            else:
                """ when the alert is coming with the status is closed"""
                payload = self._convert_to_massage_for_user_actions(alert=alert)
        else:
            """ when the alert is coming from the user action (ack, unack, snooze, close) """
            payload = self._convert_to_massage_for_user_actions(
                alert=alert, action=action, modifier=modifier
            )

        return payload

    def _convert_to_massage_for_user_actions(
        self,
        *,
        alert: ZcpAlert,
        action: Action | None = None,
        modifier: str | None = None,
    ) -> str:
        """Convert ZcpAlert to Slack message for user actions"""
        status_tilte = ""
        if action == Action.UNACK:
            status_tilte = "Unacked"
        elif action == Action.WAKEUP:
            status_tilte = "Woken"
        else:
            status_tilte = alert.status.value

        subject = f"{status_tilte if status_tilte else 'N/A'}"
        snoozed_info = (
            f"until at _{alert.snoozed_until_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds')}_"
            if alert.status == AlertStatus.SNOOZED
            and alert.snoozed_until_at is not None
            else ""
        )
        description = (
            alert.annotations["description"]
            if alert.annotations["description"]
            else "N/A"
        )
        modifier = modifier if modifier else alert.sender.value

        payload = {
            "text": f"*{subject}* the alert (#{alert.id}) "
            f"{snoozed_info} "
            f"by {modifier}\n"
            f"<{ALERT_VIEW_URL.format(alert_id=alert.id)}|{description}>"
        }

        log.debug(f"Converted payload: {json.dumps(payload, indent=2)}")

        return json.dumps(payload)

    def _convert_to_massage_for_repeated(
        self,
        *,
        alert: ZcpAlert,
    ) -> str:
        """Convert ZcpAlert to Slack message for repeated alert"""
        description = (
            alert.annotations["description"]
            if alert.annotations["description"]
            else "N/A"
        )
        modifier = alert.sender.value

        payload = {
            "text": f"Triggered repeatedly {alert.repeated_count} times the alert (#{alert.id}) "
            f"by {modifier}\n"
            f"<{ALERT_VIEW_URL.format(alert_id=alert.id)}|{description}>"
        }

        log.debug(f"Converted payload: {json.dumps(payload, indent=2)}")

        return json.dumps(payload)

    def _convert_to_massage_for_new(self, *, alert: ZcpAlert) -> str:
        """
        Convert ZcpAlert to google chat message for new alert

        https://addons.gsuite.google.com/uikit/builder?hl=ko
        """

        payload = {
            "cards": [
                {
                    "header": self._get_header_section(alert=alert),
                    "sections": [
                        {
                            "widgets": self._get_alert_fields_widget(alert=alert),
                        }
                    ],
                }
            ]
        }

        log.debug(f"Converted payload: {json.dumps(payload, indent=2)}")

        return json.dumps(payload)

    def _get_header_section(self, *, alert: ZcpAlert) -> Dict[str, Any]:
        return {
            "title": f"[{alert.status.value}] {alert.annotations['summary'] if alert.annotations.get('summary') else 'N/A'}",
            "subtitle": f"{alert.annotations['description'] if alert.annotations.get('description') else 'N/A'}",
            "imageUrl": "https://fonts.gstatic.com/s/e/notoemoji/15.1/1f6a8/512.png=s60",
        }

    def _get_alert_fields_widget(self, *, alert: ZcpAlert) -> Dict[str, Any]:
        widgets = []
        widgets.append(
            {
                "textParagraph": {
                    "text": f"<b>* Priority</b>: {alert.labels['priority'] if alert.labels.get('priority') else 'N/A'}"
                }
            }
        )
        widgets.append(
            {
                "textParagraph": {
                    "text": f"<b>* Severity</b>: {alert.labels['severity'] if alert.labels.get('severity') else 'N/A'}"
                }
            }
        )
        widgets.append(
            {
                "textParagraph": {
                    "text": f"<b>* Cluster</b>: {alert.labels['cluster'] if alert.labels.get('cluster') else 'N/A'}"
                }
            }
        )
        widgets.append(
            {
                "textParagraph": {
                    "text": f"<b>* Namespace</b>: {alert.labels['namespace'] if alert.labels.get('namespace') else 'N/A'}"
                }
            }
        )
        widgets.append(
            {
                "textParagraph": {
                    "text": f"<b>* Occured At</b>: {alert.starts_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds') if alert.starts_at else 'N/A'}"
                }
            }
        )
        widgets.append(
            {
                "textParagraph": {
                    "text": f"<b>* Triggered At</b>: {alert.created_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds') if alert.created_at else 'N/A'}"
                }
            }
        )
        widgets.append(
            {
                "textParagraph": {
                    "text": f"<b>* Sender</b>: {alert.sender.value if alert.sender else 'N/A'}"
                }
            }
        )
        widgets.append({"textParagraph": {"text": f"<b>* ID</b>: {alert.id}"}})

        widgets.append(
            {
                "buttons": [
                    {
                        "textButton": {
                            "text": "Go to alert",
                            "onClick": {
                                "openLink": {
                                    "url": f"{ALERT_VIEW_URL.format(alert_id=alert.id)}"
                                }
                            },
                        }
                    }
                ]
            }
        )

        return widgets

    def _generate_test_message(self, *, modifier: str | None = None) -> str:
        payload = {"text": f"Test message from ZCP Alert Manager. Sent by : {modifier}"}

        log.debug(f"Converted payload: {json.dumps(payload, indent=2)}")

        return json.dumps(payload)
