"""
This module contains the standard time format for the application.
"""

from datetime import timezone

DEFAULT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
"""Default time format and time zone %Y-%m-%dT%H:%M:%S%z"""
DEFAULT_TIME_ZONE = timezone.utc
"""Default time zone is UTC(+00:00)"""
