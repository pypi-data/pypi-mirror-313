import logging
import time
import uuid
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from bson import ObjectId
from bson.errors import InvalidId

from app import settings
from app.client import (
    GoogleChatClient,
    KakaoTalkClient,
    MSTeamsClient,
    SlackClient,
    WebhookClient,
)
from app.client.email_client import EmailClient
from app.db import (
    ActivityRepository,
    AlertRepository,
    BasicAuthUserRepository,
    ChannelRepository,
    IntegrationRepository,
    KakaoTaklTokenRepository,
    SilenceRepository,
)
from app.db.exceptions import InvalidObjectIDException, ObjectNotFoundException
from app.db.user_notification_settings_repository import (
    UserNotificationSettingsRepository,
)
from app.event.event_handler import publish_alert_event
from app.exception.common_exception import AlertBackendException, AlertError
from app.model.alert_model import (
    Action,
    Alert,
    AlertActivity,
    AlertStatus,
    Priority,
    Sender,
    Severity,
    ZcpAlert,
)
from app.model.auth_model import BasicAuthUser
from app.model.channel_model import (
    Channel,
    ChannelSortField,
    ChannelType,
    EmailChannel,
    GoogleChatChannel,
    KakaoTalkChannel,
    MSTeamsChannel,
    SlackChannel,
    WebhookChannel,
)
from app.model.integration_model import (
    Filter,
    FilterKey,
    FilterMode,
    FilterValueType,
    Integration,
    IntegrationStatus,
    Operator,
)
from app.model.kakaotalk_model import KakaoTalkFriend, KakaoTalkToken
from app.model.result_model import Result
from app.model.silence_model import Silence, SilenceSortField, SilenceStatus
from app.model.user_notification_settings import UserNotificationSettings
from app.schema.alert_request_model import AlertActionRequest, AlertSearchRequest
from app.thread.threadpool_executor import get_executor
from app.utils.list_utils import SortDirection
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")


