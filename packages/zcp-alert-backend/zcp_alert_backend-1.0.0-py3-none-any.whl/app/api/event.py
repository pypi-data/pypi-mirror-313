import logging

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.auth.oauth2_keycloak import get_current_user
from app.event.event_handler import consume_alert_event
from app.model.auth_model import TokenData
from app.service.alert_service import AlertService

log = logging.getLogger("appLogger")

router = APIRouter()

_service = AlertService()


@router.get("/events/join/{client_id}", summary="Request to join the event stream")
async def sse_endpoint(
    client_id: str,
    oauth_user: TokenData = Depends(get_current_user),
) -> StreamingResponse:
    """A restful API to join the event stream for receiving alert events thru Server-Sent Events

    Regarding the user notification settings,

    if the user notification settings of the logged in user exists, it will be used to filter the alert events.
    Otherwise, the default user notification settings will be used to filter the alert events.

    The default user notification settings has the following default values:
    - username: logged in user name
    - priorities: [P1, P2, P3]

    Parameters
    ----------
    client_id : str
        the unique client id

    Returns
    -------
    StreamingResponse
    ```json
        msg = {
            'id': id,
            'status': status,
            'priority': priority,
            'severity': severity,
            'cluster': cluster,
            'repeated_count': repeated_count,
            'alertname': alertname,
            'summary': summary,
            'description': description,
            'updated_at': updated_at,
        }
    ```

    Examples
    -------
    ```javascript
    const UUID = Math.floor(Math.random() * 1000);
    const newUUID = uuidv4();
    const eventSource = new EventSource(`https://api.ags.cloudzcp.net/api/alert/v1/events/join/${newUUID}`);

    eventSource.onmessage = function(event) {
        console.log(event);
        const data = JSON.parse(event.data);
        console.log(data);

        for (let i = 0; i < data.length; i++) {
            const message = document.createElement("p");
            message.textContent = `[${data[i].updated_at}](${data[i].status}:${data[i].priority}) ${data[i].id} ${data[i].repeated_count}times repeated ${data[i].summary} - ${data[i].description}`;
            document.getElementById("messages").appendChild(message);
        }
    };
    ```
    """
    user_notification_settings = _service.get_user_notification_settins(
        oauth_user.username
    )
    return StreamingResponse(
        consume_alert_event(client_id, user_notification_settings),
        media_type="text/event-stream",
    )
