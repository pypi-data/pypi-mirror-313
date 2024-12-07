import json
import logging
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

from app.client.httpx_client import HTTPBaseClient
from app.model.alert_model import Action, AlertStatus, Priority, ZcpAlert
from app.model.channel_model import AuthenticationType
from app.settings import (
    ALERT_VIEW_URL,
    HTTP_CLIENT_SSL_VERIFY,
    SLACK_ACTION_ENABLED,
    WEBHOOK_DEFAULT_TIMEOUT,
)

log = logging.getLogger("appLogger")

# _DISPLAY_TIMEZONE = DEFAULT_TIME_ZONE
_DISPLAY_TIMEZONE = ZoneInfo("Asia/Seoul")


class SlackClient(HTTPBaseClient):
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
        """
        Convert ZcpAlert to Slack message

        https://api.slack.com/interactivity/handling#payloads
        https://app.slack.com/block-kit-builder/
        """
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

        emoji = ""
        if action is not None:
            if action == Action.ACK:
                emoji = ":white_check_mark:"
            elif action == Action.SNOOZE:
                emoji = ":zzz:"
            elif action == Action.CLOSE:
                emoji = ":negative_squared_cross_mark:"
            elif action == Action.UNACK:
                emoji = ":ballot_box_with_check:"
        else:
            # resolved by alertmanager
            emoji = ":negative_squared_cross_mark:"

        payload = {
            "attachments": [
                {
                    "color": self._get_color_by_status(alert.status),
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"{emoji} *{subject}* the alert (#{alert.id}) "
                                f"{snoozed_info} "
                                f"by {modifier}\n"
                                f"<{ALERT_VIEW_URL.format(alert_id=alert.id)}|{description}>",
                            },
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"_*Triggered at* {alert.updated_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds')}_",
                                }
                            ],
                        },
                    ],
                }
            ]
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
            "attachments": [
                {
                    "color": self._get_color_by_status(alert.status),
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f":heavy_plus_sign: Triggered repeatedly {alert.repeated_count} times the alert (#{alert.id}) "
                                f"by {modifier} \n"
                                f"<{ALERT_VIEW_URL.format(alert_id=alert.id)}|{description}>",
                            },
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"_*Triggered at* {alert.updated_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds')}_",
                                }
                            ],
                        },
                    ],
                }
            ]
        }

        log.debug(f"Converted payload: {json.dumps(payload, indent=2)}")

        return json.dumps(payload)

    def _convert_to_massage_for_new(self, *, alert: ZcpAlert) -> str:
        """
        Convert ZcpAlert to Slack message

        https://api.slack.com/interactivity/handling#payloads
        https://app.slack.com/block-kit-builder/
        """
        priority_for_color = (
            alert.labels["priority"] if alert.labels.get("priority") else Priority.P5
        )

        blocks = []
        blocks.append(self._get_header_section(alert=alert))
        blocks.append(self._get_description_section(alert=alert))
        blocks.append(self._get_divider())
        blocks.append(self._get_infomation_fields_setion(alert=alert))
        blocks.append(self._get_action_buttons(alert=alert))
        blocks.append(self._get_divider())
        blocks.append(self._get_details_section(alert=alert))

        payload = {
            "attachments": [
                {
                    "color": self._get_color_by_priority(priority=priority_for_color),
                    "blocks": blocks,
                }
            ]
        }

        log.debug(f"Converted payload: {json.dumps(payload, indent=2)}")

        return json.dumps(payload)

    def _get_header_section(self, *, alert: ZcpAlert) -> Dict[str, Any]:
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": (
                    f":rotating_light: [{alert.status.value}] {alert.annotations['summary']
                    if alert.annotations.get('summary')
                    else 'N/A'}"
                ),
                "emoji": True,
            },
        }

    def _get_description_section(self, *, alert: ZcpAlert) -> Dict[str, Any]:
        description = (
            f"<{ALERT_VIEW_URL.format(alert_id=alert.id)}| {alert.annotations['description']} >"
            if alert.annotations.get("description")
            else "N/A"
        )

        return {"type": "section", "text": {"type": "mrkdwn", "text": f"{description}"}}

    def _get_infomation_fields_setion(self, *, alert: ZcpAlert) -> List[Dict[str, Any]]:
        fields = []
        fields.append(
            {
                "type": "mrkdwn",
                "text": f"*Priority:*\n{alert.labels['priority'] if alert.labels.get('priority') else 'N/A'}",
            }
        )
        fields.append(
            {
                "type": "mrkdwn",
                "text": f"*Severity:*\n{alert.labels['severity'] if alert.labels.get('severity') else 'N/A'}",
            }
        )
        fields.append(
            {
                "type": "mrkdwn",
                "text": f"*Clsuter:*\n{alert.labels['cluster'] if alert.labels.get('cluster') else 'N/A'}",
            }
        )
        fields.append(
            {
                "type": "mrkdwn",
                "text": f"*Namespace:*\n{alert.labels['namespace'] if alert.labels.get('namespace') else 'N/A'}",
            }
        )
        fields.append(
            {
                "type": "mrkdwn",
                "text": f"*Occured At:*\n{alert.starts_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds') if alert.starts_at else 'N/A'}",
            }
        )
        fields.append(
            {
                "type": "mrkdwn",
                "text": f"*Triggered At:*\n{alert.created_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds') if alert.created_at else 'N/A'}",
            }
        )
        fields.append(
            {
                "type": "mrkdwn",
                "text": f"*Sender:*\n{alert.sender.value if alert.sender else 'N/A'}",
            }
        )
        fields.append({"type": "mrkdwn", "text": f"*ID:*\n{alert.id}"})

        return {"type": "section", "fields": fields}

    def _get_divider(self) -> Dict[str, Any]:
        return {"type": "divider"}

    def _get_action_buttons(self, *, alert: ZcpAlert) -> Dict[str, Any]:
        elements = []
        elements.append(
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "Go to alert", "emoji": True},
                "url": f"{ALERT_VIEW_URL.format(alert_id=alert.id)}",
            }
        )

        if SLACK_ACTION_ENABLED:
            elements.append(
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Ack", "emoji": True},
                    "value": f"{alert.id}",
                    "action_id": "ack",
                }
            )
            elements.append(
                {
                    "type": "button",
                    "text": {"type": "plain_text", "emoji": True, "text": "Snooze"},
                    "value": f"{alert.id}",
                    "action_id": "snooze",
                }
            )
            elements.append(
                {
                    "type": "button",
                    "text": {"type": "plain_text", "emoji": True, "text": "Close"},
                    "style": "primary",
                    "value": f"{alert.id}",
                    "action_id": "close",
                }
            )

        return {"type": "actions", "elements": elements}

    def _get_details_section(self, *, alert: ZcpAlert) -> Dict[str, Any]:
        elements = []
        elements.append(
            {
                "type": "rich_text_section",
                "elements": [{"type": "text", "text": "Detail informations\n"}],
            }
        )
        elements.append(
            {
                "type": "rich_text_list",
                "style": "bullet",
                "elements": self._get_label_details(alert=alert),
            }
        )

        return {"type": "rich_text", "elements": elements}

    def _get_label_details(self, *, alert: ZcpAlert) -> List[Dict[str, Any]]:
        elements = []
        for key, value in alert.labels.items():
            elements.append(
                {
                    "type": "rich_text_section",
                    "elements": [
                        {"type": "text", "text": f"{key}: "},
                        {"type": "text", "text": f"{value}"},
                    ],
                }
            )

        return elements

    def _get_color_by_priority(self, priority: Priority) -> str:
        if priority == Priority.P1:
            return "#ff0000"
        elif priority == Priority.P2:
            return "#ff7214"
        elif priority == Priority.P3:
            return "#ffa603"
        elif priority == Priority.P4:
            return "#ffc400"
        elif priority == Priority.P5:
            return "#ffc400"

    def _get_color_by_status(self, status: AlertStatus) -> str:
        if status == AlertStatus.OPEN:
            return "#ffd479"
        elif status == AlertStatus.ACKED:
            return "#ffd479"
        elif status == AlertStatus.CLOSED:
            return "#009051"
        elif status == AlertStatus.SNOOZED:
            return "#d6d6d6"

    def _generate_test_message(self, *, modifier: str | None = None) -> str:
        payload = {
            "attachments": [
                {
                    "color": "#ffd479",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"Test message from ZCP Alert Manager. Sent by : {modifier}",
                            },
                        }
                    ],
                }
            ]
        }

        log.debug(f"Converted payload: {json.dumps(payload, indent=2)}")

        return json.dumps(payload)
