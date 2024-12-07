from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Dict, List, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_serializer


class Status(str, Enum):
    """Status of the alert. It can be firing or resolved.

    It's value should be 'firing' or 'resolved' because it's from AlertManager
    """

    FIRING = "firing"
    RESOVLED = "resolved"


class Sender(str, Enum):
    """Sender of the alert. It can be AlertManager, OpenSearch, K8sWatcher, Others"""

    ALERT_MANAGER = "AlertManager"
    OPENSEARCH = "OpenSearch"
    K8S_WATCHER = "K8sWatcher"


class Alert(BaseModel):
    """
    Alert payload specification

    ref:
    https://prometheus.io/docs/alerting/latest/notifications/
    """

    sender: Optional[Sender] = None
    """ Added for the sender of the alert"""
    status: Status
    labels: Dict[str, str]
    annotations: Dict[str, str] = None
    startsAt: Optional[datetime] = None
    endsAt: Optional[datetime] = None
    generatorURL: Optional[str] = None
    fingerprint: str

    sender: Optional[Sender] = None
    """ Added for the sender of the alert"""

    def is_include_mandatory_fields_in_annotations(self, key: str) -> bool:
        """Check if the mandatory fields are included in annotations"""
        return key in self.annotations.keys()

    def is_include_mandatory_fields_in_labels(self, key: str) -> bool:
        """Check if the mandatory fields are included in labels"""
        return key in self.labels.keys()


class AlertData(BaseModel):
    """
    Alert Data payload specification

    ref:
    https://prometheus.io/docs/alerting/latest/notifications/
    """

    receiver: Optional[str] = None
    status: Optional[Status] = None
    alerts: List[Alert]
    groupLabels: Optional[Dict[str, str]] = None
    commonLabels: Optional[Dict[str, str]] = None
    commonAnnotations: Optional[Dict[str, str]] = None
    externalURL: Optional[str] = None
    version: Optional[str] = None
    groupKey: Optional[str] = None


class Action(str, Enum):
    """Action of the alert. It can be ack, unack, snooze, close"""

    ACK = "ack"
    UNACK = "unack"
    SNOOZE = "snooze"
    CLOSE = "close"
    WAKEUP = "wakeup"

    def get_tobe_status(self) -> "AlertStatus":
        """Get the status of the alert after the action applied"""
        if self == Action.ACK:
            return AlertStatus.ACKED
        elif self == Action.UNACK:
            return AlertStatus.OPEN
        elif self == Action.SNOOZE:
            return AlertStatus.SNOOZED
        elif self == Action.CLOSE:
            return AlertStatus.CLOSED
        elif self == Action.WAKEUP:
            return AlertStatus.OPEN
        return None


class AlertStatus(str, Enum):
    """Alert status. It can be Open, Closed, Snoozed, Acked"""

    OPEN = "Open"
    CLOSED = "Closed"
    SNOOZED = "Snoozed"
    ACKED = "Acked"

    def allow_action(self, action: Action) -> bool:
        """Check if the action can be applied to the alert status

        params:
        - action: Action

        return:
        - bool
        """
        if self == AlertStatus.OPEN:
            return action in [Action.ACK, Action.SNOOZE, Action.CLOSE]
        elif self == AlertStatus.SNOOZED:
            return action in [Action.ACK, Action.SNOOZE, Action.CLOSE, Action.WAKEUP]
        elif self == AlertStatus.ACKED:
            return action in [Action.UNACK, Action.CLOSE]
        return False


class Priority(str, Enum):
    """Priority model"""

    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"


class Severity(str, Enum):
    """Severity model"""

    CRITICAL = "critical"
    WARNING = "warning"


class RepeatedCountOperator(str, Enum):
    GT = "gt(>)"
    GTE = "gte(>=)"
    LT = "lt(<)"
    LTE = "lte(<=)"


class AlertSortField(str, Enum):
    SENDER = "sender"
    STATUS = "status"
    REPEATED_COUNT = "repeated_count"
    ALERT_NAME = "alertname"  # labels.alertname
    SUMMARY = "summary"  # annotation.summary
    PRIORITY = "priority"  # labels.priority
    SEVERITY = "severity"  # labels.severity
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    CLOSED_AT = "closed_at"
    ACKNOWLEDGED_AT = "acknowledged_at"


PyObjectId = Annotated[str, BeforeValidator(str)]


class AlertBaseModel(BaseModel):
    """Alert Base Model

    mongodb objectId _id issues

    refence:
    https://github.com/tiangolo/fastapi/issues/1515
    https://github.com/mongodb-developer/mongodb-with-fastapi
    """

    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        extra="forbid",
        # json_encoders has been deprecated
        # https://docs.pydantic.dev/2.6/migration/
        # https://docs.pydantic.dev/latest/concepts/serialization/#custom-serializers
        #
        # json_encoders={
        #     ObjectId: str,
        #     datetime: lambda dt: dt.isoformat(),
        # },
    )

    @field_serializer("id")
    def _serialize_id(self, id: Optional[PyObjectId]) -> Optional[str]:
        if id is None:
            return None
        else:
            return str(id)

    @field_serializer("created_at", "updated_at")
    def _serialize_created_updated_at(self, dt: Optional[datetime]) -> Optional[str]:
        return dt.isoformat(timespec="milliseconds") if dt else None

    @classmethod
    def from_empty(cls):
        return cls()

    def set_data(self, **data: Dict[Any, Any]):
        for k, v in data.items():
            setattr(self, k, v)


