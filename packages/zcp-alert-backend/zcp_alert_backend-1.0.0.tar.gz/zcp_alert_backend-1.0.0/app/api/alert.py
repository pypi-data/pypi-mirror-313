import asyncio
import logging
import uuid
from datetime import datetime
from functools import partial
from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse

from app import settings
from app.auth.basic_auth import BasicAuthUser, get_current_user_for_basicauth
from app.auth.oauth2_keycloak import TokenData, get_current_user
from app.exception.common_exception import AlertBackendException, AlertError
from app.model.alert_model import (
    Action,
    Alert,
    AlertData,
    AlertSortField,
    AlertStatus,
    Priority,
    RepeatedCountOperator,
    Sender,
    Severity,
    Status,
    ZcpAlert,
)
from app.schema.alert_request_model import (
    AlertActionRequest,
    AlertSearchRequest,
    TestAlertCreateRequest,
)
from app.schema.list_model import ActivityList, ZcpAlertList
from app.schema.response_model import ResponseModel
from app.service.alert_service import AlertService
from app.thread.threadpool_executor import get_executor
from app.utils.list_utils import (
    ACTIVITY_DEFAULT_PAGE_SIZE,
    DEFAULT_PAGE_NUMBER,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
    SortDirection,
)
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")

router = APIRouter()

__service = AlertService()

# executor = ThreadPoolExecutor(max_workers=settings.MAX_THREAD_COUNT)
__executor = get_executor()

_mandatory_annotations_fields = (
    settings.MANDATORY_FIELDS_ANNOTATIONS
)  # ['summary', 'description']
_mandatory_labels_fields = settings.MANDATORY_FIELDS_LABELS  # ['severity', 'priority']


