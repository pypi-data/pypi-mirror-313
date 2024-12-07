from typing import Dict, List, Optional

from app.model.alert_model import AlertBaseModel, Priority, ZcpAlert


class UserNotificationSettings(AlertBaseModel):
    username: str
    projects: Optional[List[str]] = None
    clusters: Optional[List[str]] = None
    priorities: Optional[List[Priority]] = None
    labels: Optional[Dict[str, str]] = None

    def is_match(self, zcp_alert: ZcpAlert) -> bool:
        if self.projects and zcp_alert.labels.get("project", "") not in self.projects:
            return False
        if self.clusters and zcp_alert.labels.get("cluster", "") not in self.clusters:
            return False
        if (
            self.priorities
            and zcp_alert.labels.get("priority", "") not in self.priorities
        ):
            return False
        if self.labels:
            for key, value in self.labels.items():
                alert_value = zcp_alert.labels.get(key, None)
                if alert_value is None or alert_value != value:
                    return False
        return True
