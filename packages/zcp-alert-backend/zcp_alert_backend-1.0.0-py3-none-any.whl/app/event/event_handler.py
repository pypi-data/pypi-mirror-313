import asyncio
import json
import logging
from typing import Dict, List

from app.model import ZcpAlert
from app.model.user_notification_settings import UserNotificationSettings

log = logging.getLogger("appLogger")

clients: Dict[str, Dict] = {}

QUEUE_KEY = "queue"
SETTINGS_KEY = "settings"


async def publish_alert_event(alerts: List[ZcpAlert]):
    if not clients:
        log.debug("No client to send event")
        return

    for client_id, client_dict in clients.items():
        log.debug(f"Adding event to client[{client_id}]'s queue: {len(alerts)} alerts")

        client_queue: asyncio.Queue = client_dict[QUEUE_KEY]
        client_notification_settings: UserNotificationSettings = client_dict[
            SETTINGS_KEY
        ]
        client_matched_alerts = [
            alert for alert in alerts if client_notification_settings.is_match(alert)
        ]

        if len(client_matched_alerts) > 0:
            await client_queue.put(client_matched_alerts)


async def consume_alert_event(
    client_id: str, user_notification_settings: UserNotificationSettings
):
    if client_id not in clients:
        client_queue = asyncio.Queue()
        clients[client_id] = {
            QUEUE_KEY: client_queue,
            SETTINGS_KEY: user_notification_settings,
        }
        log.debug(
            f"Added new client queue for client[{client_id}]. Total clients: {len(clients)}"
        )

    try:
        while True:
            alerts: List[ZcpAlert] = await client_queue.get()

            log.debug(f"Consume event from client[{client_id}]'s queue: {len(alerts)}")

            event_data = []

            for alert in alerts:
                data = {
                    "id": alert.id,
                    "status": alert.status.value,
                    "priority": alert.labels.get("priority", ""),
                    "severity": alert.labels.get("severity", ""),
                    "cluster": alert.labels.get("cluster", ""),
                    "repeated_count": alert.repeated_count,
                    "alertname": alert.labels.get("alertname", ""),
                    "summary": alert.annotations.get("summary", ""),
                    "description": alert.annotations.get("description", ""),
                    "updated_at": alert.updated_at.isoformat(timespec="milliseconds"),
                }

                event_data.append(data)

            yield f"data: {json.dumps(event_data)}\n\n"
            # event_queue.task_done()
    finally:
        del clients[client_id]
        log.debug(
            f"Removed client queue for client[{client_id}]. Total clients: {len(clients)}"
        )
