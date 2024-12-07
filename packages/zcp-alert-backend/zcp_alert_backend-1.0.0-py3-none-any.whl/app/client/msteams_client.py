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
    MSTEAMS_ACTION_ENABLED,
    OPEN_API_ACTION_URL,
    WEBHOOK_DEFAULT_TIMEOUT,
)

# _DISPLAY_TIMEZONE = DEFAULT_TIME_ZONE
_DISPLAY_TIMEZONE = ZoneInfo("Asia/Seoul")

log = logging.getLogger("appLogger")


class MSTeamsClient(HTTPBaseClient):
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
        Convert ZcpAlert to the ms teams message for user actions
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

        payload = {
            "text": f"**{subject}** the alert (#{alert.id}) "
            f"{snoozed_info} "
            f"by {modifier}<br>"
            f"[{description}]({ALERT_VIEW_URL.format(alert_id=alert.id)})"
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
            f"by {modifier}<br>"
            f"[{description}]({ALERT_VIEW_URL.format(alert_id=alert.id)})"
        }

        log.debug(f"Converted payload: {json.dumps(payload, indent=2)}")

        return json.dumps(payload)

    def _convert_to_massage_for_new(self, *, alert: ZcpAlert) -> str:
        """
        Convert ZcpAlert to the ms teams message for new alert

        https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL%2Ctext1#send-a-message-through-incoming-webhook-or-connector-for-microsoft-365-groups
        """
        priority_for_color = (
            alert.labels["priority"] if alert.labels.get("priority") else Priority.P5
        )

        message_card = {}
        message_card["@type"] = "MessageCard"
        message_card["@context"] = "http://schema.org/extensions"
        message_card["themeColor"] = self._get_color_by_priority(priority_for_color)
        message_card["summary"] = f"[{alert.status.value}] {alert.annotations['summary']
            if alert.annotations.get('summary')
            else 'N/A'}"
        message_card["sections"] = self._get_sections(alert=alert)
        message_card["potentialAction"] = self._get_action_buttons(alert=alert)

        log.debug(f"Converted payload: {json.dumps(message_card, indent=2)}")

        return json.dumps(message_card)

    def _get_action_buttons(self, *, alert: ZcpAlert) -> List[Dict[str, Any]]:
        actions = []
        action_button_detail = {}
        action_button_detail["@type"] = "OpenUri"
        action_button_detail["name"] = "Go to Alert"
        action_button_detail["targets"] = [
            {"os": "default", "uri": f"{ALERT_VIEW_URL.format(alert_id=alert.id)}"}
        ]
        actions.append(action_button_detail)

        if MSTEAMS_ACTION_ENABLED:
            # Acknowledge action button
            action_button_ack = {}
            action_button_ack["@type"] = "ActionCard"
            action_button_ack["name"] = "Acknowledge"
            action_button_ack["inputs"] = [
                {
                    "@type": "TextInput",
                    "id": "modifier",
                    "isMultiline": False,
                    "title": "Input your id or name",
                }
            ]
            action_button_ack["actions"] = [
                {
                    "@type": "HttpPOST",
                    "name": "Acknowledge",
                    "target": f"{OPEN_API_ACTION_URL.format(alert_id=alert.id, action=Action.ACK.value)}",
                }
            ]
            actions.append(action_button_ack)

            # Snooze action button
            action_button_snooze = {}
            action_button_snooze["@type"] = "ActionCard"
            action_button_snooze["name"] = "Snooze"
            action_button_snooze["inputs"] = [
                {
                    "@type": "TextInput",
                    "id": "modifier",
                    "isMultiline": False,
                    "title": "Input your id or name",
                },
                {
                    "@type": "TextInput",
                    "id": "snooze_until_at",
                    "isMultiline": False,
                    "title": "Input the snooze time in ISO format(e.g. 2024-07-05T14:48)",
                },
            ]
            action_button_snooze["actions"] = [
                {
                    "@type": "HttpPOST",
                    "name": "Snooze",
                    "target": f"{OPEN_API_ACTION_URL.format(alert_id=alert.id, action=Action.SNOOZE.value)}",
                }
            ]
            actions.append(action_button_snooze)

            # Close action button
            action_button_close = {}
            action_button_close["@type"] = "ActionCard"
            action_button_close["name"] = "Close"
            action_button_close["inputs"] = [
                {
                    "@type": "TextInput",
                    "id": "modifier",
                    "isMultiline": False,
                    "title": "Input your id or name",
                }
            ]
            action_button_close["actions"] = [
                {
                    "@type": "HttpPOST",
                    "name": "Close",
                    "target": f"{OPEN_API_ACTION_URL.format(alert_id=alert.id, action=Action.CLOSE.value)}",
                }
            ]
            actions.append(action_button_close)

        return actions

    def _get_sections(self, *, alert: ZcpAlert) -> Dict[str, Any]:
        sections = []
        section = {}
        section[
            "activityTitle"
        ] = f"[{alert.status.value}] {alert.annotations['summary']
            if alert.annotations.get('summary')
            else 'N/A'}"
        section["activitySubtitle"] = (
            f"[{alert.annotations['description']}]({ALERT_VIEW_URL.format(alert_id=alert.id)})"
            if alert.annotations.get("description")
            else "N/A"
        )
        section["activityImage"] = (
            "https://fonts.gstatic.com/s/e/notoemoji/15.1/1f6a8/512.png=s60"
        )
        section["facts"] = self._get_facts(alert=alert)
        section["markdown"] = True

        sections.append(section)

        return sections

    def _get_facts(self, *, alert: ZcpAlert) -> List[Dict[str, Any]]:
        facts = []
        facts.append(
            {
                "name": "Priority",
                "value": alert.labels["priority"]
                if alert.labels.get("priority")
                else "N/A",
            }
        )
        facts.append(
            {
                "name": "Severity",
                "value": alert.labels["severity"]
                if alert.labels.get("severity")
                else "N/A",
            }
        )
        facts.append(
            {
                "name": "Cluster",
                "value": alert.labels["cluster"]
                if alert.labels.get("cluster")
                else "N/A",
            }
        )
        facts.append(
            {
                "name": "Namespace",
                "value": alert.labels["namespace"]
                if alert.labels.get("namespace")
                else "N/A",
            }
        )
        facts.append(
            {
                "name": "Occured At",
                "value": f"{alert.starts_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds') if alert.starts_at else 'N/A'} ",  # if doesn't have space, teams will not render the timezone in iso format
            }
        )
        facts.append(
            {
                "name": "Triggered At",
                "value": f"{alert.created_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds') if alert.created_at else 'N/A'} ",
            }
        )
        facts.append(
            {"name": "Sender", "value": alert.sender.value if alert.sender else "N/A"}
        )
        facts.append({"name": "ID", "value": alert.id})

        return facts

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

    def _generate_test_message(self, *, modifier: str | None = None) -> str:
        payload = {"text": f"Test message from ZCP Alert Manager. Sent by : {modifier}"}

        log.debug(f"Converted payload: {json.dumps(payload, indent=2)}")

        return json.dumps(payload)
