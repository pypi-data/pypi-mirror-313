"""
This is a constants file where we define all the configs, constant variable, etc...
"""

import os

from dotenv import load_dotenv

load_dotenv(".config")

# Logging config
LOGGER_CONFIG = "logging.conf"

# MongoDB config
MONGODB_URI = os.environ.get("MONGODB_URI")  # mandatory
MONGODB_DATABASE = os.environ.get("MONGODB_DATABASE", "alerts")
MONGODB_COLLECTION_ALERT = os.environ.get("MONGODB_COLLECTION_ALERT", "zcp_alert")
MONGODB_COLLECTION_ACTIVITY = os.environ.get(
    "MONGODB_COLLECTION_ACTIVITY", "zcp_activity"
)
MONGODB_COLLECTION_CHANNEL = os.environ.get("MONGODB_COLLECTION_CHANNEL", "zcp_channel")
MONGODB_COLLECTION_INTEGRATION = os.environ.get(
    "MONGODB_COLLECTION_INTEGRATION", "zcp_integration"
)
MONGODB_COLLECTION_SILENCE = os.environ.get("MONGODB_COLLECTION_SILENCE", "zcp_silence")
MONGODB_COLLECTION_KAKAO_TOKEN = os.environ.get(
    "MONGODB_COLLECTION_KAKAO_TOKEN", "zcp_kakao_token"
)
MONGODB_COLLECTION_BASIC_AUTH_USER = os.environ.get(
    "MONGODB_COLLECTION_BASIC_AUTH_USER", "zcp_basic_auth_user"
)
MONGODB_COLLECTION_USER_NOTIFICATION_SETTINGS = os.environ.get(
    "MONGODB_COLLECTION_USER_NOTIFICATION_SETTINGS", "zcp_user_notification_settings"
)

# App config
APP_NAME = os.environ.get("APP_NAME", "zcp-alert-backend")
APP_ROOT = os.environ.get("APP_ROOT", "/api/alert/v1")
DOCS_URL = os.environ.get("DOCS_URL", f"{APP_ROOT}/api-docs")
REDOC_URL = os.environ.get("REDOC_URL", f"{APP_ROOT}/api-redoc")
OPENAPI_URL = os.environ.get("OPENAPI_URL", f"{APP_ROOT}/openapi")
APP_TITLE = os.environ.get("APP_TITLE", "ZCP Alert Backend")
APP_VERSION = os.environ.get("APP_VERSION")  # set by helm chart automatically
APP_DESCRIPTION = os.environ.get("APP_DESCRIPTION", "ZCP Alert Backend API")

# App and Webhook config
ALERT_API_ENDPOINT = os.environ.get(
    "ALERT_API_ENDPOINT", f"http://localhost:9150{APP_ROOT}"
)  # mandatory
ALERT_CONSOLE_ENDPOINT = os.environ.get(
    "ALERT_CONSOLE_ENDPOINT", f"http://localhost:9150{APP_ROOT}"
)  # mandatory
MAX_THREAD_COUNT = int(os.environ.get("MAX_THREAD_COUNT", 100))
ALERT_VIEW_URL = os.environ.get(
    "ALERT_VIEW_URL", f"{ALERT_CONSOLE_ENDPOINT}" "/alerts/detail/{alert_id}"
)  # mandatory
WEBHOOK_DEFAULT_TIMEOUT = int(
    os.environ.get("WEBHOOK_DEFAULT_TIMEOUT", 10)
)  # in seconds
WAKEUP_SCHEDULER_INTERVAL = int(
    os.environ.get("WAKEUP_SCHEDULER_INTERVAL", 1)
)  # in minutes
WAKEUP_SCHEDULER_NAME = os.environ.get(
    "WAKEUP_SCHEDULER_NAME", "wakeup-scheduler"
)  # mandatory
# Alert system user name
ALERT_SYSTEM_USERNAME = os.environ.get("ALERT_SYSTEM_USERNAME", "System")

