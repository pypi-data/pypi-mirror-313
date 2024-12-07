import logging
from datetime import datetime
from typing import Optional

import pymongo
from bson import ObjectId
from bson.errors import InvalidId

from app.db.base_repository import BaseRepository
from app.db.exceptions import InvalidObjectIDException, ObjectNotFoundException
from app.db.search_utils import get_escaped_regex_pattern
from app.model.channel_model import Channel, ChannelSortField, ChannelType
from app.utils.list_utils import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_SIZE, SortDirection
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")


class ChannelRepository(BaseRepository):
    def __init__(
        self, *, collection: str, aggregation_collection: Optional[str] = None
    ):
        super().__init__(
            collection=collection, aggregation_collection=aggregation_collection
        )

    @classmethod
    def from_config(cls, *, collection: str) -> "ChannelRepository":
        """Create ChannelRepository instance from configuration"""
        return cls(collection=collection)

    @classmethod
    def from_config_with_aggregation(
        cls, *, collection: str, aggregation_collection: str
    ) -> "ChannelRepository":
        """Create ChannelRepository instance from configuration"""
        return cls(collection=collection, aggregation_collection=aggregation_collection)

    def insert(self, channel: Channel) -> str:
        """Insert one alert channel

        Args:
            channel (Channel): alert channel instance

        Returns:
            str: inserted id

        Raises:
            ValueErrorException: if activity is None
        """

        if channel.created_at is None:
            channel.created_at = datetime.now(DEFAULT_TIME_ZONE)

        channel_dict = channel.model_dump(by_alias=True, exclude=["id"])
        channel_dict.update({"created_at": channel.created_at})

        return str(self._collection.insert_one(channel_dict).inserted_id)
        # return str(
        #     self._collection.insert_one(
        #         channel.model_dump(by_alias=True, exclude=['id'])
        #     ).inserted_id
        # )

    def find(
        self,
        *,
        name: Optional[str] = None,
        types: Optional[list[ChannelType]] = None,
        sort_field: Optional[ChannelSortField],
        sort_direction: Optional[SortDirection],
        page_number: int,
        page_size: int,
    ) -> list[Channel]:
        """Find all alert channels

        Args:
            params (dict): query parameters

        Returns:
            List[Channel]: list of Channel instances

        Example:
            params = {
                "status": "OPEN"
            }
        """
        query = self.__find_query(name=name, types=types)

        log.debug(f"Query: {query}")

        if page_number < 1:
            page_number = DEFAULT_PAGE_NUMBER
        if page_size < 1:
            page_size = DEFAULT_PAGE_SIZE

        skip, limit = (page_size * (page_number - 1), page_size)

        log.debug(f"page_number={page_number}, page_size={page_size}")
        log.debug(f"skip: {skip}, limit: {limit}")

        direction = (
            pymongo.ASCENDING
            if sort_direction == SortDirection.ASC
            else pymongo.DESCENDING
        )
        log.debug(
            f"sort_field: {sort_field.value}, direction: {sort_direction} ({direction})"
        )

        cursor = (
            self._collection.find(query)
            .sort(sort_field.value, direction)
            .skip(skip)
            .limit(limit)
        )
        return [Channel(**document) for document in cursor if document is not None]

    def __find_query(
        self,
        *,
        name: Optional[str] = None,
        types: Optional[list[ChannelType]] = None,
    ) -> dict:
        query = {}
        query.update({"type": {"$in": [t.value for t in types]}}) if types else None
        query.update(
            {"name": {"$regex": get_escaped_regex_pattern(name), "$options": "i"}}
        ) if name else None
        return query

    def count(
        self, *, name: Optional[str] = None, types: Optional[list[ChannelType]] = None
    ) -> int:
        """Count all alert channels

        Args:
            params (dict): query parameters

        Returns:
            int: count of Channel instances

        Example:

        """
        query = self.__find_query(name=name, types=types)

        log.debug(f"Query: {query}")

        return self._collection.count_documents(query)

    # def __get_pattern(self, serach_text: Optional[str]):
    #     return f".*{serach_text}.*" if serach_text else ".*"

    def update(self, channel: Channel) -> Channel:
        """Update one alert channel

        Args:
            channel (Channel): alert channel instance

        Returns:
            Channel: Channel instance

        Raises:
            InvalidObjectIDException: if channel id is invalid
            ObjectNotFoundException: if channel not found
        """
        try:
            query = {"_id": ObjectId(channel.id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        if channel.updated_at is None:
            channel.updated_at = datetime.now(DEFAULT_TIME_ZONE)

        channel_dict = channel.model_dump(by_alias=True, exclude=["id", "created_at"])
        channel_dict.update({"updated_at": channel.updated_at})

        update = {"$set": channel_dict}
        # update = {"$set": channel.model_dump(by_alias=True, exclude=['id', 'created_at'])}

        log.debug(f"Update channel: {channel.id}")
        log.debug(f"Update data: {update}")

        document = self._collection.find_one_and_update(
            query, update=update, return_document=pymongo.ReturnDocument.AFTER
        )

        if document is None:
            raise ObjectNotFoundException(object_id=channel.id)

        return Channel(**document)

    def find_by_id(self, channel_id: str) -> Channel:
        """Find one alert channel by channel id

        Args:
            channel_id (str): channel id

        Returns:
            Channel: Channel instance

        Raises:
            InvalidObjectIDException: if channel id is invalid
            ObjectNotFoundException: if channel not found
        """
        try:
            query = {"_id": ObjectId(channel_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        document = self._collection.find_one(query)

        if document is None:
            raise ObjectNotFoundException(object_id=channel_id)

        return Channel(**document)

    def delete_by_id(self, channel_id: str) -> bool:
        """Delete channel by channel id

        Args:
            channel_id (str): channel id

        Returns:
            bool: True if deleted successfully
        """
        try:
            query = {"_id": ObjectId(channel_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)
        result = self._collection.find_one_and_delete(query)

        if result is None:
            raise ObjectNotFoundException(f"Channel not found: {channel_id}")

        return True

    def find_all(self) -> list[dict]:
        """Find all alert channels

        Returns:
            List[dict]: list of Channel instances
        """
        cursor = self._collection.find({}, {"_id": 1, "name": 1})
        channels = []
        for document in cursor:
            if document is not None:
                channels.append({"id": str(document["_id"]), "name": document["name"]})

        return channels
