from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field

from app.model.alert_model import (
    AlertSortField,
    AlertStatus,
    Priority,
    RepeatedCountOperator,
    Sender,
    Severity,
)
from app.utils.list_utils import SortDirection


class Label:
    key: str
    value: str

    def __init__(self, label: str):
        self.key, self.value = label.split(":", 1)


class AlertSearchRequest(BaseModel):
    statuses: Optional[list[AlertStatus]] = None
    senders: Optional[list[Sender]] = None
    priorities: Optional[list[Priority]] = None  # labels.priority
    severities: Optional[list[Severity]] = None  # labels.severity
    fingerprint: Optional[str] = Field(None, max_length=36)
    repeated_count: Optional[int] = Field(None, le=10000, ge=0)
    repeated_count_operator: Optional[RepeatedCountOperator] = RepeatedCountOperator.GTE
    alertname: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=100)  # annotation.description
    summary: Optional[str] = Field(None, max_length=100)  # annotation.summary
    project: Optional[str] = Field(None, max_length=100)  # labels.project
    clusters: Optional[list[str]] = None  # labels.cluster
    namespaces: Optional[list[str]] = None  # labels.namespace
    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)
    sort_field: Optional[AlertSortField] = Field(None)
    sort_direction: Optional[SortDirection] = Field(None)
    alert_id: Optional[str] = Field(None, max_length=100)
    start_date_created_at: Optional[datetime] = Field(None)
    end_date_created_at: Optional[datetime] = Field(None)
    start_date_closed_at: Optional[datetime] = Field(None)
    end_date_closed_at: Optional[datetime] = Field(None)
    labels: Optional[list[str]] = None

    @property
    def parsed_labels(self) -> list[Label]:
        if self.labels:
            return [Label(label) for label in self.labels]
        else:
            return None


class AlertActionRequest(BaseModel):
    """Alert action request model for the restful api which patch alert status"""

    alert_id: Optional[str] = Field(max_length=100)
    asis_status: Optional[AlertStatus]


class TestAlertCreateRequest(BaseModel):
    """Alert request model for the restful api which create or update alert"""

    summary: str = Field("This is a test alert", max_length=300)
    description: str = Field(
        "This is a test alert for checking the integration channel", max_length=500
    )
    alertname: str = Field("AlertNotificationTest", max_length=100)
    priority: Priority
    severity: Severity
    labels: Optional[Dict[str, str]] = None
