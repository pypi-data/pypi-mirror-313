import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Optional, Tuple
from zoneinfo import ZoneInfo

from app.model.alert_model import Action, ZcpAlert
from app.model.result_model import Result
from app.settings import ALERT_VIEW_URL

# _DISPLAY_TIMEZONE = DEFAULT_TIME_ZONE
_DISPLAY_TIMEZONE = ZoneInfo("Asia/Seoul")

log = logging.getLogger("appLogger")


class EmailClient:
    def __init__(
        self,
        *,
        smtp_server: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        smtp_tls: bool | None = True,
        smtp_ssl: bool | None = False,
        from_email: str,
        from_display_name: str | None = None,
    ):
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port
        self._smtp_user = smtp_user
        self._smtp_password = smtp_password
        if smtp_tls:
            self._smtp_tls = True
            self._smtp_port = 587
        else:
            self._smtp_tls = False
        if smtp_ssl:
            self._smtp_ssl = True
            self._smtp_port = 465
        else:
            self._smtp_ssl = False
        self._from_email = from_email
        self._from_display_name = from_display_name

    def send_email(
        self,
        *,
        action: Action | None = None,
        alert: ZcpAlert,
        modifier: str | None = None,
        to_emails: list[str],
    ) -> Tuple[Result, Optional[str]]:
        message = MIMEMultipart()
        if self._from_display_name:
            message["From"] = formataddr((self._from_display_name, self._from_email))
        else:
            message["From"] = self._from_email
        message["To"] = ", ".join(to_emails)
        message["Subject"] = self._get_email_subject(
            action=action, alert=alert, modifier=modifier
        )

        message.attach(
            MIMEText(
                self._get_email_html_body(
                    action=action, alert=alert, modifier=modifier
                ),
                "html",
            )
        )

        message_string = message.as_string()
        log.debug(f"Email body: {message_string}")

        if self._smtp_tls and not self._smtp_ssl:
            try:
                with smtplib.SMTP(self._smtp_server, self._smtp_port) as server:
                    # server.set_debuglevel(1)
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(self._smtp_user, self._smtp_password)
                    server.sendmail(self._from_email, to_emails, message_string)
                    log.info("Email has been sent successfully.")
                    return Result.SUCCESS, None
            except Exception as e:
                log.error(f"An error occurred while sending the email: {e}")
                return Result.FAILED, str(e)
        elif self._smtp_ssl and not self._smtp_tls:
            try:
                with smtplib.SMTP_SSL(self._smtp_server, self._smtp_port) as server:
                    server.login(self._smtp_user, self._smtp_password)
                    server.sendmail(self._from_email, to_emails, message_string)
                    log.info("Email has been sent successfully.")
                    return Result.SUCCESS, None
            except Exception as e:
                log.error(f"An error occurred while sending the email: {e}")
                return Result.FAILED, str(e)
        else:
            log.error("Please set either smtp_tls or smtp_ssl to True.")
            return Result.FAILED, "Please set either smtp_tls or smtp_ssl to True."

    def _get_email_subject(
        self,
        *,
        action: Action | None = None,
        alert: ZcpAlert,
        modifier: str | None = None,
    ) -> str:
        subject = ""
        if action is None:
            subject = f"[{alert.status.value}] {alert.annotations['summary']
                    if alert.annotations.get('summary')
                    else 'N/A'}"
            if alert.repeated_count > 0:
                subject += f" (repeated {alert.repeated_count} times)"
        else:
            status_tilte = ""
            if action == Action.UNACK:
                status_tilte = "Unacked"
            elif action == Action.WAKEUP:
                status_tilte = "Woken"
            else:
                status_tilte = alert.status.value
            subject = f"[{status_tilte} by {modifier if modifier else ""}] {alert.annotations['summary']
                    if alert.annotations.get('summary')
                    else 'N/A'}"

        return subject

    def _get_email_html_body(
        self,
        *,
        action: Action | None = None,
        alert: ZcpAlert,
        modifier: str | None = None,
    ) -> str:
        body = (
            f"<!DOCTYPE html>"
            f"<html lang=\"en\">"
            f"{self._get_email_head()}"
            f"<body>"
            f"<!-- Alert Header -->"
            f"<div class=\"alert-header\">"
            f"        <img src=\"https://fonts.gstatic.com/s/e/notoemoji/15.1/1f6a8/512.png=s6\" alt=\"Alert Icon\" width=\"24\" height=\"24\">"
            f"        <span>{self._get_email_subject(action=action, alert=alert, modifier=modifier)}</span>"
            f"    </div>"
            f"    <!-- Alert Description -->"
            f"    <div class=\"alert-description\">"
            f"        <a href=\"{ALERT_VIEW_URL.format(alert_id=alert.id)}\">{alert.annotations['description'] if alert.annotations.get('description') else 'N/A'}</a>"
            f"    </div>"
            f"    <!-- Alert Information -->"
            f"    <div class=\"container\">"
            f"        <div class=\"section\">"
            f"            <p><strong>Priority:</strong> {alert.labels['priority'] if alert.labels.get('priority') else 'N/A'}</p>"
            f"            <p><strong>Cluster:</strong> {alert.labels['cluster'] if alert.labels.get('cluster') else 'N/A'}</p>"
            f"            <p><strong>Occurred At:</strong> {alert.starts_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds') if alert.starts_at else 'N/A'}</p>"
            f"            <p><strong>Sender:</strong> {alert.sender.value if alert.sender else 'N/A'}</p>"
            f"        </div>"
            f"        <div class=\"section\">"
            f"            <p><strong>Severity:</strong> {alert.labels['severity'] if alert.labels.get('severity') else 'N/A'}</p>"
            f"            <p><strong>Namespace:</strong> {alert.labels['namespace'] if alert.labels.get('namespace') else 'N/A'}</p>"
            f"            <p><strong>Triggered At:</strong> {alert.created_at.astimezone(_DISPLAY_TIMEZONE).isoformat(timespec='milliseconds') if alert.created_at else 'N/A'}</p>"
            f"            <p><strong>ID:</strong> {alert.id}</p>"
            f"        </div>"
            f"    </div>"
            f"    <!-- Detail Information -->"
            f"    <div class=\"details\">"
            f"        <p><strong>Detail informations</strong></p>"
            f"        <ul>"
            f"            {self._get_email_body_labels(labels=alert.labels)}"
            f"        </ul>"
            f"    </div>"
            f"</body>"
            f"</html>"
        )

        return body

    def _get_email_head(
        self,
    ) -> str:
        return """<head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Alert Notification</title>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 20px;
                        }
                        .alert-header {
                            display: flex;
                            align-items: center;
                            font-size: 18px;
                            font-weight: bold;
                            margin-bottom: 10px;
                        }
                        .alert-header img {
                            margin-right: 10px;
                        }
                        .alert-description {
                            color: #007bff;
                            margin-bottom: 20px;
                        }
                        .container {
                            display: flex;
                            justify-content: space-between;
                            margin-bottom: 20px;
                            width: 60%;
                        }
                        .section {
                            width: 45%;
                        }
                        .section p {
                            margin: 5px 0;
                        }
                        .details {
                            margin-top: 20px;
                        }
                        .details ul {
                            list-style-type: disc;
                            padding-left: 20px;
                        }
                    </style>
                </head>"""

    def _get_email_body_labels(self, *, labels: dict[str, str]) -> str:
        body = ""
        for key, value in labels.items():
            body += f"<li>{key}: {value}</li>"
        return body

    def send_test_email(
        self,
        *,
        modifier: str | None = None,
        to_emails: list[str],
    ) -> Tuple[Result, Optional[str]]:
        message = MIMEMultipart()
        if self._from_display_name:
            message["From"] = formataddr((self._from_display_name, self._from_email))
        else:
            message["From"] = self._from_email
        message["To"] = ", ".join(to_emails)
        message["Subject"] = "Test Email from ZCP Alert Manager"

        message.attach(
            MIMEText("<p>This is a test email from ZCP Alert Manager.</p>", "html")
        )

        message_string = message.as_string()
        log.debug(f"Email body: {message_string}")

        if self._smtp_tls and not self._smtp_ssl:
            try:
                with smtplib.SMTP(self._smtp_server, self._smtp_port) as server:
                    # server.set_debuglevel(1)
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    server.login(self._smtp_user, self._smtp_password)
                    server.sendmail(self._from_email, to_emails, message_string)
                    log.info("Email has been sent successfully.")
                    return Result.SUCCESS, None
            except Exception as e:
                log.error(f"An error occurred while sending the email: {e}")
                return Result.FAILED, str(e)
        elif self._smtp_ssl and not self._smtp_tls:
            try:
                with smtplib.SMTP_SSL(self._smtp_server, self._smtp_port) as server:
                    server.login(self._smtp_user, self._smtp_password)
                    server.sendmail(self._from_email, to_emails, message_string)
                    log.info("Email has been sent successfully.")
                    return Result.SUCCESS, None
            except Exception as e:
                log.error(f"An error occurred while sending the email: {e}")
                return Result.FAILED, str(e)
        else:
            log.error("Please set either smtp_tls or smtp_ssl to True.")
            return Result.FAILED, "Please set either smtp_tls or smtp_ssl to True."
