import logging
from datetime import datetime
from typing import Optional

import pymongo
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError

from app.db.base_repository import BaseRepository
from app.db.exceptions import InvalidObjectIDException, ObjectNotFoundException
from app.model.auth_model import BasicAuthUser
from app.utils.encryption_utils import decrypt, encrypt
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")


class BasicAuthUserRepository(BaseRepository):
    def __init__(
        self, *, collection: str, aggregation_collection: Optional[str] = None
    ):
        super().__init__(
            collection=collection, aggregation_collection=aggregation_collection
        )

    @classmethod
    def from_config(cls, *, collection: str) -> "BasicAuthUserRepository":
        """Create BasicAuthUserRepository instance from configuration"""
        return cls(collection=collection)

    @classmethod
    def from_config_with_aggregation(
        cls, *, collection: str, aggregation_collection: str
    ) -> "BasicAuthUserRepository":
        """Create BasicAuthUserRepository instance from configuration"""
        return cls(collection=collection, aggregation_collection=aggregation_collection)

    def __call__(self) -> "BasicAuthUserRepository":
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

    def insert(self, basic_auth_user: BasicAuthUser) -> str:
        if basic_auth_user.created_at is None:
            basic_auth_user.created_at = datetime.now(DEFAULT_TIME_ZONE)

        # encrypt the token data
        basic_auth_user.password = encrypt(basic_auth_user.password).hex()

        basic_auth_user_dict = basic_auth_user.model_dump(by_alias=True, exclude=["id"])
        basic_auth_user_dict.update({"created_at": basic_auth_user.created_at})

        try:
            result = self._collection.insert_one(basic_auth_user_dict)
        except DuplicateKeyError as e:
            raise ValueError(f"BasicAuthUser already exists: {e}")

        return str(result.inserted_id)

    def find(self) -> list[BasicAuthUser]:
        cursor = self._collection.find().sort("created_at", pymongo.DESCENDING)
        basic_auth_users = []
        for document in cursor:
            if document is not None:
                basic_auth_user = BasicAuthUser(**document)
                # decrypt the token data
                basic_auth_user.password = decrypt(
                    bytes.fromhex(basic_auth_user.password)
                )
                basic_auth_users.append(basic_auth_user)

        return basic_auth_users
        # return [BasicAuthUser(**document) for document in cursor if document is not None]

    def update(self, basic_auth_user: BasicAuthUser) -> BasicAuthUser:
        try:
            query = {"_id": ObjectId(basic_auth_user.id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        if basic_auth_user.updated_at is None:
            basic_auth_user.updated_at = datetime.now(DEFAULT_TIME_ZONE)

        # encrypt the token data
        basic_auth_user.password = encrypt(basic_auth_user.password).hex()

        basic_auth_user_dict = basic_auth_user.model_dump(
            by_alias=True, exclude=["id", "created_at"]
        )
        basic_auth_user_dict.update({"updated_at": basic_auth_user.updated_at})
        update = {"$set": basic_auth_user_dict}
        # update = {"$set": basic_auth_user.model_dump(by_alias=True, exclude=['id', 'created_at'])}

        log.debug(f"Update basic_auth_user: {basic_auth_user.id}")
        log.debug(f"Update data: {update}")

        document = self._collection.find_one_and_update(
            query, update=update, return_document=pymongo.ReturnDocument.AFTER
        )

        if document is None:
            raise ObjectNotFoundException(object_id=basic_auth_user.id)

        updated = BasicAuthUser(**document)

        # decrypt the token data
        updated.password = decrypt(bytes.fromhex(updated.password))
        return updated

    def find_by_id(self, basic_auth_user_id: str) -> BasicAuthUser:
        if not basic_auth_user_id:
            raise InvalidObjectIDException("BasicAuthUser id is required")

        try:
            query = {"_id": ObjectId(basic_auth_user_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        document = self._collection.find_one(query)

        if document is None:
            raise ObjectNotFoundException(object_id=basic_auth_user_id)

        basic_auth_user = BasicAuthUser(**document)

        # decrypt the token data
        basic_auth_user.password = decrypt(bytes.fromhex(basic_auth_user.password))
        return basic_auth_user

    def find_by_username(self, basic_auth_username: str) -> BasicAuthUser:
        if not basic_auth_username:
            raise InvalidObjectIDException("BasicAuthUser username is required")

        document = self._collection.find_one({"username": basic_auth_username})

        if document is None:
            raise ObjectNotFoundException(object_id=basic_auth_username)

        basic_auth_user = BasicAuthUser(**document)

        # decrypt the token data
        basic_auth_user.password = decrypt(bytes.fromhex(basic_auth_user.password))
        return basic_auth_user

    def delete_by_id(self, basic_auth_user_id: str) -> bool:
        if not basic_auth_user_id:
            raise InvalidObjectIDException("BasicAuthUser id is required")

        try:
            query = {"_id": ObjectId(basic_auth_user_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        result = self._collection.find_one_and_delete(query)

        if result is None:
            raise ObjectNotFoundException(
                f"BasicAuthUser not found: {basic_auth_user_id}"
            )

        return True
