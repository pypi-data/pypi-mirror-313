import logging
from datetime import datetime, timedelta
from typing import List, Optional, Union

import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from app.db.base_repository import BaseRepository
from app.db.exceptions import (
    InvalidObjectIDException,
    ObjectNotFoundException,
    ValueErrorException,
)
from app.db.search_utils import get_escaped_regex_pattern
from app.model.alert_model import (
    AlertSortField,
    AlertStatus,
    RepeatedCountOperator,
    ZcpAlert,
)

# special import
from app.schema.alert_request_model import AlertSearchRequest
from app.utils.list_utils import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_SIZE, SortDirection
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")


class AlertRepository(BaseRepository):
    """AlertRepository class to handle alert"""

    def __init__(
        self, *, collection: str, aggregation_collection: Optional[str] = None
    ):
        super().__init__(
            collection=collection, aggregation_collection=aggregation_collection
        )

    @classmethod
    def from_config(cls, *, collection: str) -> "AlertRepository":
        """Create AlertRepository instance from configuration"""
        return cls(collection=collection)

    @classmethod
    def from_config_with_aggregation(
        cls, *, collection: str, aggregation_collection: str
    ) -> "AlertRepository":
        """Create AlertRepository instance with aggregation collection from configuration"""
        return cls(collection=collection, aggregation_collection=aggregation_collection)

    def __call__(self) -> "AlertRepository":
        indexes = self._collection.list_indexes()

        unique_index_name = "unique_key_fingerprint"

        unique_index_exists = False
        for index in indexes:
            if index["name"] == unique_index_name and index.get("unique", True):
                unique_index_exists = True
                break

        if not unique_index_exists:
            self._collection.create_index(
                "fingerprint", name=unique_index_name, unique=True
            )

        return self

    def find(
        self,
        *,
        alert_search_request: Optional[AlertSearchRequest],
        page_number: Optional[int],
        page_size: Optional[int],
    ) -> List[ZcpAlert]:
        """Find all alert requests

        Args:
            alert_search_request (AlertSearchRequest): alert search request

        Returns:
            List[ZcpAlert]: list of ZcpAlert instances
        """

        query = self.__find_query(alert_search_request)

        log.debug(f"Query: {query}")

        if page_number < 1:
            page_number = DEFAULT_PAGE_NUMBER
        if page_size < 1:
            page_size = DEFAULT_PAGE_SIZE

        skip, limit = (page_size * (page_number - 1), page_size)

        log.debug(f"page_number={page_number}, page_size={page_size}")
        log.debug(f"skip: {skip}, limit: {limit}")

        sort_field = self.__find_sort_field(alert_search_request.sort_field)
        direction = (
            pymongo.ASCENDING
            if alert_search_request.sort_direction == SortDirection.ASC
            else pymongo.DESCENDING
        )

        log.debug(
            f"sort_field: {sort_field}, direction: {alert_search_request.sort_direction} ({direction})"
        )

        cursor = (
            self._collection.find(query)
            .sort(sort_field, direction)
            .skip(skip)
            .limit(limit)
        )
        zcp_alerts = [
            ZcpAlert(**document) for document in cursor if document is not None
        ]

        return zcp_alerts

    def count(
        self,
        *,
        alert_search_request: Optional[AlertSearchRequest],
    ) -> int:
        """Count all alert requests

        Args:
            alert_search_request (AlertSearchRequest): alert search request

        Returns:
            int: count of ZcpAlert instances
        """
        query = self.__find_query(alert_search_request)

        log.debug(f"Query: {query}")

        return self._collection.count_documents(filter=query)

    def __find_sort_field(self, sort_field: AlertSortField) -> str:
        switcher = {
            AlertSortField.SENDER: "sender",
            AlertSortField.STATUS: "status",
            AlertSortField.REPEATED_COUNT: "repeated_count",
            AlertSortField.ALERT_NAME: "labels.alertname",
            AlertSortField.SUMMARY: "annotations.summary",
            AlertSortField.PRIORITY: "labels.priority",
            AlertSortField.SEVERITY: "labels.severity",
            AlertSortField.CREATED_AT: "created_at",
            AlertSortField.UPDATED_AT: "updated_at",
            AlertSortField.CLOSED_AT: "closed_at",
            AlertSortField.ACKNOWLEDGED_AT: "acknowledged_at",
        }
        return switcher.get(sort_field, "updated_at")

    def __find_query(
        self,
        alert_search_request: Optional[AlertSearchRequest],
    ) -> dict:
        query = {}
        # search by common fields
        query.update(
            {"status": {"$in": [s.value for s in alert_search_request.statuses]}}
        ) if alert_search_request.statuses else None
        query.update(
            {"sender": {"$in": [s.value for s in alert_search_request.senders]}}
        ) if alert_search_request.senders else None
        query.update(
            {"fingerprint": alert_search_request.fingerprint}
        ) if alert_search_request.fingerprint else None
        query.update(
            {"_id": ObjectId(alert_search_request.alert_id)}
        ) if alert_search_request.alert_id else None

        # search by repeated_count and repeated_count_operator
        if (
            alert_search_request.repeated_count is not None
            and alert_search_request.repeated_count_operator is not None
        ):
            query.update(
                {"repeated_count": {"$gt": alert_search_request.repeated_count}}
            ) if alert_search_request.repeated_count_operator == RepeatedCountOperator.GT else None
            query.update(
                {"repeated_count": {"$lt": alert_search_request.repeated_count}}
            ) if alert_search_request.repeated_count_operator == RepeatedCountOperator.LT else None
            query.update(
                {"repeated_count": {"$gte": alert_search_request.repeated_count}}
            ) if alert_search_request.repeated_count_operator == RepeatedCountOperator.GTE else None
            query.update(
                {"repeated_count": {"$lte": alert_search_request.repeated_count}}
            ) if alert_search_request.repeated_count_operator == RepeatedCountOperator.LTE else None

        # search by labels
        query.update(
            {
                "labels.priority": {
                    "$in": [p.value for p in alert_search_request.priorities]
                }
            }
        ) if alert_search_request.priorities else None
        query.update(
            {
                "labels.severity": {
                    "$in": [s.value for s in alert_search_request.severities]
                }
            }
        ) if alert_search_request.severities else None
        query.update(
            {"labels.project": alert_search_request.project}
        ) if alert_search_request.project else None
        query.update(
            {"labels.cluster": {"$in": [c for c in alert_search_request.clusters]}}
        ) if alert_search_request.clusters else None
        query.update(
            {"labels.namespace": {"$in": [n for n in alert_search_request.namespaces]}}
        ) if alert_search_request.namespaces else None
        query.update(
            {
                "labels.alertname": {
                    "$regex": get_escaped_regex_pattern(alert_search_request.alertname),
                    "$options": "i",
                }
            }
        ) if alert_search_request.alertname else None

        # search by labels added by user
        if alert_search_request.parsed_labels:
            for label in alert_search_request.parsed_labels:
                query.update({f"labels.{label.key}": label.value})

        # search by annotations
        query.update(
            {
                "annotations.summary": {
                    "$regex": get_escaped_regex_pattern(alert_search_request.summary),
                    "$options": "i",
                }
            }
        ) if alert_search_request.summary else None
        query.update(
            {
                "annotations.description": {
                    "$regex": get_escaped_regex_pattern(
                        alert_search_request.description
                    ),
                    "$options": "i",
                }
            }
        ) if alert_search_request.description else None

        # search by perioid with created_at, updated_at and closed_at
        # search by updated_at
        if alert_search_request.start_date and alert_search_request.end_date:
            query.update(
                {
                    "updated_at": {
                        "$gte": alert_search_request.start_date,
                        "$lte": alert_search_request.end_date,
                    }
                }
            )
        elif alert_search_request.start_date and not alert_search_request.end_date:
            query.update({"updated_at": {"$gte": alert_search_request.start_date}})
        elif not alert_search_request.start_date and alert_search_request.end_date:
            query.update({"updated_at": {"$lte": alert_search_request.end_date}})

        # search by created_at
        if (
            alert_search_request.start_date_created_at
            and alert_search_request.end_date_created_at
        ):
            query.update(
                {
                    "created_at": {
                        "$gte": alert_search_request.start_date_created_at,
                        "$lte": alert_search_request.end_date_created_at,
                    }
                }
            )
        elif (
            alert_search_request.start_date_created_at
            and not alert_search_request.end_date_created_at
        ):
            # query.update({"created_at": {"$gte": alert_search_request.start_date_created_at}})
            query.update(
                {"created_at": {"$gte": alert_search_request.start_date_created_at}}
            )
        elif (
            not alert_search_request.start_date_created_at
            and alert_search_request.end_date_created_at
        ):
            query.update(
                {"created_at": {"$lte": alert_search_request.end_date_created_at}}
            )

        # search by closed_at
        if (
            alert_search_request.start_date_closed_at
            and alert_search_request.end_date_closed_at
        ):
            query.update(
                {
                    "closed_at": {
                        "$gte": alert_search_request.start_date_closed_at,
                        "$lte": alert_search_request.end_date_closed_at,
                    }
                }
            )
        elif (
            alert_search_request.start_date_closed_at
            and not alert_search_request.end_date_closed_at
        ):
            query.update(
                {"closed_at": {"$gte": alert_search_request.start_date_closed_at}}
            )
        elif (
            not alert_search_request.start_date_closed_at
            and alert_search_request.end_date_closed_at
        ):
            query.update(
                {"closed_at": {"$lte": alert_search_request.end_date_closed_at}}
            )

        return query

    def find_by_id(self, object_id: str) -> ZcpAlert:
        """Find one alert request by object id

        Args:
            object_id (str): object id

        Returns:
            ZcpAlert: ZcpAlert instance

        Raises:
            ObjectNotFoundException: if alert is not found
            InvalidObjectIDException: if object id is invalid
        """
        try:
            query = {"_id": ObjectId(object_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        document = self._collection.find_one(query)

        if document is None:
            raise ObjectNotFoundException(object_id)

        return ZcpAlert(**document)

    def find_by_fingerprint(self, fingerprint: str) -> ZcpAlert:
        """Check if alert exists or not using fingerprint

        Args:
            fingerprint (str): fingerprint

        Returns:
            ZcpAlert: ZcpAlert instance if alert exists otherwise None
        """
        query = {"fingerprint": fingerprint}
        document = self._collection.find_one(query)

        if document is None:
            return None

        return ZcpAlert(**document)

    def find_by_snoozed_time_over(self) -> List[ZcpAlert]:
        """Find all alert which snoozed time is over

        Returns
        -------
        List[ZcpAlert]
        """
        query = {
            "status": AlertStatus.SNOOZED.value,
            "snoozed_until_at": {"$lt": datetime.now(DEFAULT_TIME_ZONE)},
        }

        log.debug(f"Query: {query}")

        cursor = self._collection.find(query)
        zcp_alerts = [
            ZcpAlert(**document) for document in cursor if document is not None
        ]

        return zcp_alerts

    def insert(self, zcp_alert: ZcpAlert) -> str:
        """Insert one alert request

        Args:
            alert (ZcpAlert): ZcpAlert instance

        Returns:
            str: object id
        """
        if zcp_alert.created_at is None:
            zcp_alert.created_at = datetime.now(DEFAULT_TIME_ZONE)
        if zcp_alert.updated_at is None:
            zcp_alert.updated_at = datetime.now(DEFAULT_TIME_ZONE)

        # model_dump will convert datetime to string
        # so we need to set again datetime filed with datetime object
        alert_dict = zcp_alert.model_dump(by_alias=True, exclude=["id"])
        alert_dict.update(
            {"created_at": zcp_alert.created_at, "updated_at": zcp_alert.updated_at}
        )
        alert_dict.update(
            {"starts_at": zcp_alert.starts_at, "ends_at": zcp_alert.ends_at}
        )

        try:
            result = self._collection.insert_one(alert_dict)
        except DuplicateKeyError as e:
            raise ValueErrorException(f"Alert already exists: {e}")

        return str(result.inserted_id)

        # return str(self._collection.insert_one(zcp_alert.model_dump(by_alias=True, exclude=['id'])).inserted_id)

    def update(self, zcp_alert: ZcpAlert) -> ZcpAlert:
        """Update one alert request

        Can not update the labels deleted when a labels has been removed
        See : https://www.mongodb.com/docs/manual/reference/operator/update/set/#mongodb-update-up.-set

        Args:
            zcp_alert (ZcpAlert): ZcpAlert instance

        Returns:
            ZcpAlert: ZcpAlert instance

        Raises:
            ObjectNotFoundException: if alert is not found
            InvalidObjectIDException: if object id is invalid
        """
        try:
            filters = {"_id": ObjectId(zcp_alert.id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        if zcp_alert.updated_at is None:
            zcp_alert.updated_at = datetime.now(DEFAULT_TIME_ZONE)

        # model_dump will convert datetime to string
        # so we need to set again datetime filed with datetime object
        alert_dict = zcp_alert.model_dump(
            by_alias=True,
            exclude=[
                "id",
                "created_at",
                "closed_at",
                "acknowledged_at",
                "snoozed_until_at",
            ],
        )
        alert_dict.update({"updated_at": zcp_alert.updated_at})
        alert_dict.update(
            {"starts_at": zcp_alert.starts_at, "ends_at": zcp_alert.ends_at}
        )
        alert_dict.update({"created_at": zcp_alert.created_at})
        alert_dict.update({"closed_at": zcp_alert.closed_at})
        alert_dict.update({"acknowledged_at": zcp_alert.acknowledged_at})
        alert_dict.update({"snoozed_until_at": zcp_alert.snoozed_until_at})

        update = [
            # {"$set": zcp_alert.model_dump(by_alias=True, exclude=['id', 'created_at', 'closed_at'])},
            {"$set": alert_dict},
        ]

        log.debug(f"Update pipeline: {update}")

        try:
            document = self._collection.find_one_and_update(
                filters, update, return_document=ReturnDocument.AFTER
            )
        except DuplicateKeyError as e:
            raise ValueErrorException(f"Alert already exists: {e}")

        if document is None:
            raise ObjectNotFoundException(zcp_alert.id)

        return ZcpAlert(**document)

    def update_status(
        self,
        *,
        alert_id: str = None,
        alert_ids: List[str] = None,
        status: AlertStatus,
        modifier: str,
        snoozed_until_at: datetime = None,
    ) -> Union[ZcpAlert, int]:
        """Update status of alert request by alert id or alert ids

        Args:
            alert_id (str): alert id
            alert_ids (List[str]): list of alert ids
            status (AlertStatus): alert status
            modifier (str): modifier
            snoozed_until_at (datetime): snoozed until at

        Returns:
            Union[ZcpAlert, int]: ZcpAlert instance if alert_id is provided otherwise int

        Raises:
            ObjectNotFoundException: if alert is not found
            InvalidObjectIDException: if object id is invalid
            ValueErrorException: if alert_id or alert_ids is not provided
        """
        current_time = datetime.now(DEFAULT_TIME_ZONE)

        if alert_id is not None:
            """
            Update status of alert request by alert id (single action)
            Suported for all actions
            """
            if self.find_by_id(alert_id) is None:
                raise ObjectNotFoundException(alert_id)

            filters = {"_id": ObjectId(alert_id)}

            alert_dict = {}
            alert_dict.update({"status": status})
            alert_dict.update({"updated_at": current_time})
            alert_dict.update({"modifier": modifier})

            if status == AlertStatus.CLOSED:
                alert_dict.update({"closed_at": current_time, "snoozed_until_at": None})
            if status == AlertStatus.ACKED:
                alert_dict.update(
                    {"acknowledged_at": current_time, "snoozed_until_at": None}
                )
            if (
                status == AlertStatus.OPEN
            ):  # when a user unacknowledges an alert or wake-up scheduler wakes up an alert
                alert_dict.update({"acknowledged_at": None, "snoozed_until_at": None})
            if status == AlertStatus.SNOOZED and snoozed_until_at is not None:
                alert_dict.update({"snoozed_until_at": snoozed_until_at})

            update = [
                {"$set": alert_dict},
            ]

            log.debug(f"Update pipeline for alert_id : {update}")

            document = self._collection.find_one_and_update(
                filters, update, return_document=ReturnDocument.AFTER
            )
            if document is not None:
                return ZcpAlert(**document)

        if alert_ids is not None and len(alert_ids) > 0:
            """
            Update status of alert requests by alert ids (bulk update)
            Supported only for Acknowledge and Close actions
            """
            try:
                filters = {
                    "_id": {"$in": [ObjectId(alert_id) for alert_id in alert_ids]}
                }
            except InvalidId as e:
                raise InvalidObjectIDException(e)

            alert_dict = {}
            alert_dict.update({"status": status})
            alert_dict.update({"updated_at": current_time})
            alert_dict.update({"modifier": modifier})

            if status == AlertStatus.CLOSED:
                alert_dict.update({"closed_at": current_time, "snoozed_until_at": None})
            if status == AlertStatus.ACKED:
                alert_dict.update(
                    {"acknowledged_at": current_time, "snoozed_until_at": None}
                )
            if status == AlertStatus.OPEN:  # when wake-up scheduler wakes up an alert
                alert_dict.update({"acknowledged_at": None, "snoozed_until_at": None})

            update = [
                {"$set": alert_dict},
            ]

            log.debug(f"Update pipeline for alert_ids : {update}")

            return self._collection.update_many(filters, update).modified_count

        return -1

    def find_by_ids(self, alert_ids: List[str]) -> List[ZcpAlert]:
        """Find all alert requests by alert ids

        Args:
            alert_ids (List[str]): list of alert ids

        Returns:
            List[ZcpAlert]: list of ZcpAlert instances

        Raises:
            InvalidObjectIDException: if object id is invalid
        """
        try:
            query = {"_id": {"$in": [ObjectId(alert_id) for alert_id in alert_ids]}}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        cursor = self._collection.find(query)
        zcp_alerts = [
            ZcpAlert(**document) for document in cursor if document is not None
        ]

        return zcp_alerts

    def delete_by_id(self, object_id: str) -> bool:
        """Delete one alert request by object id

        Args:
            object_id (str): object id

        Returns:
            bool: True if deleted otherwise False

        Raises:
            ObjectNotFoundException: if alert is not found
            InvalidObjectIDException: if object id is invalid
        """
        # check if object_id is valid
        try:
            query = {"_id": ObjectId(object_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        # check if document exists
        document = self._collection.find_one_and_delete(query)

        if document is None:
            raise ObjectNotFoundException(object_id)

        return True

    def find_number_by_status(
        self, *, excludes_status: List[AlertStatus] = None
    ) -> list[dict]:
        """Find number of alert requests by status

        Parameters
        ----------
        excludes_status : List[AlertStatus], optional

        Returns
        -------
        list[dict]
        """
        group_field = "status"
        pipeline = []
        if excludes_status and len(excludes_status) > 0:
            pipeline.append(
                {"$match": {"status": {"$nin": [s.value for s in excludes_status]}}}
            )

        pipeline.append({"$group": {"_id": f"${group_field}", "count": {"$sum": 1}}})
        pipeline.append({"$sort": {"count": -1}})

        documents = self._collection.aggregate(pipeline)

        data = []
        for doc in documents:
            data.append({"status": doc.get("_id"), "count": doc.get("count")})

        return data

    def find_number_by_label(
        self,
        *,
        key_label: str,
        excludes_status: List[AlertStatus] = None,
        limit: int = 10,
    ) -> list[dict]:
        """Find number of alert requests by label

        Parameters
        ----------
        key_label : str
        excludes_status : List[AlertStatus], optional
        limit : int, optional

        Returns
        -------
        list[dict]
        """
        group_field = f"labels.{key_label}"
        pipeline = []
        if excludes_status and len(excludes_status) > 0:
            pipeline.append(
                {
                    "$match": {
                        group_field: {"$ne": None},
                        "status": {"$nin": [s.value for s in excludes_status]},
                    }
                }
            )
        else:
            pipeline.append({"$match": {group_field: {"$ne": None}}})

        pipeline.append({"$group": {"_id": f"${group_field}", "count": {"$sum": 1}}})
        pipeline.append({"$sort": {"count": -1}})
        pipeline.append({"$limit": limit})

        log.debug(f"Pipeline: {pipeline}")

        documents = self._collection.aggregate(pipeline)

        data = []
        for doc in documents:
            data.append({f"{key_label}": doc.get("_id"), "count": doc.get("count")})

        return data

    def find_number_by_priority_per_date(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> dict:
        """Find number of alert requests by date and priority

        Args:
            start_date (datetime): start date
            end_date (datetime): end date

        Returns:
            dict: count of alert requests by date and priority
        """
        log.debug(
            f"Start date: {start_date}, End date: {end_date} range: {range((end_date - start_date).days + 1)}"
        )
        date_range = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((end_date - start_date).days + 1)
        ]

        pipeline = [
            {"$match": {"created_at": {"$gte": start_date, "$lte": end_date}}},
            {
                "$group": {
                    "_id": {
                        "date": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$created_at",
                            }
                        },
                        "priority": "$labels.priority",
                    },
                    "count": {"$sum": 1},
                }
            },
            {
                "$group": {
                    "_id": "$_id.date",
                    "priorities": {
                        "$push": {"priority": "$_id.priority", "count": "$count"}
                    },
                }
            },
            {"$sort": {"_id": 1}},
        ]

        log.debug(f"Pipeline: {pipeline}")

        documents = self._collection.aggregate(pipeline)

        data = {}
        for doc in documents:
            date = doc["_id"]
            priority_counts = {
                priority["priority"]: priority["count"]
                for priority in doc["priorities"]
            }
            data[date] = priority_counts

        final_data = {}

        for date in date_range:
            if date not in data:
                final_data[date] = {"P1": 0, "P2": 0, "P3": 0, "P4": 0, "P5": 0}
            else:
                data[date]["P1"] = data[date].get("P1", 0)
                data[date]["P2"] = data[date].get("P2", 0)
                data[date]["P3"] = data[date].get("P3", 0)
                data[date]["P4"] = data[date].get("P4", 0)
                data[date]["P5"] = data[date].get("P5", 0)

                final_data[date] = data[date]

        return final_data

    def find_number_for_mttar(
        self,
        *,
        date_field: str,
        start_date: datetime,
        end_date: datetime,
    ) -> int:
        """Find number of alert requests with period

        Args:
            date_field (str): date_field (CREATED, ACKNOWLEDGED, CLOSED)
            start_date (datetime): start date
            end_date (datetime): end date

        Returns:
            int: count of alert requests
        """

        if date_field not in ["CREATED", "ACKNOWLEDGED", "CLOSED"]:
            raise ValueError(
                f"Invalid date kind: {date_field}."
                "It should be one of ['CREATED', 'ACKNOWLEDGED', 'CLOSED']"
            )
        if date_field == "CREATED":
            date_field = "created_at"
        elif date_field == "ACKNOWLEDGED":
            date_field = "acknowledged_at"
        elif date_field == "CLOSED":
            date_field = "closed_at"
        else:
            raise ValueError(f"Invalid date field: {date_field}.")

        query = {}
        query.update({"created_at": {"$gte": start_date, "$lte": end_date}})

        if date_field != "created_at":
            query.update({date_field: {"$gte": start_date, "$lte": end_date}})

        log.debug(f"Query: {query}")

        count = self._collection.count_documents(query)

        return count

    def find_mtta(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> float:
        """Find number of alert requests MTTA with period

        Parameters
        ----------
        start_date : datetime
        end_date : datetime

        Returns
        -------
        float : minutes
        """

        pipeline = []
        pipeline.append(
            {
                "$match": {
                    "acknowledged_at": {"$ne": None},
                    "created_at": {"$gte": start_date, "$lte": end_date},
                }
            }
        )
        pipeline.append(
            {
                "$project": {
                    "timeDifference": {"$subtract": ["$acknowledged_at", "$created_at"]}
                }
            }
        )
        pipeline.append(
            {
                "$group": {
                    "_id": None,
                    "averageTimeDifference": {"$avg": "$timeDifference"},
                }
            }
        )

        log.debug(f"Pipeline: {pipeline}")

        result = list(self._collection.aggregate(pipeline))

        if result:
            return self._transform_milliseconds_to_minutes(
                result[0]["averageTimeDifference"]
            )

    def find_mttr(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> float:
        """Find number of alert requests MTTR with period

        Parameters
        ----------
        start_date : datetime
        end_date : datetime

        Returns
        -------
        float : minutes
        """
        pipeline = []
        pipeline.append(
            {
                "$match": {
                    "closed_at": {"$ne": None},
                    "created_at": {"$gte": start_date, "$lte": end_date},
                    "status": AlertStatus.CLOSED.value,
                }
            }
        )
        pipeline.append(
            {
                "$project": {
                    "timeDifference": {"$subtract": ["$closed_at", "$created_at"]}
                }
            }
        )
        pipeline.append(
            {
                "$group": {
                    "_id": None,
                    "averageTimeDifference": {"$avg": "$timeDifference"},
                }
            }
        )

        log.debug(f"Pipeline: {pipeline}")

        result = list(self._collection.aggregate(pipeline))

        if result:
            return self._transform_milliseconds_to_minutes(
                result[0]["averageTimeDifference"]
            )

    def find_mtta_number_per_date(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> dict:
        """Find number of alert mtta requests by date

        Parameters
        ----------
        start_date : datetime
        end_date : datetime

        Returns
        -------
        dict
        """
        date_range = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((end_date - start_date).days + 1)
        ]
        pipeline = [
            {
                "$match": {
                    "acknowledged_at": {"$ne": None},
                    "created_at": {"$gte": start_date, "$lte": end_date},
                }
            },
            {
                "$group": {
                    "_id": {
                        "date": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$acknowledged_at",
                            }
                        },
                    },
                    "count": {"$sum": 1},
                    "min": {"$min": {"$subtract": ["$acknowledged_at", "$created_at"]}},
                    "max": {"$max": {"$subtract": ["$acknowledged_at", "$created_at"]}},
                    "avg": {"$avg": {"$subtract": ["$acknowledged_at", "$created_at"]}},
                }
            },
            {"$sort": {"_id": 1}},
        ]

        log.debug(f"Pipeline: {pipeline}")

        documents = list(self._collection.aggregate(pipeline))

        data = {}
        for doc in documents:
            date = doc["_id"]["date"]
            data[date] = {
                "count": doc["count"],
                "min": self._transform_milliseconds_to_minutes(doc["min"]),
                "max": self._transform_milliseconds_to_minutes(doc["max"]),
                "avg": self._transform_milliseconds_to_minutes(doc["avg"]),
            }

        final_data = {}

        for date in date_range:
            if date not in data:
                final_data[date] = {"count": 0, "min": 0, "max": 0, "avg": 0}
            else:
                final_data[date] = data[date]

        return final_data

    def find_mttr_number_per_date(
        self,
        *,
        start_date: datetime,
        end_date: datetime,
    ) -> dict:
        """Find number of alert mttr requests by date

        Parameters
        ----------
        start_date : datetime
        end_date : datetime

        Returns
        -------
        dict
        """
        date_range = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((end_date - start_date).days + 1)
        ]
        pipeline = [
            {
                "$match": {
                    "closed_at": {"$ne": None},
                    "created_at": {"$gte": start_date, "$lte": end_date},
                    "status": AlertStatus.CLOSED.value,
                }
            },
            {
                "$group": {
                    "_id": {
                        "date": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$closed_at",
                            }
                        },
                    },
                    "count": {"$sum": 1},
                    "min": {"$min": {"$subtract": ["$closed_at", "$created_at"]}},
                    "max": {"$max": {"$subtract": ["$closed_at", "$created_at"]}},
                    "avg": {"$avg": {"$subtract": ["$closed_at", "$created_at"]}},
                }
            },
            {"$sort": {"_id": 1}},
        ]

        log.debug(f"Pipeline: {pipeline}")

        documents = list(self._collection.aggregate(pipeline))

        data = {}
        for doc in documents:
            date = doc["_id"]["date"]
            data[date] = {
                "count": doc["count"],
                "min": self._transform_milliseconds_to_minutes(doc["min"]),
                "max": self._transform_milliseconds_to_minutes(doc["max"]),
                "avg": self._transform_milliseconds_to_minutes(doc["avg"]),
            }

        final_data = {}

        for date in date_range:
            if date not in data:
                final_data[date] = {"count": 0, "min": 0, "max": 0, "avg": 0}
            else:
                final_data[date] = data[date]

        return final_data

    def _transform_milliseconds_to_minutes(self, milliseconds: int):
        """Transform milliseconds to minutes

        Args:
            milliseconds (int): milliseconds

        Returns:
            float: minutes
        """
        minutes = milliseconds / 60000
        return int(minutes * 100) / 100
