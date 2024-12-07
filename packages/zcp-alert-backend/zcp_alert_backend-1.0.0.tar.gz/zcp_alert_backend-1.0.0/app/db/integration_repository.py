import logging
from datetime import datetime
from typing import List, Optional

import pymongo
from bson import ObjectId
from bson.errors import InvalidId

from app.db.base_repository import BaseRepository
from app.db.exceptions import InvalidObjectIDException, ObjectNotFoundException
from app.db.search_utils import get_escaped_regex_pattern
from app.model.channel_model import ChannelType
from app.model.integration_model import (
    Integration,
    IntegrationSortField,
    IntegrationStatus,
)
from app.utils.list_utils import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_SIZE, SortDirection
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")


class IntegrationRepository(BaseRepository):
    def __init__(
        self, *, collection: str, aggregation_collection: Optional[str] = None
    ):
        super().__init__(
            collection=collection, aggregation_collection=aggregation_collection
        )

    @classmethod
    def from_config(cls, *, collection: str) -> "IntegrationRepository":
        """Create IntegrationRepository instance from configuration"""
        return cls(collection=collection)

    @classmethod
    def from_config_with_aggregation(
        cls, *, collection: str, aggregation_collection: str
    ) -> "IntegrationRepository":
        """Create IntegrationRepository instance from configuration"""
        return cls(collection=collection, aggregation_collection=aggregation_collection)

    def insert(self, integration: Integration) -> str:
        """Insert one alert integration

        Args:
            integration (Integration): alert integration instance

        Returns:
            str: inserted id
        """
        # check if channel is a valid ObjectId
        __channel_id = integration.channel
        try:
            ObjectId(__channel_id)
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        if integration.created_at is None:
            integration.created_at = datetime.now(DEFAULT_TIME_ZONE)

        integration_dict = integration.model_dump(by_alias=True, exclude=["id"])
        integration_dict.update({"created_at": integration.created_at})

        return str(self._collection.insert_one(integration_dict).inserted_id)
        # return str(self._collection.insert_one(
        #     integration.model_dump(by_alias=True, exclude=['id'])
        # ).inserted_id)

    def find_all_by_status(self, status: IntegrationStatus) -> list[Integration]:
        """Find all alert integrations"""
        pipeline = self.__get_aggregate_pipeline(status=status)

        log.debug(f"Pipeline: {pipeline}")

        cursor = self._collection.aggregate(pipeline=pipeline)
        integrations = []
        for document in cursor:
            if document is not None:
                channels = document.get("channel", [{}])
                if len(channels) > 0:
                    document["channel"] = channels[0]
                else:
                    document["channel"] = None
                integrations.append(Integration(**document))

        return integrations

    def find_all(self) -> list[dict]:
        """Find all alert integrations"""
        cursor = self._collection.find({}, {"_id": 1, "name": 1})
        integrations = []
        for document in cursor:
            if document is not None:
                integrations.append(
                    {"id": str(document["_id"]), "name": document["name"]}
                )

        return integrations

    def find(
        self,
        *,
        name: Optional[str] = None,
        channel_name: Optional[str] = None,
        channel_type: Optional[ChannelType] = None,
        status: Optional[IntegrationStatus] = None,
        sort_field: Optional[IntegrationSortField],
        sort_direction: Optional[SortDirection],
        page_number: int,
        page_size: int,
    ) -> list[Integration]:
        """Find all alert integrations"""

        if page_number < 1:
            page_number = DEFAULT_PAGE_NUMBER
        if page_size < 1:
            page_size = DEFAULT_PAGE_SIZE

        skip, limit = (page_size * (page_number - 1), page_size)

        log.debug(f"page_number={page_number}, page_size={page_size}")
        log.debug(f"skip: {skip}, limit: {limit}")

        pipeline = self.__get_aggregate_pipeline(
            name=name,
            channel_name=channel_name,
            channel_type=channel_type,
            status=status,
            sort_field=sort_field,
            sort_direction=sort_direction,
            skip=skip,
            limit=limit,
        )

        log.debug(f"Pipeline: {pipeline}")

        cursor = self._collection.aggregate(pipeline=pipeline)
        integrations = []
        for document in cursor:
            if document is not None:
                channels = document.get("channel", [{}])
                if len(channels) > 0:
                    document["channel"] = channels[0]
                else:
                    document["channel"] = None
                integrations.append(Integration(**document))

        return integrations

    def count(
        self,
        *,
        name: Optional[str] = None,
        channel_name: Optional[str] = None,
        channel_type: Optional[ChannelType] = None,
        status: Optional[IntegrationStatus] = None,
    ) -> int:
        """Count all alert"""
        pipeline = self.__get_aggregate_pipeline(
            name=name,
            channel_name=channel_name,
            channel_type=channel_type,
            status=status,
            is_count=True,
        )

        log.debug(f"Pipeline: {pipeline}")

        cursor = self._collection.aggregate(pipeline=pipeline)

        count: int = 0
        for document in cursor:
            if document is not None:
                count = document.get("total", 0)

        return count

    def update(self, integration: Integration) -> Integration:
        """Update one alert integration"""
        # check if channel is a valid ObjectId
        channel_id = integration.channel
        try:
            ObjectId(channel_id)
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        try:
            query = {"_id": ObjectId(integration.id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        if integration.updated_at is None:
            integration.updated_at = datetime.now(DEFAULT_TIME_ZONE)

        integration_dict = integration.model_dump(
            by_alias=True, exclude=["id", "created_at"]
        )
        integration_dict.update({"updated_at": integration.updated_at})

        update = {"$set": integration_dict}
        # update = {"$set": integration.model_dump(by_alias=True, exclude=['id', 'created_at'])}

        log.debug(f"Update integration: {integration.id}")
        log.debug(f"Update data: {update}")

        document = self._collection.find_one_and_update(
            query, update=update, return_document=pymongo.ReturnDocument.AFTER
        )

        if document is None:
            raise ObjectNotFoundException(object_id=integration.id)

        return Integration(**document)

    def find_by_id(self, integration_id: str) -> Integration:
        """Find one alert integration by channel id"""
        try:
            query = {"_id": ObjectId(integration_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        document = self._collection.find_one(query)

        if document is None:
            raise ObjectNotFoundException(object_id=integration_id)

        return Integration(**document)

    def find_by_id_using_aggregator(self, integration_id: str) -> Integration:
        # check if channel is a valid ObjectId
        try:
            ObjectId(integration_id)
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        pipeline = self.__get_aggregate_pipeline(integration_id=integration_id)

        log.debug(f"Pipeline: {pipeline}")

        document = self._collection.aggregate(pipeline=pipeline).next()

        if document is None:
            raise ObjectNotFoundException(object_id=integration_id)

        # aggregate result is a list of dict so we need to convert it to dict
        channels = document.get("channel", [{}])
        if len(channels) > 0:
            document["channel"] = channels[0]
        else:
            document["channel"] = None

        return Integration(**document)

    def __get_aggregate_pipeline(
        self,
        *,
        integration_id: Optional[str] = None,
        name: Optional[str] = None,
        channel_name: Optional[str] = None,
        channel_type: Optional[ChannelType] = None,
        status: Optional[IntegrationStatus] = None,
        sort_field: Optional[IntegrationSortField] = None,
        sort_direction: Optional[SortDirection] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        is_count: Optional[bool] = False,
    ) -> list[dict]:
        query = {}
        query.update({"_id": ObjectId(integration_id)}) if integration_id else None
        query.update(
            {"name": {"$regex": get_escaped_regex_pattern(name), "$options": "i"}}
        ) if name else None
        query.update(
            {
                "channel.name": {
                    "$regex": get_escaped_regex_pattern(channel_name),
                    "$options": "i",
                }
            }
        ) if channel_name else None
        query.update({"channel.type": channel_type.value}) if channel_type else None
        query.update({"status": status.value}) if status else None

        pipeline = []
        # localField and foreignField should be the same type
        pipeline.append({"$addFields": {"channel_id": {"$toObjectId": "$channel"}}})
        # for the performance of find_by_id(), $match shoud be executed first most of the $lookup
        if integration_id is not None:
            pipeline.append({"$match": query})
        pipeline.append(
            {
                "$lookup": {
                    "from": self._aggregation_collection_name,
                    "localField": "channel_id",
                    "foreignField": "_id",
                    "as": "channel",
                }
            }
        )
        # for the performance, if find_all we should use $match after $lookup
        if integration_id is None:
            pipeline.append({"$match": query})
        # we need to remove channel_id
        pipeline.append({"$project": {"channel_id": 0}})

        # for the sort
        if sort_field is not None and sort_direction is not None:
            direction = (
                pymongo.DESCENDING
                if sort_direction == SortDirection.DESC
                else pymongo.ASCENDING
            )
            pipeline.append(
                {"$sort": {self.__get_sort_field(sort_field=sort_field): direction}}
            )

        if skip is not None:
            pipeline.append({"$skip": skip})
        if limit is not None:
            pipeline.append({"$limit": limit})

        if is_count:
            pipeline.append({"$count": "total"})

        return pipeline

    def __get_sort_field(self, sort_field: IntegrationSortField) -> str:
        switcher = {
            IntegrationSortField.NAME: "name",
            IntegrationSortField.CHANNEL_NAME: "channel.name",
            IntegrationSortField.CHANNEL_TYPE: "channel.type",
            IntegrationSortField.STATUS: "status",
            IntegrationSortField.CREATED_AT: "created_at",
            IntegrationSortField.UPDATED_AT: "updated_at",
        }
        return switcher.get(sort_field, "name")

    def delete_by_id(self, integration_id: str) -> bool:
        """Delete alert integration by integration_id"""
        try:
            query = {"_id": ObjectId(integration_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)
        result = self._collection.find_one_and_delete(query)

        if result is None:
            raise ObjectNotFoundException(f"Integration not found: {integration_id}")

        return True

    def find_all_by_ids(self, ids: list[str]) -> List[Integration]:
        """Find all alert integrations by silence id"""
        query = {"_id": {"$in": [ObjectId(id) for id in ids if id is not None]}}

        log.debug(f"In Query: {query}")
        cursor = self._collection.find(query)
        return [Integration(**document) for document in cursor if document is not None]

    def find_all_by_channel_id(self, channel_id: str) -> List[Integration]:
        """Find all alert integrations by channel id"""
        query = {"channel": channel_id}

        log.debug(f"In Query: {query}")
        cursor = self._collection.find(query)
        return [Integration(**document) for document in cursor if document is not None]

    def update_status(
        self, *, integration_id: str, status: IntegrationStatus, modifier: str
    ) -> Integration:
        """Update status of alert integration"""

        if not integration_id:
            raise InvalidObjectIDException("Integration ID is None")

        try:
            query = {"_id": ObjectId(integration_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        update = {
            "$set": {
                "status": status.value,
                "modifier": modifier,
                "updated_at": datetime.now(DEFAULT_TIME_ZONE),
            }
        }

        log.debug(f"Update integration status: {integration_id}")
        log.debug(f"Update data: {update}")

        document = self._collection.find_one_and_update(
            query, update=update, return_document=pymongo.ReturnDocument.AFTER
        )

        if document is None:
            raise ObjectNotFoundException(object_id=integration_id)

        return Integration(**document)
