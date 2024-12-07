import re
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, model_validator

from app.model.alert_model import Action, AlertBaseModel, ZcpAlert
from app.model.channel_model import Channel


class IntegrationStatus(str, Enum):
    """Integration status model"""

    ON = "On"
    OFF = "Off"


class Operator(str, Enum):
    EQUALS = "Equals"  # == (text, number)
    MATCHES = "Matches(Regex)"  # regex
    STARTS_WITH = "StartsWith"  # startswith (text)
    ENDS_WITH = "EndsWith"  # endswith (text)
    IS_EMPTY = "IsEmpty"  # all
    CONTAINS = "Contains"  # in (multi-select)
    GREATER_THAN = "GreaterThan"  # > (number, text)
    LESS_THAN = "LessThan"  # < (number, text)


class FilterKey(str, Enum):
    SUMMARY = "summary"  # annotations.summary
    DESCRIPTION = "description"  # annotations.description
    PROJECT = "project"  # labels.project
    PRIORITY = "priority"  # labels.priority
    SEVERITY = "severity"  # labels.severity
    CLUSTER = "cluster"  # labels.cluster-
    NAMESPACE = "namespace"  # labels.namespace
    USER_LABEL = "user_label"  # labels.{user_input_key}
    SENDER = "sender"  # sender
    REPEATED_COUNT = "repeated_count"  # repeated_count


class FilterValueType(str, Enum):
    TEXT = "Text"
    MULTI_TEXT = "MultiText"
    NUMBER = "Number"
    SINGLE_SELECT = "SingleSelect"
    MULTI_SELECT = "MultiSelect"
    REGEX = "Regex"


class FilterMode(str, Enum):
    """Filter mode model"""

    ALL = "All-Alerts"
    MATCH_ANY = "MatchAny"
    MATCH_ALL = "MatchAll"


class IntegrationSortField(str, Enum):
    NAME = "name"
    CHANNEL_NAME = "channel_name"  # channel.name
    CHANNEL_TYPE = "channel_type"  # channel.type
    STATUS = "status"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"


class Filter(BaseModel):
    key: FilterKey
    value_type: FilterValueType
    value: Optional[Union[str, List[str]]] = None
    is_equal: bool = True
    operator: Union[Operator, List[Operator]]
    user_label_key: Optional[str] = None

    def is_multiple_value(self) -> bool:
        return self.value_type in [
            FilterValueType.MULTI_TEXT,
            FilterValueType.MULTI_SELECT,
        ]

    # @root_validator(pre=True)
    @model_validator(mode="before")
    @classmethod
    def assign_type_properties(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        value_type = values.get("value_type")
        s_value = values.get("value")
        operator = values.get("operator")
        if value_type not in [FilterValueType.MULTI_TEXT, FilterValueType.MULTI_SELECT]:
            if isinstance(s_value, list):
                raise ValueError(
                    f"Value should not be a single value when the value_type is {value_type}"
                )
        elif value_type in [FilterValueType.MULTI_TEXT, FilterValueType.MULTI_SELECT]:
            if s_value is not None and not isinstance(s_value, list):
                raise ValueError(
                    f"Value should be a list when the value_type is {value_type}"
                )
            if isinstance(operator, Operator) and operator != Operator.CONTAINS:
                raise ValueError(
                    f"Operator should not be a list when the value_type is {value_type}"
                )

        # s_key = values.get('key')
        # if s_key == FilterKey.USER_LABEL:
        #     user_label_key = values.get('user_label_key')
        #     if not user_label_key:
        #         raise ValueError(f"User label key should be set when the key is {s_key}")

        return values

    def _is_match(self, zcp_alert: ZcpAlert) -> bool:
        target_value = None
        if self.key in [FilterKey.SUMMARY, FilterKey.DESCRIPTION]:
            target_value = zcp_alert.annotations.get(self.key, None)
        elif self.key in [
            FilterKey.PROJECT,
            FilterKey.PRIORITY,
            FilterKey.SEVERITY,
            FilterKey.CLUSTER,
            FilterKey.NAMESPACE,
        ]:
            target_value = zcp_alert.labels.get(self.key, None)
        elif self.key == FilterKey.SENDER:
            target_value = zcp_alert.sender
        elif self.key == FilterKey.REPEATED_COUNT:
            target_value = zcp_alert.repeated_count
        elif self.key == FilterKey.USER_LABEL:
            target_value = zcp_alert.labels.get(self.user_label_key, None)

        if not target_value:
            return False
        if not self.value:
            return False

        result = False
        if self.is_multiple_value():
            # self.value should be a list
            if self.operator == Operator.CONTAINS:
                result = target_value in self.value
        else:
            if self.operator == Operator.MATCHES:
                result = bool(re.match(self.value, target_value))
            elif self.operator == Operator.EQUALS:
                result = target_value == self.value
            elif self.operator == Operator.STARTS_WITH:
                result = target_value.startswith(self.value)
            elif self.operator == Operator.ENDS_WITH:
                result = target_value.endswith(self.value)
            elif self.operator == Operator.IS_EMPTY:
                result = not target_value
            elif self.operator == Operator.GREATER_THAN:
                if isinstance(target_value, int):
                    result = int(target_value) > int(self.value)
            elif self.operator == Operator.LESS_THAN:
                if isinstance(target_value, int):
                    result = int(target_value) < int(self.value)
        """
        ex1)
        vlaue = [1, 2, 3]
        input_value = 1
        result = input_value in value (True)
        if is_equal = True, return result (True)
        if is_equal = False, return not result (False)

        ex2)
        vlaue = [1, 2, 3]
        input_value = 4
        result = input_value in value (False)
        if is_equal = True, return result (False)
        if is_equal = False, return not result (True)
        """
        return result if self.is_equal else not result


class Integration(AlertBaseModel):
    """Alert Channel Integration model"""

    name: str = None
    channel: Union[Optional[str], Optional[Channel]] = (
        None  # Don't change it. Should be set to None by default because of the the silence list
    )
    """ Channel ID
    Case 1) When the integration is created, the channel is set as the string
    Case 2) When the integration is retrieved, the channel is set as the Channel
    """
    message_template: Optional[str] = None
    alert_actions: Optional[List[Action]] = None
    filter_mode: FilterMode = FilterMode.ALL
    alert_filters: Optional[List[Filter]] = None
    status: Optional[IntegrationStatus] = None
    modifier: Optional[str] = None

    def is_all_match(self, *, alert: ZcpAlert, action: Optional[Action] = None) -> bool:
        if action is None:
            return self.is_match_filter(alert)

        return self.is_match_action(action) and self.is_match_filter(alert)

    def is_match_action(self, action: Action) -> bool:
        return action in self.alert_actions

    def is_match_filter(self, alert: ZcpAlert) -> bool:
        if not alert:
            return False
        if not self.filter_mode:
            return False
        elif self.filter_mode == FilterMode.ALL:
            return True
        elif self.filter_mode == FilterMode.MATCH_ANY:
            # return any(f._is_match(alert) for f in self.alert_filters)
            result = False
            try:
                result = any(f._is_match(alert) for f in self.alert_filters)
            except Exception:
                ...
            return result
        elif self.filter_mode == FilterMode.MATCH_ALL:
            # return all(f._is_match(alert) for f in self.alert_filters)
            result = False
            try:
                result = all(f._is_match(alert) for f in self.alert_filters)
            except Exception:
                ...
            return result
        else:
            return False

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Integration):
            return self.id == other.id
        return False
