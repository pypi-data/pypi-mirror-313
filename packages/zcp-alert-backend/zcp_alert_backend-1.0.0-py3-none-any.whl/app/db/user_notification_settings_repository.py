import logging
from datetime import datetime
from typing import Optional

import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

from app.db.base_repository import BaseRepository
from app.db.exceptions import InvalidObjectIDException, ObjectNotFoundException
from app.model.user_notification_settings import UserNotificationSettings
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")


class UserNotificationSettingsRepository(BaseRepository):
    def __init__(
        self, *, collection: str, aggregation_collection: Optional[str] = None
    ):
        super().__init__(
            collection=collection, aggregation_collection=aggregation_collection
        )

    @classmethod
    def from_config(cls, *, collection: str) -> "UserNotificationSettingsRepository":
        """Create UserNotificationSettingsRepository instance from configuration"""
        return cls(collection=collection)

    @classmethod
    def from_config_with_aggregation(
        cls, *, collection: str, aggregation_collection: str
    ) -> "UserNotificationSettingsRepository":
        """Create UserNotificationSettingsRepository instance from configuration"""
        return cls(collection=collection, aggregation_collection=aggregation_collection)

    def __call__(self) -> "UserNotificationSettingsRepository":
        indexes = self._collection.list_indexes()

        unique_index_name = "unique_key_username"

        unique_index_exists = False
        for index in indexes:
            if index["name"] == unique_index_name and index.get("unique", True):
                unique_index_exists = True
                break

        if not unique_index_exists:
            self._collection.create_index(
                "username", name=unique_index_name, unique=True
            )

        return self

    def insert(self, user_notification_settings: UserNotificationSettings) -> str:
        if user_notification_settings.created_at is None:
            user_notification_settings.created_at = datetime.now(DEFAULT_TIME_ZONE)

        user_notification_settings_dict = user_notification_settings.model_dump(
            by_alias=True, exclude=["id"]
        )
        user_notification_settings_dict.update(
            {"created_at": user_notification_settings.created_at}
        )

        try:
            result = self._collection.insert_one(user_notification_settings_dict)
        except DuplicateKeyError as e:
            raise ValueError(f"UserNotificationSettings already exists: {e}")

        return str(result.inserted_id)

    def find(self) -> list[UserNotificationSettings]:
        cursor = self._collection.find().sort("created_at", pymongo.DESCENDING)
        return [
            UserNotificationSettings(**document)
            for document in cursor
            if document is not None
        ]

    def update(
        self, user_notification_settings: UserNotificationSettings
    ) -> UserNotificationSettings:
        try:
            query = {"_id": ObjectId(user_notification_settings.id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        if user_notification_settings.updated_at is None:
            user_notification_settings.updated_at = datetime.now(DEFAULT_TIME_ZONE)

        user_notification_settings_dict = user_notification_settings.model_dump(
            by_alias=True, exclude=["id", "created_at"]
        )
        user_notification_settings_dict.update(
            {"updated_at": user_notification_settings.updated_at}
        )
        update = {"$set": user_notification_settings_dict}

        log.debug(f"Update user_notification_settings: {user_notification_settings.id}")
        log.debug(f"Update data: {update}")

        document = self._collection.find_one_and_update(
            query, update=update, return_document=pymongo.ReturnDocument.AFTER
        )

        if document is None:
            raise ObjectNotFoundException(object_id=user_notification_settings.id)

        return UserNotificationSettings(**document)

    def find_by_id(
        self, user_notification_settings_id: str
    ) -> UserNotificationSettings:
        if not user_notification_settings_id:
            raise InvalidObjectIDException("UserNotificationSettings id is required")

        try:
            query = {"_id": ObjectId(user_notification_settings_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        document = self._collection.find_one(query)

        if document is None:
            raise ObjectNotFoundException(object_id=user_notification_settings_id)

        return UserNotificationSettings(**document)

    def find_by_username(self, username: str) -> UserNotificationSettings:
        if not username:
            raise InvalidObjectIDException(
                "UserNotificationSettings username is required"
            )

        document = self._collection.find_one({"username": username})

        if document is None:
            raise ObjectNotFoundException(
                f"UserNotificationSettings not found: {username}"
            )

        return UserNotificationSettings(**document)

    def delete_by_id(self, user_notification_settings_id: str) -> bool:
        if not user_notification_settings_id:
            raise InvalidObjectIDException("UserNotificationSettings id is required")

        try:
            query = {"_id": ObjectId(user_notification_settings_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        result = self._collection.find_one_and_delete(query)

        if result is None:
            raise ObjectNotFoundException(
                f"UserNotificationSettings not found: {user_notification_settings_id}"
            )

        return True
