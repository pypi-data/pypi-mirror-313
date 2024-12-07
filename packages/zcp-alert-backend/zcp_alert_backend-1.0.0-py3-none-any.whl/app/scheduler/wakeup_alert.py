import logging
import threading
import time

import schedule

import app.settings as settings
from app.service import AlertService

log = logging.getLogger("appLogger")

_service = AlertService()


def job():
    _service.wake_up_alerts_snoozed_time_over(modifier=settings.WAKEUP_SCHEDULER_NAME)


def run_scheduler():
    schedule.every(settings.WAKEUP_SCHEDULER_INTERVAL).minutes.do(job)
    log.info(
        f"Scheduler started with interval {settings.WAKEUP_SCHEDULER_INTERVAL} minutes"
    )

    while True:
        schedule.run_pending()
        time.sleep(1)


def start_scheduler():
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
