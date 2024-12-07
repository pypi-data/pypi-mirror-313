import logging
from datetime import datetime
from typing import List

from app import settings
from app.db import AlertRepository
from app.exception.common_exception import AlertBackendException, AlertError
from app.model.alert_model import AlertStatus
from app.thread.threadpool_executor import get_executor

log = logging.getLogger("appLogger")
logging.getLogger("matplotlib.font_manager").setLevel(logging.INFO)


class ReportService:
    """ReportService class"""

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

        self.__initiated = True

        self.__executor = get_executor()

        log.info(f"{__name__} ReportService Initialized")

    def get_number_of_alerts_by_status(
        self, *, excludes_status: List[AlertStatus]
    ) -> list[dict]:
        """Get the number of alerts by status

        Parameters
        ----------
        excludes_status : List[AlertStatus]

        Returns
        -------
        list[dict]
        """
        return self.__alert_repository.find_number_by_status(
            excludes_status=excludes_status
        )

    def get_number_of_alerts_by_label(
        self, *, key_label: str, excludes_status: List[AlertStatus], limit: int = 10
    ) -> list[dict]:
        """Get the number of alerts by status

        Parameters
        ----------
        excludes_status : List[AlertStatus]

        Returns
        -------
        list[dict]
        """
        return self.__alert_repository.find_number_by_label(
            key_label=key_label, excludes_status=excludes_status, limit=limit
        )

    def get_number_of_alerts_by_priority_trend_data(
        self, *, start_date: datetime, end_date: datetime
    ) -> dict:
        """Get the number of alerts by priority per date

        Parameters
        ----------
        start_date : str
        end_date : str

        Returns
        -------
        dict
        """
        return self.__alert_repository.find_number_by_priority_per_date(
            start_date=start_date, end_date=end_date
        )

    def get_number_of_alerts_for_mttar(
        self, *, date_field: str, start_date: datetime, end_date: datetime
    ) -> int:
        """Get the number of alerts MTTAR (created, acknowledged, closed) with period

        Parameters
        ----------
        date_field : str
        start_date : datetime
        end_date : datetime

        Returns
        -------
        dict
        """
        return self.__alert_repository.find_number_for_mttar(
            date_field=date_field, start_date=start_date, end_date=end_date
        )

    def get_alerts_mttar(
        self, *, type: str, start_date: datetime, end_date: datetime
    ) -> int:
        """Get the number of alerts MTTAR with period

        Parameters
        ----------
        type : str
            MTTA is Mean Time To Acknowledge
            MTTR is Mean Time To Resolve
        start_date : datetime
        end_date : datetime

        Returns
        -------
        int
            mean time to acknowledge or resolve in milliseconds
        """
        if type == "MTTA":
            return self.__alert_repository.find_mtta(
                start_date=start_date, end_date=end_date
            )
        elif type == "MTTR":
            return self.__alert_repository.find_mttr(
                start_date=start_date, end_date=end_date
            )
        else:
            raise AlertBackendException(
                AlertError.BAD_REQUEST, details=f"Invalid type({type})"
            )

    def get_alerts_mtta_trend_data(
        self, *, start_date: datetime, end_date: datetime
    ) -> dict:
        """Get the number of alerts MTTA per date
        Parameters
        ----------
        start_date : str
        end_date : str

        Returns
        -------
        dict
        """
        return self.__alert_repository.find_mtta_number_per_date(
            start_date=start_date, end_date=end_date
        )

    def get_alerts_mttr_trend_data(
        self, *, start_date: datetime, end_date: datetime
    ) -> dict:
        """Get the number of alerts MTTR per date
        Parameters
        ----------
        start_date : str
        end_date : str

        Returns
        -------
        dict
        """
        return self.__alert_repository.find_mttr_number_per_date(
            start_date=start_date, end_date=end_date
        )