class AlertService:
    """AlertService class to handle alert service

    Naming convention:
    - get_{model}s: get model list
    - get_{model}: get model
    - create_{model}: create model
    - modify_{model}: update model
    - remove_{model}: delete model
    - patch_{model}_{field}: patch field of model
    - patch_{model}s_{field}: patch field of models
    """

    # for singleton pattern
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__initiated = False
        return cls.__instance

    def __init__(self):
        if self.__initiated:
            return

        self.__alert_repository = AlertRepository.from_config(
            collection=settings.MONGODB_COLLECTION_ALERT
        )
        self.__alert_repository()  # call the __call__ method to create the unique index

        self.__activity_repository = ActivityRepository.from_config(
            collection=settings.MONGODB_COLLECTION_ACTIVITY
        )

        self.__channel_repository = ChannelRepository.from_config(
            collection=settings.MONGODB_COLLECTION_CHANNEL
        )

        self.__integration_repository = (
            IntegrationRepository.from_config_with_aggregation(
                collection=settings.MONGODB_COLLECTION_INTEGRATION,
                aggregation_collection=settings.MONGODB_COLLECTION_CHANNEL,
            )
        )

        self.__silence_repository = SilenceRepository.from_config_with_aggregation(
            collection=settings.MONGODB_COLLECTION_SILENCE,
            aggregation_collection=settings.MONGODB_COLLECTION_INTEGRATION,
        )

        self.__kakaotalk_token_repository = KakaoTaklTokenRepository.from_config(
            collection=settings.MONGODB_COLLECTION_KAKAO_TOKEN
        )

        self.__basic_auth_user_repository = BasicAuthUserRepository.from_config(
            collection=settings.MONGODB_COLLECTION_BASIC_AUTH_USER
        )
        self.__basic_auth_user_repository()  # call the __call__ method to create the unique index

        self.__user_notification_settings_repository = (
            UserNotificationSettingsRepository.from_config(
                collection=settings.MONGODB_COLLECTION_USER_NOTIFICATION_SETTINGS
            )
        )
        self.__user_notification_settings_repository()  # call the __call__ method to create the unique index

        self.__initiated = True

        self.__cached_integrations__: Dict[str, Integration] = {}

        self.__executor = get_executor()

        log.info(f"{__name__} AlertService Initialized")

    def create_alert(self, alert: Alert) -> bool:
        """Create alert for testing

        Just send the alert event to the event handler
        """

        zcp_alert = ZcpAlert.from_alert(alert=alert)
        zcp_alert.id = str(uuid.uuid4())
        zcp_alert.created_at = datetime.now(DEFAULT_TIME_ZONE)

        # for sending the test notification
        # ----------------------------------------------------------------
        # Step 1.
        # find the integrations related to the for each alerts
        # and get the pairs of alert and integration
        alert_integration_pairs = self.__internal_process_step2(zcp_alerts=[zcp_alert])
        log.debug(f"Alert : Integration pair len : {len(alert_integration_pairs)}")

        # Step 2.
        # send the notification using the client
        # and the alert and integration pairs data
        self.__internal_process_step3(alert_integration_pairs=alert_integration_pairs)

        return True

    def get_alert(self, alert_id: str) -> ZcpAlert:
        """Get alert by alert_id

        Args:
            param alert_id: alert id mandatory

        Returns:
            ZcpAlert: alert object

        Raises:
            AlertBackendException: if the alert is not found
            AlertBackendException: if the alert id is invalid
        """
        if not alert_id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Alert id is required"
            )

        try:
            zcp_alert = self.__alert_repository.find_by_id(alert_id)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="alert", object_id=alert_id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        # activities = self.__activity_repository.find_all_by_alert_id(
        #     alert_id=alert_id,
        #     page_number=DEFAULT_PAGE_NUMBER,
        #     page_size=ACTIVITY_DEFAULT_PAGE_SIZE
        # )
        # if activities is not None and len(activities) > 0:
        #     zcp_alert.activities = activities

        return zcp_alert

    def get_activities(
        self, *, alert_id: str, page_number: Optional[int], page_size: Optional[int]
    ) -> List[AlertActivity]:
        """Get activities by alert_id

        Parameters
        ----------
        alert_id : str
        page_number : Optional[int]
        page_size : Optional[int]

        Returns
        -------
        List[AlertActivity]
        """
        return self.__activity_repository.find_all_by_alert_id(
            alert_id=alert_id, page_number=page_number, page_size=page_size
        )

    def get_activities_count(self, *, alert_id: str) -> int:
        """Get activities count by alert_id

        Parameters
        ----------
        alert_id : str

        Returns
        -------
        int
        """
        return self.__activity_repository.count_by_alert_id(alert_id=alert_id)

    def get_alerts(
        self,
        *,
        alert_search_request: Optional[AlertSearchRequest],
        page_number: Optional[int],
        page_size: Optional[int],
    ) -> List[ZcpAlert]:
        """Get alerts by query parameters

        Args:
            param alert_search_request: alert search request optional
            param page_number: page number optional
            param page_size: page size optional

        Returns:
            List[ZcpAlert]: list of alert objects
        """
        return self.__alert_repository.find(
            alert_search_request=alert_search_request,
            page_number=page_number,
            page_size=page_size,
        )

    def get_alerts_count(
        self, *, alert_search_request: Optional[AlertSearchRequest]
    ) -> int:
        """Get alerts count by query parameters

        Args:
            param alert_search_request: alert search request optional

        Returns:
            int: count of alerts
        """
        return self.__alert_repository.count(alert_search_request=alert_search_request)

    def patch_bulk_alerts_status(
        self, *, alerts: List[AlertActionRequest], action: Action, modifier: str
    ) -> int:
        """Patch alerts status (bulk action for multiple alerts)

        Args:
            param alerts: alert ids mandatory
            param action: alert action mandatory
            param modifier: modifier mandatory

        Returns:
            int: count of updated alerts

        Raises:
            AlertBackendException: if the alert is closed
            AlertBackendException: if the action is not allowed
        """
        if action in [Action.UNACK, Action.SNOOZE]:
            raise AlertBackendException(
                AlertError.BAD_REQUEST,
                details=f"Action {action.value} is not allowed for multiple alerts",
            )

        if action in [Action.WAKEUP]:
            if modifier != settings.WAKEUP_SCHEDULER_NAME:
                raise AlertBackendException(
                    AlertError.BAD_REQUEST,
                    details=f"Action {action.value} is only allowed for {settings.WAKEUP_SCHEDULER_NAME}",
                )

        if alerts is None or len(alerts) == 0:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Alerts are required"
            )

        # Step 1. Check if alert exists and current status
        for alert in alerts:
            if alert.asis_status == AlertStatus.CLOSED:
                raise AlertBackendException(
                    AlertError.BAD_REQUEST, details="Closed alert cannot be updated"
                )

        # Step 2. Set the tobe status based on the action
        tobe_status = action.get_tobe_status()
        if tobe_status is None:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details=f"Action {action.value} is not allowed"
            )

        for alert in alerts:
            if alert.asis_status.allow_action(action) is False:
                raise AlertBackendException(
                    AlertError.BAD_REQUEST,
                    details=f"Action {action.value} is not allowed for "
                    f"the current status {alert.asis_status.value}"
                    f" of the alert {alert.alert_id}",
                )

        # Step 3. update the status
        result_count = self.__alert_repository.update_status(
            alert_ids=[alert.alert_id for alert in alerts],
            status=tobe_status,
            modifier=modifier,
        )

        # Step 4. Insert activity log
        activities = []
        for alert in alerts:
            activities.append(
                AlertActivity(
                    alert_id=alert.alert_id,
                    action=action,
                    user=modifier,
                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                    description=[
                        f"Status: {alert.asis_status.value} -> {tobe_status.value}",
                        f"Modified by {modifier}",
                    ],
                )
            )

        self.__activity_repository.insert_many(activities)

        # for sending the notification
        # ----------------------------------------------------------------
        # Step 0. find the alerts by ids
        zcp_alerts = self.__alert_repository.find_by_ids(
            [alert.alert_id for alert in alerts]
        )

        # Step 1. find the integrations related to the for each alerts and get the pairs of alert and integration
        alert_integration_pairs = self.__internal_process_step2(
            action=action, zcp_alerts=zcp_alerts
        )
        log.debug(f"Alert : Integration pair len : {len(alert_integration_pairs)}")

        if alert_integration_pairs is not None and len(alert_integration_pairs) > 0:
            # Step 2. send the notification using the client and the alert and integration pairs data
            future = self.__executor.submit(
                self.__internal_process_step3,
                action=action,
                alert_integration_pairs=alert_integration_pairs,
                modifier=modifier,
            )
            log.debug(f"Future : {future}")
        else:
            log.debug("Alert : Integration pair is empty")

        return result_count

    def patch_single_alert_status(
        self,
        *,
        alert_id: str,
        action: Action,
        modifier: str,
        snoozed_until_at: datetime | None = None,
    ) -> bool:
        """Patch alert status (single action for single alert)

        Args:
            param alert_id: alert id mandatory
            param action: alert action mandatory
            param modifier: modifier mandatory
            param snoozed_until_at: snoozed until at optional

        Returns:
            bool: True if successful

        Raises:
            AlertBackendException: if the alert is closed
            AlertBackendException: if the action is not allowed
            AlertBackendException: if snoozed_until_at is required when snooze action
        """
        # Step 1. Check if alert exists and current status
        if not alert_id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Alert id is required"
            )

        try:
            exist_zcp_alert = self.__alert_repository.find_by_id(alert_id)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="alert", object_id=alert_id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        if exist_zcp_alert.status == AlertStatus.CLOSED:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Closed alert cannot be updated"
            )

        # Step 2. Set the tobe status based on the action
        tobe_status = action.get_tobe_status()

        if tobe_status is None:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details=f"Action {action.value} is not allowed"
            )

        # Step 3. check the transition of the status
        if exist_zcp_alert.status.allow_action(action) is False:
            raise AlertBackendException(
                AlertError.BAD_REQUEST,
                details=f"Action {action.value} is not allowed for "
                f"the current status {exist_zcp_alert.status.value}",
            )

        # Step 4. Check if snoozed_until_at is required when snooze action
        if tobe_status == AlertStatus.SNOOZED and snoozed_until_at is None:
            log.debug("Snoozed datetime is required for snooze action")
            raise AlertBackendException(
                AlertError.BAD_REQUEST,
                details="Snoozed datetime is required for snooze action",
            )
        # check if snoozed_until_at is in the future
        log.debug(
            f"Snoozed until at : {snoozed_until_at}, current datetime : {datetime.now(DEFAULT_TIME_ZONE) - timedelta(minutes=1)}"
        )
        if (
            tobe_status == AlertStatus.SNOOZED
            and snoozed_until_at is not None
            and snoozed_until_at
            < (datetime.now(DEFAULT_TIME_ZONE) - timedelta(minutes=1))
        ):
            log.debug("Snoozed datetime should be in the future")
            raise AlertBackendException(
                AlertError.BAD_REQUEST,
                details="Snoozed datetime should be in the future",
            )

        # Step 5. Update the status
        updated_zcp_alert = self.__alert_repository.update_status(
            alert_id=alert_id,
            status=tobe_status,
            modifier=modifier,
            snoozed_until_at=snoozed_until_at,
        )

        # Step 6. Insert activity log
        description = updated_zcp_alert.diff(before=exist_zcp_alert)
        description.append(f"Modified by {modifier}")
        activity = AlertActivity(
            alert_id=alert_id,
            action=action,
            user=modifier,
            created_at=datetime.now(DEFAULT_TIME_ZONE),
            description=description,
        )

        activity_object_id = self.__activity_repository.insert(activity)
        log.debug(f"Inserted activity : {str(activity_object_id)}")

        # for sending the notification
        # ----------------------------------------------------------------
        # Step 1. find the integrations related to the for each alerts and get the pairs of alert and integration
        alert_integration_pairs = self.__internal_process_step2(
            action=action, zcp_alerts=[updated_zcp_alert]
        )
        log.debug(f"Alert : Integration pair len : {len(alert_integration_pairs)}")

        if alert_integration_pairs is not None and len(alert_integration_pairs) > 0:
            # Step 2. send the notification using the client and the alert and integration pairs data
            # self.__internal_process_step3(
            #     action=action,
            #     alert_integration_pairs=alert_integration_pairs,
            #     modifier=modifier
            # )

            future = self.__executor.submit(
                self.__internal_process_step3,
                action=action,
                alert_integration_pairs=alert_integration_pairs,
                modifier=modifier,
            )

            log.debug(f"Future : {future}")
        else:
            log.debug("Alert : Integration pair is empty")

        return True

    def wake_up_alerts_snoozed_time_over(self, *, modifier: str) -> int:
        zcp_alerts = self.__alert_repository.find_by_snoozed_time_over()
        log.debug(f"Alerts snoozed time over count : {len(zcp_alerts)}")
        if len(zcp_alerts) > 0:
            alert_action_request = [
                AlertActionRequest(alert_id=alert.id, asis_status=alert.status)
                for alert in zcp_alerts
            ]
            self.patch_bulk_alerts_status(
                alerts=alert_action_request, action=Action.WAKEUP, modifier=modifier
            )
            return len(zcp_alerts)
        else:
            return 0

    def remove_alert(self, alert_id: str) -> bool:
        """Delete alert by alert_id

        Args:
            param alert_id: alert id mandatory

        Returns:
            bool: True if successful

        Raises:
            AlertBackendException: if the alert is not found
            AlertBackendException: if the alert id is invalid
        """

        if not alert_id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Alert id is required"
            )

        # Step 1. Remove all activities
        removed_activitiy_count = self.__activity_repository.delete_all_by_alert_id(
            alert_id
        )
        log.debug(f"Removed activities count : {removed_activitiy_count}")

        # Step 2. Remove the alert
        try:
            result = self.__alert_repository.delete_by_id(alert_id)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="alert", object_id=alert_id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        log.debug(f"Removed alert : {alert_id}")

        return result

    # async def process(self, alerts: List[Alert]) -> int:
    def alert_webhook_process(self, alerts: List[Alert]) -> List[ZcpAlert]:
        """Process alerts

        Args:
            param alerts: alert list mandatory

        Returns:
            int: count of zcp alerts
        """
        # Step 1.
        # check if alert exists or not and extract the zcp alerts
        zcp_alerts = self.__internal_process_step1(alerts)
        log.debug(f"ZcpAlerts len : {len(zcp_alerts)}")

        # Step 2.
        # find the integrations related to the for each alerts
        # and get the pairs of alert and integration
        alert_integration_pairs = self.__internal_process_step2(zcp_alerts=zcp_alerts)
        log.debug(f"Alert : Integration pair len : {len(alert_integration_pairs)}")

        # Step 3.
        # send the notification using the client
        # and the alert and integration pairs data
        if alert_integration_pairs is not None and len(alert_integration_pairs) > 0:
            future = self.__executor.submit(
                self.__internal_process_step3,
                alert_integration_pairs=alert_integration_pairs,
            )

            log.debug(f"Future : {future}")
        else:
            log.debug("Alert : Integration pair is empty")

        return zcp_alerts

    async def push_alert_event(self, zcp_alerts: List[ZcpAlert]):
        # @TODO: Modify the timing to publish alert event
        await publish_alert_event(zcp_alerts)

    def __internal_process_step3(
        self,
        *,
        action: Optional[Action] = None,
        alert_integration_pairs: List[Tuple[ZcpAlert, List[Integration]]],
        modifier: str | None = None,
    ) -> None:
        """Internal process step 3

        1. Send the notification to the matched integrations
        2. Skip to send the notification if the alert status is ACKED or SNOOZED
           when the alert from the alertmanager or other sources(elasticsearch, etc..)
        3. Insert activity log

        Args:
            param action: action optional
            param alert_integration_pairs: alert integration pairs mandatory
            param modifier: modifier optional

        Returns:
            None
        """
        if alert_integration_pairs is None or len(alert_integration_pairs) == 0:
            return None

        activities = []
        for zcp_alert, matched_integrations in alert_integration_pairs:
            if action is None and zcp_alert.status in [
                AlertStatus.ACKED,
                AlertStatus.SNOOZED,
            ]:
                log.debug(
                    f"ZcpAlert={zcp_alert.id} is ACKED or SNOOZED status, "
                    "so skip to send the notification"
                )
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        user=settings.ALERT_SYSTEM_USERNAME,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        description=[
                            f"The notification was not sent to the related channel "
                            f"because the alert staus is {zcp_alert.status.value}"
                        ],
                    )
                )
            else:
                # get the channel of the integration
                for integration in matched_integrations:
                    channel = integration.channel

                    if channel.type == ChannelType.SLACK:
                        # send the notification to the slack
                        self._send_notification_to_slack(
                            action=action,
                            modifier=modifier,
                            activities=activities,
                            zcp_alert=zcp_alert,
                            integration=integration,
                            slack=channel.type_properties,
                        )

                    elif channel.type == ChannelType.WEBHOOK:
                        # send the notification to the webhook
                        self._send_notification_to_webhook(
                            action=action,
                            modifier=modifier,
                            activities=activities,
                            zcp_alert=zcp_alert,
                            integration=integration,
                            webhook=channel.type_properties,
                        )
                    elif channel.type == ChannelType.KAKAOTALK:
                        # send the notification to the kakao talk
                        self._send_notification_to_kakaotalk(
                            action=action,
                            modifier=modifier,
                            activities=activities,
                            zcp_alert=zcp_alert,
                            integration=integration,
                            kakaotalk=channel.type_properties,
                            channel_id=channel.id,
                        )
                    elif channel.type == ChannelType.MSTEAMS:
                        # send the notification to the slack
                        self._send_notification_to_msteams(
                            action=action,
                            modifier=modifier,
                            activities=activities,
                            zcp_alert=zcp_alert,
                            integration=integration,
                            msteams=channel.type_properties,
                        )
                    elif channel.type == ChannelType.GOOGLECHAT:
                        # send the notification to the slack
                        self._send_notification_go_goolechat(
                            action=action,
                            modifier=modifier,
                            activities=activities,
                            zcp_alert=zcp_alert,
                            integration=integration,
                            google_chat=channel.type_properties,
                        )
                    elif channel.type == ChannelType.EMAIL:
                        # send the notification to the email
                        self._send_notification_to_email(
                            action=action,
                            modifier=modifier,
                            activities=activities,
                            zcp_alert=zcp_alert,
                            integration=integration,
                            email=channel.type_properties,
                        )
                    else:
                        log.debug(f"Channel type is not matched : {channel.type}")

        if len(activities) > 0:
            self.__activity_repository.insert_many(activities)

        return None

    def _send_notification_to_email(
        self,
        *,
        action: Action | None,
        modifier: str,
        activities: List[AlertActivity],
        zcp_alert: ZcpAlert,
        integration: Integration,
        email: EmailChannel,
    ) -> None:
        client = EmailClient(
            smtp_server=email.smtp_server,
            smtp_port=email.smtp_port,
            smtp_user=email.smtp_user,
            smtp_password=email.smtp_password,
            smtp_tls=email.smtp_tls,
            smtp_ssl=email.smtp_ssl,
            from_email=email.from_email,
            from_display_name=email.from_display_name,
        )

        start_time = time.time()

        response, message = client.send_email(
            action=action, alert=zcp_alert, modifier=modifier, to_emails=email.to_emails
        )

        elapsed_time = time.time() - start_time

        log.info(f"Send Email processing elapsed time : {elapsed_time:.5f} seconds")

        if response == Result.FAILED:
            log.error(
                f"Failed to send the notification to the email channel({email.smtp_server})"
                f" because {message}"
                f" of ({integration.id}:{integration.name})"
            )

            activities.append(
                AlertActivity(
                    alert_id=zcp_alert.id,
                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                    action=action,
                    user=settings.ALERT_SYSTEM_USERNAME,
                    description=(
                        [
                            f"Failed to send the notification to the email channel({email.smtp_server})"
                            f" of ({integration.id}:{integration.name}) because {message}"
                        ]
                    ),
                )
            )
        else:
            log.debug(f"Email Client response : {response}")

            # Success
            activities.append(
                AlertActivity(
                    alert_id=zcp_alert.id,
                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                    action=action,
                    user=settings.ALERT_SYSTEM_USERNAME,
                    description=(
                        [
                            "The notification has been sent successfully "
                            f"to the email channel({email.smtp_server})"
                            f" of ({integration.id}:{integration.name}).",
                            f"Elapsed time : {elapsed_time:.2f} ms",
                        ]
                    ),
                )
            )

        return None

    def _send_notification_to_kakaotalk(
        self,
        *,
        action: Action | None,
        modifier: str,
        activities: List[AlertActivity],
        zcp_alert: ZcpAlert,
        integration: Integration,
        kakaotalk: KakaoTalkChannel,
        channel_id: str,
    ) -> None:
        kakaotalk_token = None
        try:
            kakaotalk_token = self.__kakaotalk_token_repository.find_by_channel_id(
                channel_id
            )
        except ObjectNotFoundException:
            log.error(f"KakaoTalk token is not found : {channel_id}")
            activities.append(
                AlertActivity(
                    alert_id=zcp_alert.id,
                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                    action=action,
                    user=settings.ALERT_SYSTEM_USERNAME,
                    description=[
                        f"Failed to send the notification to the kakaotalk({kakaotalk.app_name}) "
                        f" of ({integration.id}:{integration.name})"
                        f" because the KakaoTalk token is not found by the channel id : {channel_id}"
                    ],
                )
            )
            return None

        if kakaotalk_token.is_expired_access_token():
            if kakaotalk_token.is_expired_refresh_token():
                log.error(
                    f"KakaoTalk access token and refresh token are expired : {kakaotalk_token.id}"
                )
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        action=action,
                        user=settings.ALERT_SYSTEM_USERNAME,
                        description=[
                            f"Failed to send the notification to the kakaotalk({kakaotalk.app_name}) "
                            f" of ({integration.id}:{integration.name})"
                            f" because the KakaoTalk access token and refresh token are expired"
                        ],
                    )
                )
                return None
            else:
                # refresh the access token
                try:
                    kakaotalk_token = self._refresh_kakaotalk_token(
                        kakaotalk_channel=kakaotalk, kakaotalk_token=kakaotalk_token
                    )
                except AlertBackendException as e:
                    log.error(
                        f"Failed to refresh the kakaotalk token : {kakaotalk_token.id}"
                    )
                    activities.append(
                        AlertActivity(
                            alert_id=zcp_alert.id,
                            created_at=datetime.now(DEFAULT_TIME_ZONE),
                            action=action,
                            user=settings.ALERT_SYSTEM_USERNAME,
                            description=[
                                f"Failed to send the notification to the kakaotalk({kakaotalk.app_name}) "
                                f" of ({integration.id}:{integration.name})"
                                f" because of failed to refresh the kakaotalk token : {str(e)}"
                            ],
                        )
                    )

                    return None

        client = KakaoTalkClient(access_token=kakaotalk_token.access_token)

        start_time = time.time()

        response, message = client.send_message_to_all(
            alert=zcp_alert, action=action, modifier=modifier
        )

        if response.get("result") == "failed" and message is not None:
            log.error(
                f"Failed to send the notification to the kakaotalk({kakaotalk.app_name})"
                f" of ({integration.id}:{integration.name})"
                f" because of {message}"
            )

            activities.append(
                AlertActivity(
                    alert_id=zcp_alert.id,
                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                    action=action,
                    user=settings.ALERT_SYSTEM_USERNAME,
                    description=(
                        [
                            f"Failed to send the notification to the kakaotalk({kakaotalk.app_name}) "
                            f" of ({integration.id}:{integration.name})"
                            f" because of {message}"
                        ]
                    ),
                )
            )
        else:
            # Success
            elapsed_time = time.time() - start_time
            log.info(f"Kakao Talk processing elapsed time : {elapsed_time:.5f} seconds")

            activities.append(
                AlertActivity(
                    alert_id=zcp_alert.id,
                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                    action=action,
                    user=settings.ALERT_SYSTEM_USERNAME,
                    description=(
                        [
                            "The notification has been sent successfully "
                            f"to the kakaotalk({kakaotalk.app_name})"
                            f" of ({integration.id}:{integration.name}).",
                            f"Elapsed time : {elapsed_time:.2f} ms",
                        ]
                    ),
                )
            )

        return None

    def _refresh_kakaotalk_token(
        self,
        *,
        kakaotalk_channel: KakaoTalkChannel,
        kakaotalk_token: KakaoTalkToken,
    ) -> KakaoTalkToken:
        log.debug(
            f"KakaoTalk access token is expired, so refresh the token : {kakaotalk_token.id}"
        )
        client = KakaoTalkClient()

        try:
            new_kakaotalk_token = client.kakao_refresh_token(
                client_id=kakaotalk_channel.client_id,
                client_secret=kakaotalk_channel.client_secret,
                refresh_token=kakaotalk_token.refresh_token,
            )
        except Exception as e:
            log.error(f"Failed to refresh the kakaotalk token : {kakaotalk_token.id}")
            raise AlertBackendException(
                AlertError.KAKAO_CHANNEL_ERROR,
                details=f"Failed to refresh the kakaotalk token : {str(e)}",
            )

        # Kakaotalk oauth server returns the new token data only
        # with the access token, expires_in, token_type
        # (id_token, refresh_token, expires_in_refresh_token are optional)
        #
        # copy the new token data value to the old token data
        kakaotalk_token.access_token = new_kakaotalk_token.access_token
        kakaotalk_token.access_token_updated_at = datetime.now(DEFAULT_TIME_ZONE)

        if new_kakaotalk_token.id_token:
            kakaotalk_token.id_token = new_kakaotalk_token.id_token

        if new_kakaotalk_token.refresh_token:
            kakaotalk_token.refresh_token = new_kakaotalk_token.refresh_token
            kakaotalk_token.refresh_token_updated_at = datetime.now(DEFAULT_TIME_ZONE)

        # update the token data and return the updated token data
        return self.__kakaotalk_token_repository.update(kakaotalk_token)

    def _send_notification_go_goolechat(
        self,
        *,
        action: Action | None,
        modifier: str,
        activities: List[AlertActivity],
        zcp_alert: ZcpAlert,
        integration: Integration,
        google_chat: GoogleChatChannel,
    ) -> None:
        client = GoogleChatClient(google_chat.api_url)

        start_time = time.time()

        response, message = client.sync_request(
            action=action, alert=zcp_alert, modifier=modifier
        )

        elapsed_time = time.time() - start_time

        log.info(f"Google Chat processing elapsed time : {elapsed_time:.5f} seconds")

        if response is None:
            log.error(
                f"Failed to send the notification to the google chat({google_chat.api_url})"
                f" #{google_chat.space_name}"
                f" of ({integration.id}:{integration.name})"
            )

            activities.append(
                AlertActivity(
                    alert_id=zcp_alert.id,
                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                    action=action,
                    user=settings.ALERT_SYSTEM_USERNAME,
                    description=(
                        [
                            f"Failed to send the notification to the google chat({google_chat.space_name}) "
                            f" of ({integration.id}:{integration.name}) because {message}"
                        ]
                    ),
                )
            )
        else:
            log.debug(f"Google Chat response : {response.status_code}")

            if response.status_code != HTTPStatus.OK:
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        action=action,
                        user=settings.ALERT_SYSTEM_USERNAME,
                        description=(
                            [
                                "Failed to send the notification "
                                f"to the google chat({google_chat.space_name}) "
                                f" of ({integration.id}:{integration.name}).",
                                f"Response code : {response.status_code}",
                            ]
                        ),
                    )
                )
            else:
                # Success
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        action=action,
                        user=settings.ALERT_SYSTEM_USERNAME,
                        description=(
                            [
                                "The notification has been sent successfully "
                                f"to the google chat({google_chat.space_name})"
                                f" of ({integration.id}:{integration.name}).",
                                f"Elapsed time : {elapsed_time:.2f} ms",
                            ]
                        ),
                    )
                )

        return None

    def _send_notification_to_msteams(
        self,
        *,
        action: Action | None,
        modifier: str,
        activities: List[AlertActivity],
        zcp_alert: ZcpAlert,
        integration: Integration,
        msteams: MSTeamsChannel,
    ) -> None:
        client = MSTeamsClient(msteams.api_url)

        start_time = time.time()

        response, message = client.sync_request(
            action=action, alert=zcp_alert, modifier=modifier
        )

        elapsed_time = time.time() - start_time

        log.info(f"MS Teams processing elapsed time : {elapsed_time:.5f} seconds")

        if response is None:
            log.error(
                f"Failed to send the notification to the ms teams({msteams.api_url})"
                f" #{msteams.channel_name}"
                f" of ({integration.id}:{integration.name})"
            )

            activities.append(
                AlertActivity(
                    alert_id=zcp_alert.id,
                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                    action=action,
                    user=settings.ALERT_SYSTEM_USERNAME,
                    description=(
                        [
                            f"Failed to send the notification to the ms teams({msteams.channel_name}) "
                            f" of ({integration.id}:{integration.name}) because {message}"
                        ]
                    ),
                )
            )
        else:
            log.debug(f"MS Teams Webhook response : {response.status_code}")

            if response.status_code != HTTPStatus.OK:
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        action=action,
                        user=settings.ALERT_SYSTEM_USERNAME,
                        description=(
                            [
                                "Failed to send the notification "
                                f"to the ms teams({msteams.channel_name}) "
                                f" of ({integration.id}:{integration.name}).",
                                f"Response code : {response.status_code}",
                            ]
                        ),
                    )
                )
            else:
                # Success
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        action=action,
                        user=settings.ALERT_SYSTEM_USERNAME,
                        description=(
                            [
                                "The notification has been sent successfully "
                                f"to the msteams({msteams.channel_name})"
                                f" of ({integration.id}:{integration.name}).",
                                f"Elapsed time : {elapsed_time:.2f} ms",
                            ]
                        ),
                    )
                )

        return None

    def _send_notification_to_webhook(
        self,
        *,
        action: Action | None,
        modifier: str,
        activities: List[AlertActivity],
        zcp_alert: ZcpAlert,
        integration: Integration,
        webhook: WebhookChannel,
    ) -> None:
        client = WebhookClient(
            webhook.webhook_url, **webhook.model_dump(exclude=["webhook_url"])
        )

        start_time = time.time()

        response, message = client.sync_request(
            action=action, alert=zcp_alert, modifier=modifier
        )

        elapsed_time = time.time() - start_time  # * 1000

        log.info(f"Webhook processing elapsed time : {elapsed_time:.5f} seconds")

        if response is None:
            log.error(
                f"Failed to send the notification to the webhook({webhook.webhook_url})"
                f" of ({integration.id}:{integration.name})"
            )

            activities.append(
                AlertActivity(
                    alert_id=zcp_alert.id,
                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                    action=action,
                    user=settings.ALERT_SYSTEM_USERNAME,
                    description=(
                        [
                            "Failed to send the notification "
                            f"to the webhook({webhook.webhook_url})"
                            f" of ({integration.id}:{integration.name}) because {message}"
                        ]
                    ),
                )
            )
        else:
            log.debug(f"Webhook response : {response.status_code}")

            if response.status_code != HTTPStatus.OK:
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        action=action,
                        user=settings.ALERT_SYSTEM_USERNAME,
                        description=(
                            [
                                "Failed to send the notification "
                                f"to the webhook({webhook.webhook_url})"
                                f" of ({integration.id}:{integration.name}).",
                                f"Response code : {response.status_code}",
                            ]
                        ),
                    )
                )
            else:
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        action=action,
                        user=settings.ALERT_SYSTEM_USERNAME,
                        description=(
                            [
                                "The notification has been sent successfully "
                                f"to the webhook({webhook.webhook_url})"
                                f" of ({integration.id}:{integration.name}).",
                                f"Elapsed time : {elapsed_time:.2f} ms",
                            ]
                        ),
                    )
                )

        return None

    def _send_notification_to_slack(
        self,
        *,
        action: Action | None,
        modifier: str,
        activities: List[AlertActivity],
        zcp_alert: ZcpAlert,
        integration: Integration,
        slack: SlackChannel,
    ) -> None:
        client = SlackClient(slack.api_url)

        start_time = time.time()

        response, message = client.sync_request(
            action=action, alert=zcp_alert, modifier=modifier
        )

        elapsed_time = time.time() - start_time

        log.info(f"Slack processing elapsed time : {elapsed_time:.5f} seconds")

        if response is None:
            log.error(
                f"Failed to send the notification to the slack({slack.api_url})"
                f" #{slack.channel_name}"
                f" of ({integration.id}:{integration.name})"
            )

            activities.append(
                AlertActivity(
                    alert_id=zcp_alert.id,
                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                    action=action,
                    user=settings.ALERT_SYSTEM_USERNAME,
                    description=(
                        [
                            f"Failed to send the notification to the slack({slack.channel_name}) "
                            f" of ({integration.id}:{integration.name}) because {message}"
                        ]
                    ),
                )
            )
        else:
            log.debug(f"Slack Webhook response : {response.status_code}")

            if response.status_code != HTTPStatus.OK:
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        action=action,
                        user=settings.ALERT_SYSTEM_USERNAME,
                        description=(
                            [
                                "Failed to send the notification "
                                f"to the slack({slack.channel_name}) "
                                f" of ({integration.id}:{integration.name}).",
                                f"Response code : {response.status_code}",
                            ]
                        ),
                    )
                )
            else:
                # Success
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        action=action,
                        user=settings.ALERT_SYSTEM_USERNAME,
                        description=(
                            [
                                "The notification has been sent successfully "
                                f"to the slack({slack.channel_name})"
                                f" of ({integration.id}:{integration.name}).",
                                f"Elapsed time : {elapsed_time:.2f} ms",
                            ]
                        ),
                    )
                )

        return None

    def __internal_process_step2(
        self, *, action: Optional[Action] = None, zcp_alerts: List[ZcpAlert]
    ) -> List[Tuple[ZcpAlert, List[Integration]]]:
        """Internal process step 2

        1. Find the matched integrations related for each alert
        2. Return alert integrations pairs in the list[Tuple[ZcpAlert, Integration]]

        Args:
            param action: action optional
            param zcp_alerts: zcp alerts mandatory

        Returns:
            List[Tuple[ZcpAlert, List[Integration]]]: list of alert integration pairs
        """
        alert_integration_pairs: List[Tuple[ZcpAlert, List[Integration]]] = []
        activities = []

        for zcp_alert in zcp_alerts:
            matched_integrations = []
            for integration in self.__get_cached_integrations().values():
                if integration.is_all_match(alert=zcp_alert, action=action):
                    # check if there are any active silences
                    silences = (
                        self.__silence_repository.find_all_active_by_integration_id(
                            integration.id
                        )
                    )
                    if silences is not None and len(silences) > 0:
                        log.debug(
                            f"ZcpAlert={zcp_alert.id} is matched with {integration.id}:{integration.name}"
                            f" but there are {len(silences)} active silences ({silences[0].name}, ..)"
                            f" so skip to send the notification to the channel ({integration.channel.name})"
                        )

                        activities.append(
                            AlertActivity(
                                alert_id=zcp_alert.id,
                                created_at=datetime.now(DEFAULT_TIME_ZONE),
                                user=settings.ALERT_SYSTEM_USERNAME,
                                description=[
                                    f"Didn't send the notification because"
                                    f" there are {len(silences)} active silences ({silences[0].name}, ..)"
                                    f" so skip to send the notification to the channel ({integration.channel.name})"
                                ],
                            )
                        )
                    else:
                        # get the channel of the integration
                        channel = integration.channel
                        if channel is not None and isinstance(channel, Channel):
                            log.debug(
                                f"ZcpAlert={zcp_alert.id} is matched with {integration.name} - {channel.name}"
                            )

                            matched_integrations.append(integration)
                        else:
                            log.debug(
                                f"ZcpAlert={zcp_alert.id} is matched with {integration.id}:{integration.name} "
                                "but channel is not found"
                            )

                            activities.append(
                                AlertActivity(
                                    alert_id=zcp_alert.id,
                                    created_at=datetime.now(DEFAULT_TIME_ZONE),
                                    user=settings.ALERT_SYSTEM_USERNAME,
                                    description=(
                                        [
                                            f"Couldn't send the notification because"
                                            f" the integration({integration.id}:{integration.name}) has no channel"
                                        ]
                                    ),
                                )
                            )
                else:
                    log.debug(
                        f"ZcpAlert={zcp_alert.id} is not matched with integration : "
                        f"{integration.id}:{integration.name}"
                    )

            if len(matched_integrations) == 0:
                activities.append(
                    AlertActivity(
                        alert_id=zcp_alert.id,
                        created_at=datetime.now(DEFAULT_TIME_ZONE),
                        user=settings.ALERT_SYSTEM_USERNAME,
                        description=[
                            "Couldn't send the notification to anywhere "
                            "because there is no any matched integrations"
                        ],
                    )
                )
            else:
                alert_integration_pairs.append((zcp_alert, matched_integrations))

        if len(activities) > 0:
            self.__activity_repository.insert_many(activities)

        return alert_integration_pairs

    def __internal_process_step1(self, alerts: List[Alert]) -> List[ZcpAlert]:
        """Internal process step 1

        1. Check if alert exists or not
        2. Create or Update alert
        3. Insert activity log
        4. Return zcp alerts

        Args:
            param alerts: alert list mandatory

        Returns:
            List[ZcpAlert]: list of zcp alerts
        """
        zcp_alerts = []
        for alert in alerts:
            exist_zcp_alert = self.__alert_repository.find_by_fingerprint(
                alert.fingerprint
            )
            activity = AlertActivity.from_empty()

            if exist_zcp_alert is None:
                """Create new alert"""
                new_zcp_alert = ZcpAlert.from_alert(alert=alert)
                # updated_at is set to created_at because of the search default sorting
                # converted to standard time zone
                new_zcp_alert.created_at = new_zcp_alert.updated_at = datetime.now(
                    DEFAULT_TIME_ZONE
                )

                new_zcp_alert.id = str(self.__alert_repository.insert(new_zcp_alert))
                zcp_alerts.append(new_zcp_alert)
                log.debug(f"Created an alert : {new_zcp_alert.id}")

                activity.set_data(
                    alert_id=new_zcp_alert.id,
                    description=[f"Created by {new_zcp_alert.sender.value}"],
                )

            else:
                """Update the alert"""
                updated_zcp_alert = exist_zcp_alert.model_copy()

                updated_zcp_alert.copy_from_alert(alert=alert)
                # update the updated_at and closed_at properties according to the status
                if updated_zcp_alert.status == AlertStatus.CLOSED:
                    updated_zcp_alert.updated_at = updated_zcp_alert.closed_at = (
                        datetime.now(DEFAULT_TIME_ZONE)
                    )
                else:
                    updated_zcp_alert.updated_at = datetime.now(DEFAULT_TIME_ZONE)
                    updated_zcp_alert.increase_repeated_count()
                    # @TODO: Check if the alert is triggered again by sender(alertmanager) after closed
                    if (
                        exist_zcp_alert.status == AlertStatus.CLOSED
                        and updated_zcp_alert.status == AlertStatus.OPEN
                    ):
                        # reset the timeline properties
                        updated_zcp_alert.created_at = datetime.now(DEFAULT_TIME_ZONE)
                        updated_zcp_alert.closed_at = None
                        updated_zcp_alert.acknowledged_at = None
                        updated_zcp_alert.snoozed_until_at = None
                        log.debug(
                            f"Reset the timeline properties : {updated_zcp_alert.id} "
                            "because the alert is triggered again alfert closed"
                        )

                updated_zcp_alert = self.__alert_repository.update(updated_zcp_alert)
                zcp_alerts.append(updated_zcp_alert)
                log.debug(f"Updated the alert : {updated_zcp_alert.id}")

                diffs = updated_zcp_alert.diff(before=exist_zcp_alert)
                description = (
                    diffs
                    if diffs is not None and len(diffs) > 0
                    else [f"Updated by {exist_zcp_alert.sender.value}"]
                )
                activity.set_data(alert_id=exist_zcp_alert.id, description=description)

            activity.set_data(
                created_at=datetime.now(DEFAULT_TIME_ZONE),
                user=Sender.ALERT_MANAGER if alert.sender is None else alert.sender,
            )

            activity_object_id = self.__activity_repository.insert(activity)
            log.debug(f"Inserted activity : {str(activity_object_id)}")
        return zcp_alerts

    def get_channel(self, channel_id: str) -> Channel:
        """Get channel by channel_id

        Args:
            param channel_id: channel id mandatory

        Returns:
            Channel: channel object

        Raises:
            AlertBackendException: if the channel is not found
            AlertBackendException: if the channel id is invalid
        """
        if not channel_id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Channel id is required"
            )

        try:
            return self.__channel_repository.find_by_id(channel_id)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="channel", object_id=channel_id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

    def get_all_channels(self) -> List[dict]:
        """Get all channels

        Returns:
            List[dict]: list of channel objects
        """
        return self.__channel_repository.find_all()

    def get_channels(
        self,
        *,
        name: Optional[str] = None,
        types: Optional[list[ChannelType]] = None,
        sort_field: Optional[ChannelSortField],
        sort_direction: Optional[SortDirection],
        page_number: int,
        page_size: int,
    ) -> List[Channel]:
        """Get channels by query parameters

        Args:
            param params: query parameters optional

        Returns:
            List[Channel]: list of channel objects  -
        """
        return self.__channel_repository.find(
            name=name,
            types=types,
            sort_field=sort_field,
            sort_direction=sort_direction,
            page_number=page_number,
            page_size=page_size,
        )

    def get_channels_count(
        self, *, name: Optional[str] = None, types: Optional[list[ChannelType]] = None
    ) -> int:
        """Get channels count by query parameters

        Parameters
        ----------
        name : Optional[str], optional
            by default None
        types : Optional[list[ChannelType]], optional
            by default None

        Returns
        -------
        int
            the count of channels which are matched with the query parameters
        """
        return self.__channel_repository.count(name=name, types=types)

    def create_channel(self, channel: Channel) -> str:
        """Create channel

        Parameters
        ----------
        channel : Channel

        Returns
        -------
        str
            inserted channel id

        Raises
        ------
        AlertBackendException
        """
        inserted_channel_id = ""
        try:
            inserted_channel_id = self.__channel_repository.insert(channel)
        except ValueError as e:
            raise AlertBackendException(AlertError.BAD_REQUEST, details=str(e))

        if inserted_channel_id is not None:
            if channel.type == ChannelType.KAKAOTALK:
                client = KakaoTalkClient()
                # kakaotalk_channel = channel.get_notification_channel(KakaoTalkChannel)
                kakaotalk_channel = channel.type_properties
                kakaotalk_token = {}

                try:
                    kakaotalk_token = client.generate_kakaotalk_token(
                        code=kakaotalk_channel.auth_code,
                        client_id=kakaotalk_channel.client_id,
                        client_secret=kakaotalk_channel.client_secret,
                    )
                except Exception as e:
                    raise AlertBackendException(
                        AlertError.KAKAO_CHANNEL_ERROR,
                        details=f"Failed to generate the Kakao token : {str(e)}",
                    )

                kakaotalk_token.channel_id = inserted_channel_id

                self.__kakaotalk_token_repository.insert(
                    kakaotalk_token=kakaotalk_token
                )

        return inserted_channel_id

    def modify_channel(self, channel: Channel) -> Channel:
        """Update channel

        Args:
            param channel: channel object mandatory

        Returns:
            Channel: updated channel object

        Raises:
            AlertBackendException: if the channel is not found
            AlertBackendException: if the channel id is invalid
        """
        exist_channel = self.__channel_repository.find_by_id(channel.id)
        if exist_channel is None:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="channel", object_id=channel.id
            )

        try:
            channel = self.__channel_repository.update(channel)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="channel", object_id=channel.id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        if channel.type == ChannelType.KAKAOTALK:
            kakaotalk_channel = channel.type_properties
            exit_kakaotalk_channel = exist_channel.type_properties
            if kakaotalk_channel.auth_code != exit_kakaotalk_channel.auth_code:
                client = KakaoTalkClient()
                kakaotalk_token = {}

                try:
                    kakaotalk_token = client.generate_kakaotalk_token(
                        code=kakaotalk_channel.auth_code,
                        client_id=kakaotalk_channel.client_id,
                        client_secret=kakaotalk_channel.client_secret,
                    )
                except Exception as e:
                    raise AlertBackendException(
                        AlertError.KAKAO_CHANNEL_ERROR,
                        details=f"Failed to generate the Kakao token : {str(e)}",
                    )

                exist_token = self.__kakaotalk_token_repository.find_by_channel_id(
                    channel.id
                )
                if exist_token is None:
                    self.__kakaotalk_token_repository.insert(
                        kakaotalk_token=kakaotalk_token
                    )
                else:
                    kakaotalk_token.channel_id = channel.id
                    kakaotalk_token.id = exist_token.id
                    self.__kakaotalk_token_repository.update(
                        kakaotalk_token=kakaotalk_token
                    )

        return channel

    def send_test_notification(self, channel: Channel) -> bool:
        if channel is None:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Channel is required"
            )

        if isinstance(channel.type_properties, KakaoTalkChannel):
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="KaKaoTalk channel is not supported"
            )
        elif isinstance(channel.type_properties, EmailChannel):
            email_channel = channel.type_properties
            client = EmailClient(
                smtp_user=email_channel.smtp_user,
                smtp_password=email_channel.smtp_password,
                smtp_server=email_channel.smtp_server,
                smtp_port=email_channel.smtp_port,
                smtp_tls=email_channel.smtp_tls,
                smtp_ssl=email_channel.smtp_ssl,
                from_email=email_channel.from_email,
                from_display_name=email_channel.from_display_name,
            )
            response, message = client.send_test_email(
                to_emails=email_channel.to_emails
            )

            if response == Result.FAILED:
                log.error(
                    f"Failed to send the notification to the email channel({email_channel.smtp_server})"
                )
                raise AlertBackendException(
                    AlertError.INTERNAL_SERVER_ERROR, details=message
                )
            else:
                return True
        else:
            response = None
            message = None
            if isinstance(channel.type_properties, SlackChannel):
                slack_channel = channel.type_properties
                client = SlackClient(slack_channel.api_url)
                response, message = client.send_test_message(modifier=channel.modifier)
            elif isinstance(channel.type_properties, GoogleChatChannel):
                googlechat_channel = channel.type_properties
                client = GoogleChatClient(googlechat_channel.api_url)
                response, message = client.send_test_message(modifier=channel.modifier)
            elif isinstance(channel.type_properties, MSTeamsChannel):
                msteams_channel = channel.type_properties
                client = MSTeamsClient(msteams_channel.api_url)
                response, message = client.send_test_message(modifier=channel.modifier)

            elif isinstance(channel.type_properties, WebhookChannel):
                webhook_channel = channel.type_properties
                client = WebhookClient(
                    webhook_channel.webhook_url,
                    **webhook_channel.model_dump(exclude=["webhook_url"]),
                )
                response, message = client.send_test_message(modifier=channel.modifier)
            else:
                raise AlertBackendException(
                    AlertError.BAD_REQUEST, details="Invalid channel object"
                )

            if response is None:
                log.error("Failed to send the test notification to the channel")

                raise AlertBackendException(
                    AlertError.INTERNAL_SERVER_ERROR, details=message
                )
            else:
                log.debug(f"Slack Webhook response : {response.status_code}")

                if response.status_code != HTTPStatus.OK:
                    raise AlertBackendException(
                        AlertError.INTERNAL_SERVER_ERROR,
                        details=f"Failed to send the test notification to the channel : {response.status_code}",
                    )
                else:
                    return True

    def remove_channel(self, channel_id: str) -> bool:
        """Delete channel by channel_id

        Args:
            param channel_id: channel id mandatory

        Returns:
            bool: True if successful

        Raises:
            AlertBackendException: if the channel is not found
            AlertBackendException: if the channel id is invalid
        """
        if not channel_id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Channel id is required"
            )

        # check logic related to integrations
        integrations = self.__integration_repository.find_all_by_channel_id(channel_id)
        if integrations is not None and len(integrations) > 0:
            raise AlertBackendException(
                AlertError.BAD_REQUEST,
                details=f"There are integrations({len(integrations)}) related to this channel",
            )

        try:
            return self.__channel_repository.delete_by_id(channel_id)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="channel", object_id=channel_id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

    def generate_kakao_token(
        self, *, code: str, client_id: str, client_secret: str | None = None
    ) -> List[Dict[str, Any]]:
        """Generate Kakao token

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
        List[Dict[str, Any]]
            the tokens which are returned from the Kakao OAuth2.0

        Raises
        ------
        AlertBackendException
        """
        data = {}
        data["grant_type"] = "authorization_code"
        data["client_id"] = client_id
        data["client_secret"] = client_secret
        data["code"] = code

        response = requests.post(
            f"{settings.KAKAO_AUTH_ENDPOINT}/oauth/token", data=data
        )
        if response.ok is False:
            raise AlertBackendException(AlertError.BAD_REQUEST, details=response.text)

        tokens = response.json()

        return tokens

    def get_kakao_friends(
        self,
        *,
        channel_id: str,
    ) -> list[KakaoTalkFriend]:
        """Get Kakao friends

        Parameters
        ----------
        channel_id : str

        Returns
        -------
        List[Dict[str, Any]]
        """
        if not channel_id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Channel id is required"
            )

        kakaotalk_token = None
        try:
            kakaotalk_token = self.__kakaotalk_token_repository.find_by_channel_id(
                channel_id
            )
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND,
                document="kakaotalk token",
                object_id=channel_id,
            )

        client = KakaoTalkClient(access_token=kakaotalk_token.access_token)

        try:
            return client.get_kakaotalk_friends()
        except Exception as e:
            raise AlertBackendException(
                AlertError.KAKAO_TOKEN_ERROR,
                details=f"Failed to get the Kakao friends : {str(e)}",
            )

    def get_integration(self, integration_id: str) -> Integration:
        """Get integration by integration_id

        Args:
            param integration_id: integration id mandatory

        Returns:
            Integration: integration object

        Raises:
            AlertBackendException: if the integration is not found
            AlertBackendException: if the integration id is invalid
        """
        if not integration_id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Integration id is required"
            )

        return self.__integration_repository.find_by_id_using_aggregator(integration_id)

    def _get_cached_integrations(self) -> Dict[str, Integration]:
        """Get all active integrations"""
        return self.__get_cached_integrations()

    def _refresh_cached_integrations(self):
        """Refresh all active integrations"""
        self.__cached_integrations__ = {}
        return True if len(self.__cached_integrations__) == 0 else False

    def __get_cached_integrations(self) -> Dict[str, Integration]:
        """Get all active integrations"""
        if len(self.__cached_integrations__) == 0:
            self.__cached_integrations__ = self.__init_cached_integrations()

        return self.__cached_integrations__

    def __init_cached_integrations(self) -> Dict[str, Integration]:
        """Get all active integrations"""
        integrations = self.__integration_repository.find_all_by_status(
            status=IntegrationStatus.ON
        )
        cache_data = {}
        for integration in integrations:
            cache_data[integration.id] = integration
            log.debug(
                f"Integration cached[init] : {integration.id} - {integration.name}"
            )

        return cache_data

    def __add_integration_to_cache(self, integration_id: str):
        """Add integration to cache

        Args:
            param integration: integration object mandatory
        """
        # for channel data of the integration which will be added in the cache
        # use the get_integration method
        integration = self.get_integration(integration_id)

        self.__cached_integrations__[integration.id] = integration
        log.debug(
            f"Integration has been added in the cache : {integration.id} - {integration.name}"
        )

    def __remove_integration_from_cache(self, integration_id: str):
        """Remove integration from cache

        Args:
            param integration_id: integration id mandatory
        """
        if integration_id in self.__cached_integrations__:
            del self.__cached_integrations__[integration_id]
            log.debug(f"Integration has been removed in the cache : {integration_id}")
        else:
            log.debug(f"Integration is not exist in the cache : {integration_id}")

    def get_integrations(
        self,
        *,
        name: Optional[str] = None,
        channel_name: Optional[str] = None,
        channel_type: Optional[ChannelType] = None,
        status: Optional[IntegrationStatus] = None,
        sort_field: Optional[str],
        sort_direction: Optional[str],
        page_number: int,
        page_size: int,
    ) -> List[Integration]:
        """Get integrations by query parameters

        Args:
            param name: name optional
            param page_number: page number mandatory
            param page_size: page size mandatory

        Returns:
            List[Integration]: list of integration objects
        """

        return self.__integration_repository.find(
            name=name,
            channel_name=channel_name,
            channel_type=channel_type,
            status=status,
            sort_field=sort_field,
            sort_direction=sort_direction,
            page_number=page_number,
            page_size=page_size,
        )

    def get_integrations_count(
        self,
        *,
        name: Optional[str] = None,
        channel_name: Optional[str] = None,
        channel_type: Optional[ChannelType] = None,
        status: Optional[IntegrationStatus] = None,
    ) -> int:
        """Get integrations count by query parameters

        Args:
            param name: name optional
            param channel_id: channel id optional
            param status: status optional

        Returns:
            int: count of integrations
        """
        return self.__integration_repository.count(
            name=name,
            channel_name=channel_name,
            channel_type=channel_type,
            status=status,
        )

    def get_all_integrations(self) -> List[dict]:
        """Get all integrations

        Returns:
            List[dict]: list of integration objects
        """
        return self.__integration_repository.find_all()

    def create_integration(self, integration: Integration) -> str:
        """Create integration

        Args:
            param integration: integration object mandatory

        Returns:
            str: inserted id

        Raises:
            AlertBackendException: if the integration is None
        """

        # check the existence of the channel
        channel_id = integration.channel
        try:
            self.__channel_repository.find_by_id(channel_id)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="channel", object_id=channel_id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        try:
            incerted_id = self.__integration_repository.insert(integration)
        except ValueError as e:
            raise AlertBackendException(AlertError.BAD_REQUEST, details=str(e))

        # refresh the cache
        if integration.status == IntegrationStatus.ON:
            self.__add_integration_to_cache(incerted_id)

        return incerted_id

    def modify_integration(self, integration: Integration) -> Integration:
        """Update integration

        Args:
            param integration: integration object mandatory

        Returns:
            Integration: updated integration object

        Raises:
            AlertBackendException: if the integration is not found
            AlertBackendException: if the integration id is invalid
        """
        try:
            updated_integration = self.__integration_repository.update(integration)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND,
                document="integration",
                object_id=integration.id,
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        # convert the channel id to channel object
        updated_integration.channel = self.__channel_repository.find_by_id(
            updated_integration.channel
        )

        # refresh the cache
        if updated_integration.status == IntegrationStatus.ON:
            self.__add_integration_to_cache(updated_integration.id)
        else:
            self.__remove_integration_from_cache(updated_integration.id)

        return updated_integration

    def patch_integration_status(
        self, *, integration_id: str, status: IntegrationStatus, modifier: str
    ) -> Integration:
        """Patch integration status

        Args:
            param integration_id: integration id mandatory
            param status: status mandatory
            param modifier: modifier mandatory

        Returns:
            bool: True if successful

        Raises:
            AlertBackendException: if the integration is not found
            AlertBackendException: if the integration id is invalid
        """
        try:
            integration = self.__integration_repository.update_status(
                integration_id=integration_id, status=status, modifier=modifier
            )
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND,
                document="integration",
                object_id=integration_id,
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        # refresh the cache
        if status == IntegrationStatus.ON:
            self.__add_integration_to_cache(integration_id)
        else:
            self.__remove_integration_from_cache(integration_id)

        return integration

    def remove_integration(self, integration_id: str) -> bool:
        """Delete integration by integration_id

        Args:
            param integration_id: integration id mandatory

        Returns:
            bool: True if successful

        Raises:
            AlertBackendException: if the integration is not found
            AlertBackendException: if the integration id is invalid
        """

        if not integration_id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Integration id is required"
            )

        # Implement the check logic related to silences
        silences = self.__silence_repository.find_by_integration_id(integration_id)
        if silences is not None and len(silences) > 0:
            raise AlertBackendException(
                AlertError.BAD_REQUEST,
                details=f"There are silences({len(silences)}) related to this integration",
            )

        try:
            result = self.__integration_repository.delete_by_id(integration_id)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND,
                document="integration",
                object_id=integration_id,
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        # refresh the cache
        self.__remove_integration_from_cache(integration_id)

        return result

    def get_integration_filters(self) -> List[Filter]:
        """Get integration filters

        Returns:
            List[str]: list of integration filters
        """
        return [
            self._get_text_type_dummy_filter(key=FilterKey.SUMMARY),
            self._get_text_type_dummy_filter(key=FilterKey.DESCRIPTION),
            self._get_single_select_type_dummy_filter(key=FilterKey.PROJECT),
            self._get_multi_select_type_dummy_filter(key=FilterKey.CLUSTER),
            self._get_multi_select_type_dummy_filter(key=FilterKey.NAMESPACE),
            self._get_text_type_dummy_filter(key=FilterKey.USER_LABEL),
            self._get_multi_select_type_dummy_filter(
                key=FilterKey.SENDER, value=[s for s in Sender]
            ),
            self._get_multi_select_type_dummy_filter(
                key=FilterKey.PRIORITY, value=[p for p in Priority]
            ),
            self._get_multi_select_type_dummy_filter(
                key=FilterKey.SEVERITY, value=[s for s in Severity]
            ),
            Filter(
                key=FilterKey.REPEATED_COUNT,
                value_type=FilterValueType.NUMBER,
                operator=[Operator.GREATER_THAN, Operator.LESS_THAN],
            ),
        ]

    def _get_text_type_dummy_filter(self, *, key: FilterKey | None) -> Filter:
        """keyword search filter

        Parameters
        ----------
        key : FilterKey | None

        Returns
        -------
        Filter
        """
        return Filter(
            key=key,
            value_type=FilterValueType.TEXT,
            operator=[
                Operator.EQUALS,
                Operator.MATCHES,
                Operator.STARTS_WITH,
                Operator.ENDS_WITH,
                Operator.IS_EMPTY,
            ],
        )

    def _get_multi_text_type_dummy_filter(self, *, key: FilterKey | None) -> Filter:
        """contains search filter

        Parameters
        ----------
        key : FilterKey | None

        Returns
        -------
        Filter
        """
        return Filter(
            key=key,
            value_type=FilterValueType.MULTI_TEXT,
            operator=[
                Operator.CONTAINS,
            ],
        )

    def _get_multi_select_type_dummy_filter(
        self,
        *,
        key: FilterKey | None,
        value: Optional[Union[Sender, Priority, Severity]] | None = None,
    ) -> Filter:
        return Filter(
            key=key,
            value_type=FilterValueType.MULTI_SELECT,
            value=value,
            operator=[
                Operator.CONTAINS,
            ],
        )

    def _get_single_select_type_dummy_filter(
        self,
        *,
        key: FilterKey | None,
        value: Optional[Union[Sender, Priority, Severity]] | None = None,
    ) -> Filter:
        return Filter(
            key=key,
            value_type=FilterValueType.SINGLE_SELECT,
            value=value,
            operator=[
                Operator.EQUALS,
            ],
        )

    def get_integration_filter_modes(self) -> List[FilterMode]:
        """Get integration filter modes

        Returns:
            List[FilterMode]: list of integration filter modes
        """
        return [mode for mode in FilterMode]

    def get_priorities(self) -> List[Priority]:
        """Get priorities

        Returns
        -------
        List[Priority]
        """
        return [priority for priority in Priority]

    def get_severities(self) -> List[Severity]:
        """Get severities

        Returns
        -------
        List[Severity]
        """
        return [severity for severity in Severity]

    def get_senders(self) -> List[Sender]:
        """Get senders

        Returns
        -------
        List[Sender]
        """
        return [sender for sender in Sender]

    def get_actions(self) -> List[Action]:
        """Get actions

        Returns
        -------
        List[Action]
        """
        return [action for action in Action]

    def get_channel_types(self) -> List[ChannelType]:
        """Get channel types

        Returns
        -------
        List[ChannelType]
        """
        return [channel_type for channel_type in ChannelType]

    def get_silences(
        self,
        *,
        name: Optional[str] = None,
        statuses: Optional[list[SilenceStatus]] = None,
        integration_id: Optional[str] = None,
        sort_field: Optional[SilenceSortField],
        sort_direction: Optional[SortDirection],
        page_number: int,
        page_size: int,
    ) -> List[Silence]:
        """Get silences by query parameters

        Args:
            param page_number: page number mandatory
            param page_size: page size mandatory

        Returns:
            List[Silence]: list of silence objects
        """
        return self.__silence_repository.find(
            name=name,
            statuses=statuses,
            sort_field=sort_field,
            sort_direction=sort_direction,
            integration_id=integration_id,
            page_number=page_number,
            page_size=page_size,
        )

    def get_silences_count(
        self,
        *,
        name: Optional[str] = None,
        statuses: Optional[list[SilenceStatus]] = None,
        integration_id: Optional[str] = None,
    ) -> int:
        """Get silences count by query parameters

        Args:
            param name: name optional
            param status: status optional

        Returns:
            int: count of silences
        """
        return self.__silence_repository.count(
            name=name, statuses=statuses, integration_id=integration_id
        )

    def create_silence(self, silence: Silence) -> str:
        """Create silence

        Args:
            param silence: silence object mandatory

        Returns:
            str: inserted id

        Raises:
            AlertBackendException: if the silence is None
        """
        # check the existence of the integrations
        integration_ids = silence.integrations
        if integration_ids is None or len(integration_ids) == 0:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Integrations are required"
            )

        for integration_id in integration_ids:
            try:
                self.__integration_repository.find_by_id(integration_id)
            except ObjectNotFoundException:
                raise AlertBackendException(
                    AlertError.ID_NOT_FOUND,
                    document="integration",
                    object_id=integration_id,
                )
            except InvalidObjectIDException as e:
                raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        try:
            return self.__silence_repository.insert(silence)
        except ValueError as e:
            raise AlertBackendException(AlertError.BAD_REQUEST, details=str(e))

    def modify_silence(self, silence: Silence) -> Silence:
        """Update silence

        Args:
            param silence: silence object mandatory

        Returns:
            Silence: updated silence object

        Raises:
            AlertBackendException: if the silence is not found
            AlertBackendException: if the silence id is invalid
        """
        # check the existence of the integrations
        integration_ids = silence.integrations
        if integration_ids is None or len(integration_ids) == 0:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Integrations are required"
            )

        for integration_id in integration_ids:
            try:
                self.__integration_repository.find_by_id(integration_id)
            except ObjectNotFoundException:
                raise AlertBackendException(
                    AlertError.ID_NOT_FOUND,
                    document="integration",
                    object_id=integration_id,
                )
            except InvalidObjectIDException as e:
                raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        try:
            updated_silence = self.__silence_repository.update(silence)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="silence", object_id=silence.id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        # convert list[str] to list[Integration]
        ids = [integration for integration in updated_silence.integrations]
        integrations = self.__integration_repository.find_all_by_ids(ids)
        if integrations is not None and len(integrations) > 0:
            updated_silence.integrations = integrations

        return updated_silence

    def remove_silence(self, silence_id: str) -> bool:
        """Delete silence by silence_id

        Args:
            param silence_id: silence id mandatory

        Returns:
            bool: True if successful

        Raises:
            AlertBackendException: if the silence is not found
            AlertBackendException: if the silence id is invalid
        """

        if not silence_id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Silence id is required"
            )

        try:
            return self.__silence_repository.delete_by_id(silence_id)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="silence", object_id=silence_id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

    def get_silence(self, silence_id: str) -> Silence:
        """Get silence by silence_id

        Args:
            param silence_id: silence id mandatory

        Returns:
            Silence: silence object

        Raises:
            AlertBackendException: if the silence is not found
            AlertBackendException: if the silence id is invalid
        """
        if not silence_id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Silence id is required"
            )
        try:
            silence = self.__silence_repository.find_by_id(silence_id)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="silence", object_id=silence_id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

        # convert list[str] to list[Integration]
        ids = [integration for integration in silence.integrations]
        integrations = self.__integration_repository.find_all_by_ids(ids)
        if integrations is not None and len(integrations) > 0:
            silence.integrations = integrations

        return silence

    def create_basic_auth_user(self, user: BasicAuthUser) -> str:
        """Create basic auth user

        Parameters
        ----------
        user : BasicAuthUser

        Returns
        -------
        str

        Raises
        ------
        AlertBackendException
        """
        try:
            return self.__basic_auth_user_repository.insert(user)
        except ValueError as e:
            raise AlertBackendException(AlertError.BAD_REQUEST, details=str(e))

    def modify_basic_auth_user(self, user: BasicAuthUser) -> BasicAuthUser:
        """Update basic auth user

        Parameters
        ----------
        user : BasicAuthUser

        Returns
        -------
        BasicAuthUser

        Raises
        ------
        AlertBackendException
        """
        try:
            return self.__basic_auth_user_repository.update(user)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND,
                document="zcp_basic_auth_user",
                object_id=user.id,
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

    def remove_basic_auth_user(self, id: str) -> bool:
        """Delete basic auth user by id

        Parameters
        ----------
        id : str

        Returns
        -------
        bool

        Raises
        ------
        AlertBackendException
        """
        if not id:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="ID is required"
            )

        try:
            return self.__basic_auth_user_repository.delete_by_id(id)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND, document="basic_auth_user", object_id=id
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

    def get_basic_auth_user_by_username(self, username: str) -> BasicAuthUser:
        """Get basic auth user by username

        Parameters
        ----------
        username : str

        Returns
        -------
        BasicAuthUser

        Raises
        ------
        AlertBackendException
        """
        if not username:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details="Username is required"
            )

        try:
            return self.__basic_auth_user_repository.find_by_username(username)
        except ObjectNotFoundException:
            raise AlertBackendException(
                AlertError.ID_NOT_FOUND,
                document="zcp_basic_auth_user",
                object_id=username,
            )
        except InvalidObjectIDException as e:
            raise AlertBackendException(AlertError.INVALID_OBJECTID, details=str(e))

    def get_basic_auth_users(self) -> List[BasicAuthUser]:
        """Get basic auth users by query parameters

        Returns
        -------
        List[BasicAuthUser]
        """
        return self.__basic_auth_user_repository.find()

    def get_user_notification_settins(self, username: str) -> UserNotificationSettings:
        """Get user notification settings

        Parameters
        ----------
        username : str

        Returns
        -------
        UserNotificationSettings
        """

        user_notification_settings = None
        try:
            user_notification_settings = (
                self.__user_notification_settings_repository.find_by_username(username)
            )
        except ObjectNotFoundException:
            user_notification_settings = UserNotificationSettings(
                username=username,
                priorities=settings.USER_NOTIFICATION_DEFAULT_PRIORITIES,
            )

        return user_notification_settings

    def update_user_notification_settings(
        self, user_notification_settings: UserNotificationSettings
    ) -> UserNotificationSettings:
        """Insert or Update user notification settings

        Parameters
        ----------
        user_notification_settings : UserNotificationSettings

        Returns
        -------
        bool
        """
        if user_notification_settings.id is not None:
            try:
                ObjectId(user_notification_settings.id)
            except InvalidId:
                raise AlertBackendException(
                    AlertError.INVALID_OBJECTID,
                    details=f"Invalid object id({user_notification_settings.id})",
                )

            exist_unss = self.__user_notification_settings_repository.find_by_id(
                user_notification_settings.id
            )
            if exist_unss is None:
                raise AlertBackendException(
                    AlertError.ID_NOT_FOUND,
                    document="zcp_user_notification_settings",
                    object_id=user_notification_settings.id,
                )

            return self.__user_notification_settings_repository.update(
                user_notification_settings
            )
        else:
            try:
                exist_unss = (
                    self.__user_notification_settings_repository.find_by_username(
                        user_notification_settings.username
                    )
                )
            except ObjectNotFoundException:
                exist_unss = None

            if exist_unss is not None:
                user_notification_settings.id = exist_unss.id
                return self.__user_notification_settings_repository.update(
                    user_notification_settings
                )
            else:
                try:
                    __object_id = self.__user_notification_settings_repository.insert(
                        user_notification_settings
                    )
                except ValueError as e:
                    raise AlertBackendException(AlertError.BAD_REQUEST, details=str(e))
                user_notification_settings.id = __object_id

                return user_notification_settings

    def delete_user_notification_settings(self, user_notification_settings_id) -> bool:
        """Delete user notification settings by id

        Parameters
        ----------
        user_notification_settings_id : str

        Returns
        -------
        bool
        """
        return self.__user_notification_settings_repository.delete_by_id(
            user_notification_settings_id
        )