# OAuth2 config
KEYCLOAK_SERVER_URL = os.environ.get("KEYCLOAK_SERVER_URL")  # mandatory
KEYCLOAK_REALM = os.environ.get("KEYCLOAK_REALM")  # mandatory
KEYCLOAK_CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID", "account")  # mandatory
KEYCLOAK_CLIENT_SECRET = os.environ.get("KEYCLOAK_CLIENT_SECRET")  # mandatory
KEYCLOAK_REDIRECT_URI = os.environ.get(
    "KEYCLOAK_REDIRECT_URI", f"{ALERT_API_ENDPOINT}/oauth2/callback"
)  # mandatory only for local development

# Mandatory fields configuration for alert
MANDATORY_FIELDS_LABELS = os.environ.get(
    "MANDATORY_FIELDS_LABELS", "alertname,priority,severity"
).split(",")
MANDATORY_FIELDS_ANNOTATIONS = os.environ.get(
    "MANDATORY_FIELDS_ANNOTATIONS", "summary,description"
).split(",")

# Role config
PLATFORM_ADMIN_ROLE = os.environ.get("PLATFORM_ADMIN_ROLE", "platform-admin")
POSTFIX_MONITORING_ADMIN_ROLE = os.environ.get(
    "POSTFIX_MONITORING_ADMIN_ROLE", "monitoring-administrator"
)
ROLE_DELIMITER = os.environ.get("ROLE_DELIMITER", "..")

ALERT_ADMIN_ROLE = f"{KEYCLOAK_REALM}{ROLE_DELIMITER}{POSTFIX_MONITORING_ADMIN_ROLE}"

# Etc config
HTTP_CLIENT_SSL_VERIFY = (
    True if os.environ.get("HTTP_CLIENT_SSL_VERIFY", "true") == "true" else False
)
APP_DEBUG_MODE = os.environ.get("APP_DEBUG_MODE", "INFO").upper()
AUTH_API_ENABLED = (
    False if os.environ.get("AUTH_API_ENABLED", "false") == "false" else True
)

# third party integration config
SLACK_ACTION_ENABLED = (
    True if os.environ.get("SLACK_ACTION_ENABLED", "true") == "true" else False
)
MSTEAMS_ACTION_ENABLED = (
    True if os.environ.get("MSTEAMS_ACTION_ENABLED", "true") == "true" else False
)
GOOGLE_CHAT_ACTION_ENABLED = (
    True if os.environ.get("GOOGLE_CHAT_ACTION_ENABLED", "true") == "true" else False
)
OPEN_API_ACTION_URL = os.environ.get(
    "OPEN_API_ACTION_URL",
    f"{ALERT_API_ENDPOINT}" "/alerts/external/{alert_id}/{action}",
)  # mandatory if any of the third party integration is enabled

KAKAO_AUTH_ENDPOINT = os.environ.get("KAKAO_AUTH_ENDPOINT", "https://kauth.kakao.com")
KAKAO_API_ENDPOINT = os.environ.get("KAKAO_API_ENDPOINT", "https://kapi.kakao.com")
KAKAO_AUTH_REDIRECT_URI = os.environ.get(
    "KAKAO_AUTH_REDIRECT_URI",
    f"{ALERT_API_ENDPOINT}" "/channels/external/kakao/oauth/callback",
)
KAKAO_FRIENDS_LIMIT = int(os.environ.get("KAKAO_FRIENDS_LIMIT", 100))
# Secret key config
KAKAO_TOKEN_AES_SECRET_KEY = os.environ.get(
    "KAKAO_TOKEN_AES_SECRET_KEY",
    "425df05bf30c8434e8a619563b602a7aa0421011f71727289eee66d310897118",
)

# Notification personalization default config
USER_NOTIFICATION_DEFAULT_PRIORITIES = os.environ.get(
    "USER_NOTIFICATION_DEFAULT_PRIORITIES", "P1,P2,P3"
).split(",")
