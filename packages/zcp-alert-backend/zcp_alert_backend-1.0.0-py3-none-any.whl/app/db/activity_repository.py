import logging
from datetime import datetime
from typing import List, Optional

import pymongo

from app.db.base_repository import BaseRepository
from app.model.alert_model import AlertActivity
from app.utils.list_utils import ACTIVITY_DEFAULT_PAGE_SIZE, DEFAULT_PAGE_NUMBER
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")


class ActivityRepository(BaseRepository):
    def __init__(
        self, *, collection: str, aggregation_collection: Optional[str] = None
    ):
        super().__init__(
            collection=collection, aggregation_collection=aggregation_collection
        )

    @classmethod
    def from_config(cls, *, collection: str) -> "ActivityRepository":
        """Create ActivityRepository instance from configuration"""
        return cls(collection=collection)

    @classmethod
    def from_config_with_aggregation(
        cls, *, collection: str, aggregation_collection: str
    ) -> "ActivityRepository":
        """Create ActivityRepository instance from configuration"""
        return cls(collection=collection, aggregation_collection=aggregation_collection)

    def insert(self, activity: AlertActivity) -> str:
        """Insert one alert activity

        Args:
            activity (AlertActivity): alert activity instance

        Returns:
            str: inserted id

        Raises:
            ValueErrorException: if activity is None
        """
        if activity.created_at is None:
            activity.created_at = datetime.now(DEFAULT_TIME_ZONE)

        activity_dict = activity.model_dump(by_alias=True, exclude=["id"])
        activity_dict["created_at"] = activity.created_at
        return str(self._collection.insert_one(activity_dict).inserted_id)

        # return str(self._collection.insert_one(
        #     activity.model_dump(by_alias=True, exclude=['id'])
        # ).inserted_id)

    def insert_many(self, activities: List[AlertActivity]) -> int:
        """Insert many alert activities

        Args:
            activities (List[AlertActivity]): list of alert activity instances

        Returns:
            int: inserted count

        Raises:
            ValueErrorException: if activities is None
        """
        activities_dict: list[dict] = []
        for activity in activities:
            activity_dict = activity.model_dump(by_alias=True, exclude=["id"])
            activity_dict["created_at"] = activity.created_at
            activities_dict.append(activity_dict)

        return len(self._collection.insert_many(activities_dict).inserted_ids)

        # return len(self._collection.insert_many([
        #     activity.model_dump(by_alias=True, exclude=['id'])
        #     for activity in activities
        # ]).inserted_ids)

    def find_all_by_alert_id(
        self, *, page_number: int, page_size: int, alert_id: str
    ) -> List[AlertActivity]:
        """Find alert activities by alert id

        Args:
            alert_id (str): alert id

        Returns:
            List[AlertActivity]: list of AlertActivity instances
        """
        if page_number < 1:
            page_number = DEFAULT_PAGE_NUMBER
        if page_size < 1:
            page_size = ACTIVITY_DEFAULT_PAGE_SIZE

        skip, limit = (page_size * (page_number - 1), page_size)

        log.debug(f"page_number={page_number}, page_size={page_size}")
        log.debug(f"skip: {skip}, limit: {limit}")

        query = {"alert_id": alert_id}
        cursor = (
            self._collection.find(query)
            .sort("created_at", pymongo.DESCENDING)
            .skip(skip)
            .limit(limit)
        )

        if cursor is None:
            return []

        activities = [
            AlertActivity(**document) for document in cursor if document is not None
        ]

        return activities

    def count_by_alert_id(self, alert_id: str) -> int:
        """Count alert activities by alert id

        Args:
            alert_id (str): alert id

        Returns:
            int: count
        """
        query = {"alert_id": alert_id}

        return self._collection.count_documents(query)

    def delete_all_by_alert_id(self, alert_id: str) -> int:
        """Delete alert activities by alert id

        Args:
            alert_id (str): alert id

        Returns:
            int: deleted count
        """
        query = {"alert_id": alert_id}
        result = self._collection.delete_many(query)

        return result.deleted_count

    def delete_all(self) -> int:
        """Delete all alert activities

        Returns:
            int: deleted count
        """
        result = self._collection.delete_many({})

        return result.deleted_count
