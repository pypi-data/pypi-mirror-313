from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from app.model.alert_model import Priority


class UserNotificationSettingsRequest(BaseModel):
    id: Optional[str] = Field(
        None,
        max_length=24,
        min_length=24,
        description="Obect ID received from the server",
    )
    projects: Optional[List[str]] = None
    clusters: Optional[List[str]] = None
    priorities: List[Priority]
    labels: Optional[Dict[str, str]] = None