@router.get(
    "/alerts",
    summary="Get alerts",
    response_class=JSONResponse,
    response_model=ZcpAlertList,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_alerts(
    statuses: list[AlertStatus] = Query(
        None, title="alert status", description="Search query string for status"
    ),
    senders: list[Sender] = Query(
        None, title="alert sender", description="Search query string for sender"
    ),
    priorities: list[Priority] = Query(
        None,
        title="alert priority",
        description="Search query string for alert priority",
    ),
    severities: list[Severity] = Query(
        None,
        title="alert severity",
        description="Search query string for alert severity",
    ),
    fingerprint: Optional[str] = Query(
        None,
        max_length=36,
        title="alert fingerprint",
        description="Search query string for fingerprint. The max length is 36",
    ),
    alert_id: Optional[str] = Query(
        None,
        max_length=100,
        title="alert id",
        description="Search query string for fingerprint. The max length is 100",
    ),
    repeated_count: Optional[int] = Query(
        None,
        le=10000,
        title="alert repeated count",
        description="Search query string for repeated count, Should be less than 10000",
    ),
    repeated_count_operator: RepeatedCountOperator = Query(
        RepeatedCountOperator.GTE,
        title="alert repeated count operator",
        description="Search query string for repeated count operator",
    ),
    alertname: Optional[str] = Query(
        None,
        max_length=100,
        title="alert name",
        description="Search query string for alert name. The max length is 100",
    ),
    description: Optional[str] = Query(
        None,
        max_length=100,
        title="alert description",
        description="Search query string for alert description. The max length is 100",
    ),
    summary: Optional[str] = Query(
        None,
        max_length=100,
        title="alert summary",
        description="Search query string for alert summary. The max length is 100",
    ),
    project: Optional[str] = Query(
        None,
        max_length=100,
        title="alert project",
        description="Search query string for alert project. The max length is 100",
    ),
    clusters: list[str] = Query(
        None,
        title="alert clusters",
        description="Search query string for alert clusters",
    ),
    namespaces: list[str] = Query(
        None,
        title="alert namespaces",
        description="Search query string for alert namespaces",
    ),
    start_date: Optional[str] = Query(
        None,
        title="search start date",
        description="Search query string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    end_date: Optional[str] = Query(
        None,
        title="search end date",
        description="Search query string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    start_date_created_at: Optional[str] = Query(
        None,
        title="search start date",
        description="Search query string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    end_date_created_at: Optional[str] = Query(
        None,
        title="search end date",
        description="Search query string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    start_date_closed_at: Optional[str] = Query(
        None,
        title="search start date",
        description="Search query string for start date (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    end_date_closed_at: Optional[str] = Query(
        None,
        title="search end date",
        description="Search query string for end date (ISO 8601 format(e.g. 2024-11-06T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    labels: list[str] = Query(
        None,
        title="search labels",
        description="Search query string for labels e.g. severity:critical,priority:P1",
    ),
    sort_field: AlertSortField = Query(
        AlertSortField.UPDATED_AT, title="sort field", description="Sort field name"
    ),
    sort_direction: SortDirection = Query(
        SortDirection.DESC, title="sort direction", description="Sort direction"
    ),
    page_number: Optional[int] = Query(
        DEFAULT_PAGE_NUMBER,
        ge=DEFAULT_PAGE_NUMBER,
        title="page number",
        description=f"Page number. Default is {DEFAULT_PAGE_NUMBER} and it should be greater than 0",
    ),
    page_size: Optional[int] = Query(
        DEFAULT_PAGE_SIZE,
        ge=DEFAULT_PAGE_SIZE,
        le=MAX_PAGE_SIZE,
        title="page size",
        description=f"Page size. Default is {DEFAULT_PAGE_SIZE} and it should be greater than 10 and less than {MAX_PAGE_SIZE}",
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> ZcpAlertList:
    """The restful API to get alerts"""

    # convert the string to datetime in the default timezone(UTC)
    log.debug(f"Original : start_date: {start_date}, end_date: {end_date}")

    start_date = (
        datetime.fromisoformat(start_date).astimezone(DEFAULT_TIME_ZONE)  # .isoformat()
        if start_date
        else start_date
    )
    end_date = (
        datetime.fromisoformat(end_date).astimezone(DEFAULT_TIME_ZONE)  # .isoformat()
        if end_date
        else end_date
    )

    start_date_created_at = (
        datetime.fromisoformat(start_date_created_at).astimezone(
            DEFAULT_TIME_ZONE
        )  # .isoformat()
        if start_date_created_at
        else start_date_created_at
    )
    end_date_created_at = (
        datetime.fromisoformat(end_date_created_at).astimezone(
            DEFAULT_TIME_ZONE
        )  # .isoformat()
        if end_date_created_at
        else end_date_created_at
    )

    start_date_closed_at = (
        datetime.fromisoformat(start_date_closed_at).astimezone(
            DEFAULT_TIME_ZONE
        )  # .isoformat()
        if start_date_closed_at
        else start_date_closed_at
    )
    end_date_closed_at = (
        datetime.fromisoformat(end_date_closed_at).astimezone(
            DEFAULT_TIME_ZONE
        )  # .isoformat()
        if end_date_closed_at
        else end_date_closed_at
    )

    log.debug(f"Converted : start_date: {start_date}, end_date: {end_date}")

    alert_search_request = AlertSearchRequest(
        statuses=statuses,
        senders=senders,
        fingerprint=fingerprint,
        alert_id=alert_id,
        repeated_count=repeated_count,
        repeated_count_operator=repeated_count_operator,
        alertname=alertname,
        description=description,
        summary=summary,
        project=project,
        clusters=clusters,
        namespaces=namespaces,
        priorities=priorities,
        severities=severities,
        start_date=start_date,
        end_date=end_date,
        start_date_created_at=start_date_created_at,
        end_date_created_at=end_date_created_at,
        start_date_closed_at=start_date_closed_at,
        end_date_closed_at=end_date_closed_at,
        labels=labels,
        sort_field=sort_field,
        sort_direction=sort_direction,
    )

    loop = asyncio.get_event_loop()

    list_partial = partial(
        __service.get_alerts,
        alert_search_request=alert_search_request,
        page_number=page_number,
        page_size=page_size,
    )
    data = await loop.run_in_executor(__executor, list_partial)

    count_partial = partial(
        __service.get_alerts_count, alert_search_request=alert_search_request
    )
    total = await loop.run_in_executor(__executor, count_partial)

    return ZcpAlertList(
        current_page=page_number, page_size=page_size, total=total, data=data
    )


async def _alert_webhook_process(alerts: List[Alert]):
    for alert in alerts:
        for field in _mandatory_annotations_fields:
            if not alert.annotations.get(field):
                raise AlertBackendException(
                    AlertError.BAD_REQUEST, details=f"Annotation {field} is required"
                )
        for field in _mandatory_labels_fields:
            if not alert.labels.get(field):
                raise AlertBackendException(
                    AlertError.BAD_REQUEST, details=f"Label {field} is required"
                )

    loop = asyncio.get_event_loop()

    zcp_alerts = await loop.run_in_executor(
        __executor, __service.alert_webhook_process, alerts
    )

    # push the alerts to the notification service
    await __service.push_alert_event(zcp_alerts)

    return ResponseModel(data={"processed_alert_count": len(zcp_alerts)})


@router.post(
    "/alerts/webhook",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_exclude_none=True,
)
@router.post(
    "/alerts/external/webhook",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def alerts_webhook(
    alert_data: AlertData,
    basic_user: BasicAuthUser = Depends(get_current_user_for_basicauth),
) -> ResponseModel:
    """A restful API to process the alerts from the prometheus alertmanager

    Parameters
    ----------
    alert_data : AlertData
        It comes from the prometheus alertmanager

    Returns
    -------
    ResponseModel
        Returns the processed alert count like following
    ```json
    {
        "result": "success",
        "data": [
            {
            "id": "66e591801659d83e105a3c4a"
            },
            {
            "id": "66e591801659d83e105a3c4c"
            },
            {
            "id": "66e591801659d83e105a3c4e"
            },
            {
            "id": "66e591801659d83e105a3c50"
            }
        ]
    }
    ```

    Raises
    ------
    AlertBackendException
    """
    # alert-backend process only the alerts of the AlertData
    alerts = alert_data.alerts

    if alerts is None:
        raise AlertBackendException(
            AlertError.BAD_REQUEST, details="Alerts is required"
        )

    for alert in alerts:
        for field in _mandatory_annotations_fields:
            if not alert.annotations.get(field):
                raise AlertBackendException(
                    AlertError.BAD_REQUEST, details=f"Annotation {field} is required"
                )
        for field in _mandatory_labels_fields:
            if not alert.labels.get(field):
                raise AlertBackendException(
                    AlertError.BAD_REQUEST, details=f"Label {field} is required"
                )

    loop = asyncio.get_event_loop()

    zcp_alerts = await loop.run_in_executor(
        __executor, __service.alert_webhook_process, alerts
    )

    # push the alerts to the notification service
    await __service.push_alert_event(zcp_alerts)

    return ResponseModel(data=[za.model_dump(include="id") for za in zcp_alerts])


@router.post(
    "/alerts/single/webhook",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def alerts_single_webhook(
    alert: Alert, basic_user: BasicAuthUser = Depends(get_current_user_for_basicauth)
) -> ResponseModel:
    """A restful API to process a single alert from the K8sWatcher or the OpenSearch

    Parameters
    ----------
    alert : Alert
        It comes from the K8sWatcher or the OpenSearch

    Returns
    -------
    ResponseModel
        Returns the processed alert count like following
    ```json
    {
        "result": "success",
        "data": [
            {
            "id": "66e591801659d83e105a3c4a"
            },
            {
            "id": "66e591801659d83e105a3c4c"
            },
            {
            "id": "66e591801659d83e105a3c4e"
            },
            {
            "id": "66e591801659d83e105a3c50"
            }
        ]
    }
    ```

    Raises
    ------
    AlertBackendException
    """
    # alert-backend process only the alerts of the AlertData
    for field in _mandatory_annotations_fields:
        if not alert.annotations.get(field):
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details=f"Annotation {field} is required"
            )
    for field in _mandatory_labels_fields:
        if not alert.labels.get(field):
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details=f"Label {field} is required"
            )

    loop = asyncio.get_event_loop()

    zcp_alerts = await loop.run_in_executor(
        __executor, __service.alert_webhook_process, [alert]
    )

    # push the alerts to the notification service
    await __service.push_alert_event(zcp_alerts)

    return ResponseModel(data=[za.model_dump(include="id") for za in zcp_alerts])


@router.post(
    "/alerts",
    summary="Create alert for notification testing",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def create_test_alert(
    alert_create_request: TestAlertCreateRequest,
    token_data: TokenData = Depends(get_current_user),
) -> ResponseModel:
    """A restful API to create an alert for notification testing

    Parameters
    ----------
    alert : Alert
        It comes from the alert backend console on the web

    Returns
    -------
    ResponseModel
        Returns the processed alert count like following
    ```json
    {
        "result": "success"
    }
    ```

    Raises
    ------
    AlertBackendException
    """
    _annotations = {}
    _annotations.update({"description": alert_create_request.description})
    _annotations.update({"summary": alert_create_request.summary})

    _labels = alert_create_request.labels
    _labels.update({"alertname": alert_create_request.alertname})
    _labels.update({"priority": alert_create_request.priority})
    _labels.update({"severity": alert_create_request.severity})

    alert = Alert(
        status=Status.FIRING,
        labels=_labels,
        annotations=_annotations,
        fingerprint=str(uuid.uuid4()),
        startsAt=datetime.now().astimezone(DEFAULT_TIME_ZONE),
        endsAt=datetime.now().astimezone(DEFAULT_TIME_ZONE),
    )

    for field in _mandatory_annotations_fields:
        if not alert.annotations.get(field):
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details=f"Annotation {field} is required"
            )
    for field in _mandatory_labels_fields:
        if not alert.labels.get(field):
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details=f"Label {field} is required"
            )

    return ResponseModel(
        data={"result": "success" if __service.create_alert(alert) else "failed"}
    )


def validate_bulk_action(action: Action):
    if action in [Action.SNOOZE, Action.UNACK, Action.WAKEUP]:
        raise AlertBackendException(
            AlertError.BAD_REQUEST, details=f"Action {action.value} is not allowed"
        )
    return action


def validate_single_action(action: Action):
    if action in [Action.WAKEUP]:
        raise AlertBackendException(
            AlertError.BAD_REQUEST, details=f"Action {action.value} is not allowed"
        )
    return action


@router.patch(
    "/alerts/bulk/{action}",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_exclude_none=True,
)
async def alerts_bulk_action(
    alerts: List[AlertActionRequest],
    action: Action = Depends(validate_bulk_action),
    oauth_user: TokenData = Depends(get_current_user),
) -> ResponseModel:
    """The restful API to perform actions on alerts

    Parameters
    ----------
    alerts : List[AlertActionRequest]
        list of AlertActionRequest instances

    action : Action
        Action enum. Snooze, Unack, Wakeup are not allowed

    Returns
    -------
    ResponseModel
        Returns the processed alert count like following
    ```json
    {
        "result": "success",
        "data": {
            "updated_count": 1
        }
    }
    ```
    """
    updated_count = __service.patch_bulk_alerts_status(
        alerts=alerts, action=action, modifier=oauth_user.username
    )

    return ResponseModel(data={"updated_count": updated_count})


@router.patch(
    "/alerts/{alert_id}/{action}",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_exclude_none=True,
    summary="Alert single action on the web console by system administator",
)
async def alert_single_action(
    alert_id: str = Path(title="Alert id", description="Alert id"),
    action: Action = Path(title="Action", description="Action enum"),
    # action: Action=Depends(validate_single_action),
    # snoozed_until_at: Optional[str] = Query(None, title="Snoozed time", description="Snoozed time (ISO 8601 format(e.g. 2023-07-05T14:48))", pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"),
    snoozed_until_at: Optional[str] = Query(
        None,
        title="Snoozed time",
        description="Snoozed time (ISO 8601 format(e.g. 2024-11-05T14:48:00.000+09:00))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}$",
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> ResponseModel:
    """The restful API to perform an action on an alert

    Parameters
    ----------
    alert_id : str
        by default Path(..., title="Alert id", description="Alert id")

    action : Action
        by default Path(title="Action", description="Action enum").
        Wakeup is not allowed

    snoozed_until_at : _type_, optional
        by default Query(None, title="Snoozed time",
        description="Snoozed time (ISO 8601 format(e.g. 2023-07-05T14:48))"

    oauth_user : TokenData
        by default Depends(get_current_user)

    Returns
    -------
    ResponseModel
        returns a response model like following
    ```json
    {
        "result": "success"
    }
    ```
    """
    snoozed_until_at = (
        datetime.fromisoformat(snoozed_until_at).astimezone(DEFAULT_TIME_ZONE)
        if snoozed_until_at
        else snoozed_until_at
    )
    __service.patch_single_alert_status(
        alert_id=alert_id,
        action=action,
        modifier=oauth_user.username,
        snoozed_until_at=snoozed_until_at,
    )
    return ResponseModel()


@router.post(
    "/alerts/external/{alert_id}/{action}/{username}",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_exclude_none=True,
    summary="Alert single action by the third party services. e.g. slack, google chat, etc.",
)
async def alert_external_single_action(
    alert_id: str = Path(..., title="Alert id", description="Alert id"),
    action: Action = Path(title="Action", description="Action enum"),
    snoozed_until_at: Optional[str] = Query(
        None,
        title="Snoozed time",
        description="Snoozed time (ISO 8601 format(e.g. 2023-07-05T14:48))",
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$",
    ),
    username: str = Path(..., title="Username", description="Username", max_length=30),
) -> ResponseModel:
    """The restful API to perform an action on an alert from the third party services on the public network

    Parameters
    ----------
    alert_id : str, optional
    action : Action, optional
    snoozed_until_at : _type_, optional

    Returns
    -------
    ResponseModel

    Raises
    ------
    AlertBackendException
    """
    snoozed_until_at = (
        datetime.fromisoformat(snoozed_until_at).astimezone(DEFAULT_TIME_ZONE)
        if snoozed_until_at
        else snoozed_until_at
    )
    __service.patch_single_alert_status(
        alert_id=alert_id,
        action=action,
        modifier=username,
        snoozed_until_at=snoozed_until_at,
    )
    return ResponseModel()


@router.get(
    "/alerts/{alert_id}",
    response_class=JSONResponse,
    response_model=ZcpAlert,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_alert(
    alert_id: str = Path(title="Alert id", description="Alert id", max_length=36),
    oauth_user: TokenData = Depends(get_current_user),
) -> ZcpAlert:
    """The restful API to get an alert by alert id

    Parameters
    ----------
    alert_id : str, optional
        by default Path(title="Alert id", description="Alert id", max_length=36)

    Returns
    -------
    ZcpAlert
    """
    # return ResponseModel(data=__service.get_alert(alert_id))
    return __service.get_alert(alert_id)


@router.get(
    "/alerts/{alert_id}/activities",
    summary="Get activities for an alert",
    response_class=JSONResponse,
    response_model=ActivityList,
    response_model_by_alias=False,
    response_model_exclude_none=False,
)
async def get_activities(
    alert_id: str = Path(title="Alert id", description="Alert id", max_length=36),
    page_number: Optional[int] = Query(
        DEFAULT_PAGE_NUMBER,
        ge=DEFAULT_PAGE_NUMBER,
        title="page number",
        description=f"Page number. Default is {DEFAULT_PAGE_NUMBER} and it should be greater than 0",
    ),
    page_size: Optional[int] = Query(
        ACTIVITY_DEFAULT_PAGE_SIZE,
        ge=ACTIVITY_DEFAULT_PAGE_SIZE,
        le=MAX_PAGE_SIZE,
        title="page size",
        description=f"Page size. Default is {ACTIVITY_DEFAULT_PAGE_SIZE} and it should be greater than 10 and less than {MAX_PAGE_SIZE}",
    ),
    oauth_user: TokenData = Depends(get_current_user),
) -> ActivityList:
    """_summary_

    Returns
    -------
    _type_
        _description_

    Raises
    ------
    AlertBackendException
        _description_
    """
    return ActivityList(
        current_page=page_number,
        page_size=page_size,
        total=__service.get_activities_count(alert_id=alert_id),
        data=__service.get_activities(
            alert_id=alert_id, page_number=page_number, page_size=page_size
        ),
    )


@router.delete(
    "/alerts/{alert_id}",
    response_class=JSONResponse,
    response_model=ResponseModel,
    response_model_exclude_none=True,
)
async def remove_alert(
    alert_id: str = Path(title="Alert id", description="Alert id", max_length=36),
    oauth_user: TokenData = Depends(get_current_user),
) -> ResponseModel:
    """The restful API to delete an alert by alert id

    Parameters
    ----------
    alert_id : str, optional
        by default Path(title="Alert id", description="Alert id", max_length=36)

    Returns
    -------
    ResponseModel
        Returns the processed alert count like following
    ```json
    {
        "result": "success"
    }
    ```

    Raises
    ------
    AlertBackendException
    """
    if oauth_user.is_alert_admin() or oauth_user.is_platform_admin():
        __service.remove_alert(alert_id)
        return ResponseModel()

    raise AlertBackendException(
        AlertError.PERMISSION_DENIED,
        details="You don't have permission to delete this resource",
    )


@router.get(
    "/alert/priorities",
    summary="Get priorites for alerts",
    response_class=JSONResponse,
    response_model=List[Priority],
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def get_priorities() -> List[Priority]:
    """The restful API to get priorities for alerts

    Returns
    -------
    List[Priority]
    """
    return __service.get_priorities()


@router.get(
    "/alert/severities",
    summary="Get severities for alerts",
    response_class=JSONResponse,
    response_model=List[Severity],
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def get_severities() -> List[Severity]:
    """The restful API to get severities for alerts

    Returns
    -------
    List[Severity]
    """
    return __service.get_severities()


@router.get(
    "/alert/senders",
    summary="Get senders for alerts",
    response_class=JSONResponse,
    response_model=List[Sender],
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def get_senders() -> List[Sender]:
    """The restful API to get senders for alerts

    Returns
    -------
    List[Sender]
    """
    return __service.get_senders()


@router.get(
    "/alert/actions",
    summary="Get actions for alerts",
    response_class=JSONResponse,
    response_model=List[Action],
    response_model_by_alias=False,
    response_model_exclude_none=True,
)
async def get_actions() -> List[Action]:
    """The restful API to get actions for alerts

    Returns
    -------
    List[Action]
    """
    return __service.get_actions()