class AlertActivity(AlertBaseModel):
    """Alert activity log model"""

    alert_id: Optional[str] = None
    action: Optional[Action] = None
    user: Optional[str] = None
    description: Optional[List[str]] = None

    updated_at: Optional[datetime] = Field(default=None, exclude=True)


class ZcpAlert(AlertBaseModel):
    """ZcpAlert model"""

    sender: Optional[Sender] = None
    repeated_count: Optional[int] = 0
    activities: Optional[List[AlertActivity]] = None
    snoozed_until_at: Optional[datetime] = None
    modifier: Optional[str] = None

    # from Alert
    status: Optional[AlertStatus] = None
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, str]] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    generator_url: Optional[str] = None
    fingerprint: Optional[str] = None

    # add for the analysis
    closed_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None

    model_config = ConfigDict(
        extra="allow",
    )

    @field_serializer(
        "acknowledged_at", "closed_at", "snoozed_until_at", "starts_at", "ends_at"
    )
    def _serialize_closed_snoozed_at(self, dt: Optional[datetime]) -> Optional[str]:
        return dt.isoformat(timespec="milliseconds") if dt else None

    @classmethod
    def from_alert(cls, *, alert: Alert):
        """Create ZcpAlert instance from Alert instance and return it"""
        # prometheus alertmanager sends only the firing or resolved status
        return cls(
            status=AlertStatus.OPEN
            if alert.status == Status.FIRING
            else AlertStatus.CLOSED,
            labels=alert.labels,
            annotations=alert.annotations,
            starts_at=alert.startsAt,
            ends_at=alert.endsAt,
            generator_url=alert.generatorURL,
            fingerprint=alert.fingerprint,
            sender=Sender.ALERT_MANAGER if alert.sender is None else alert.sender,
        )

    def increase_repeated_count(self):
        """Increase the repeated count"""
        if self.status != AlertStatus.CLOSED:
            self.repeated_count += 1

    def copy_from_alert(self, *, alert: Alert):
        """Copy data from Alert instance to the self instance(ZcpAlert) and return self"""
        # self.status = AlertStatus.OPEN if alert.status == Status.FIRING else AlertStatus.CLOSED
        if alert.status == Status.FIRING:
            if self.status is not None and (
                self.status == AlertStatus.ACKED or self.status == AlertStatus.SNOOZED
            ):
                # don't change the status if the alert is acked or snoozed
                ...
            else:
                self.status = AlertStatus.OPEN
        else:
            self.status = AlertStatus.CLOSED

        self.labels = alert.labels
        self.annotations = alert.annotations
        self.starts_at = alert.startsAt
        self.ends_at = alert.endsAt
        self.generator_url = alert.generatorURL
        self.fingerprint = alert.fingerprint

        self.sender = Sender.ALERT_MANAGER if alert.sender is None else alert.sender

        return self

    def diff(self, *, before: AlertBaseModel) -> List[str]:
        """Compare the data between self and before instance and return the difference

        params:
        - before: ZcpAlert instance

        return:
        - difference: List[str]

        example:
        - ["status: Open -> Closed", "labels.alertname: test -> test2", "annotations.summary: test -> test2"]
        - ["status: Open -> Closed", "repeated count: 1 -> 2", "labels.alertname: test -> test2", "annotations.summary: test -> test2"]
        """
        difference = []
        before_dict = before.model_dump()
        if before_dict["status"] != self.status:
            difference.append(
                f"status: {before_dict['status'].value} -> {self.status.value}"
            )

        if before_dict["repeated_count"] != self.repeated_count:
            difference.append(
                f"repeated count: {before_dict['repeated_count']} -> {self.repeated_count}"
            )

        labels = before_dict["labels"]
        # record the removed labels
        for k, v in labels.items():
            if k not in self.labels:
                difference.append(f"labels.{k}: {v} has been removed")
            elif v != self.labels[k]:
                difference.append(f"labels.{k}: {v} -> {self.labels[k]}")
        for k, v in self.labels.items():
            if k not in labels:
                difference.append(f"labels.{k}: {v} has been added")

        annotations = before_dict["annotations"]
        # record the updated annotations
        for k, v in annotations.items():
            if k not in self.annotations:
                difference.append(f"annotations.{k}: {v} has been removed")
            elif v != self.annotations[k]:
                difference.append(f"annotations.{k}: {v} -> {self.annotations[k]}")
        # record the added annotations
        for k, v in self.annotations.items():
            if k not in annotations:
                difference.append(f"annotations.{k}: {v} has been added")

        return difference

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, ZcpAlert):
            return self.id == other.id
        return False
