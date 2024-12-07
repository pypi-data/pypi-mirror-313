import logging
from datetime import datetime
from typing import List, Optional

import pymongo
from bson import ObjectId
from bson.errors import InvalidId

from app.db.base_repository import BaseRepository
from app.db.exceptions import InvalidObjectIDException, ObjectNotFoundException
from app.db.search_utils import get_escaped_regex_pattern
from app.model.silence_model import Silence, SilenceSortField, SilenceStatus
from app.utils.list_utils import DEFAULT_PAGE_NUMBER, DEFAULT_PAGE_SIZE, SortDirection
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")


class SilenceRepository(BaseRepository):
    def __init__(
        self, *, collection: str, aggregation_collection: Optional[str] = None
    ):
        super().__init__(
            collection=collection, aggregation_collection=aggregation_collection
        )

    @classmethod
    def from_config(cls, *, collection: str) -> "SilenceRepository":
        """Create SilenceRepository instance from configuration"""
        return cls(collection=collection)

    @classmethod
    def from_config_with_aggregation(
        cls, *, collection: str, aggregation_collection: str
    ) -> "SilenceRepository":
        """Create SilenceRepository instance from configuration"""
        return cls(collection=collection, aggregation_collection=aggregation_collection)

    def insert(self, silence: Silence) -> str:
        """Insert one alert silence

        Args:
            silence (Silence): alert silence instance

        Returns:
            str: inserted id
        """
        # check if integration id is valid
        for __integration_id in silence.integrations:
            try:
                ObjectId(__integration_id)
            except InvalidId as e:
                raise InvalidObjectIDException(e)

        if silence.created_at is None:
            silence.created_at = datetime.now(DEFAULT_TIME_ZONE)

        silence_dict = silence.model_dump(by_alias=True, exclude=["id"])
        silence_dict.update(
            {
                "created_at": silence.created_at,
                "starts_at": silence.starts_at,
                "ends_at": silence.ends_at,
            }
        )
        return str(self._collection.insert_one(silence_dict).inserted_id)

        # return str(
        #     self._collection.insert_one(
        #         silence.model_dump(by_alias=True, exclude=['id'])
        #     ).inserted_id
        # )

    def find(
        self,
        *,
        name: Optional[str] = None,
        statuses: Optional[list[SilenceStatus]] = None,
        integration_id: Optional[str] = None,
        sort_field: Optional[SilenceSortField],
        sort_direction: Optional[SortDirection],
        page_number: int,
        page_size: int,
    ) -> list[Silence]:
        """Find all alert channels

        Args:
            params (dict): query parameters

        Returns:
            List[Silence]: list of Silence instances

        Example:
            params = {
                "status": "OPEN"
            }
        """
        if page_number < 1:
            page_number = DEFAULT_PAGE_NUMBER
        if page_size < 1:
            page_size = DEFAULT_PAGE_SIZE

        skip, limit = (page_size * (page_number - 1), page_size)

        log.debug(f"page_number={page_number}, page_size={page_size}")
        log.debug(f"skip: {skip}, limit: {limit}")

        pipeline = self.__get_aggregate_pipeline(
            name=name,
            statuses=statuses,
            sort_field=sort_field,
            sort_direction=sort_direction,
            integration_id=integration_id,
            skip=skip,
            limit=limit,
        )
        log.debug(f"Pipeline: {pipeline}")

        cursor = self._collection.aggregate(pipeline=pipeline)

        return [Silence(**document) for document in cursor if document is not None]

    def __find_query(
        self,
        *,
        name: Optional[str] = None,
        statuses: Optional[list[SilenceStatus]] = None,
        integration_id: Optional[str] = None,
    ) -> dict:
        query = {}
        query.update(
            {"name": {"$regex": get_escaped_regex_pattern(name), "$options": "i"}}
        ) if name else None
        query.update(
            {"integrations": {"$in": [integration_id]}}
        ) if integration_id else None

        if statuses is not None:
            current_time = datetime.now(DEFAULT_TIME_ZONE)
            or_query = []
            for status in statuses:
                if status == SilenceStatus.ACTIVE:
                    or_query.append(
                        {
                            "starts_at": {"$lte": current_time},
                            "ends_at": {"$gte": current_time},
                        }
                    )
                elif status == SilenceStatus.EXPIRED:
                    or_query.append({"ends_at": {"$lt": current_time}})
                elif status == SilenceStatus.PLANNED:
                    or_query.append({"starts_at": {"$gt": current_time}})

            query.update({"$or": or_query})

        # if status == SilenceStatus.ACTIVE:
        #     query.update({"starts_at": {"$lte": current_time}, "ends_at": {"$gte": current_time}})
        # elif status == SilenceStatus.EXPIRED:
        #     query.update({"ends_at": {"$lt": current_time}})
        # elif status == SilenceStatus.PLANNED:
        #     query.update({"starts_at": {"$gt": current_time}})

        return query

    def __get_aggregate_pipeline(
        self,
        *,
        name: Optional[str] = None,
        statuses: Optional[list[SilenceStatus]] = None,
        integration_id: Optional[str] = None,
        sort_field: Optional[SilenceSortField] = None,
        sort_direction: Optional[SortDirection] = None,
        skip: Optional[int] = None,
        limit: Optional[int] = None,
        is_count: Optional[bool] = False,
    ) -> List[dict]:
        """Get aggregation pipeline for silence

        It is used to get the silence data with integrations data for only the silence list
        """

        query = self.__find_query(
            name=name, statuses=statuses, integration_id=integration_id
        )

        # query.update({'_id': ObjectId(silence_id)}) if silence_id else None

        pipeline = []
        pipeline.append({"$unwind": "$integrations"})
        pipeline.append({"$addFields": {"tid": {"$toObjectId": "$integrations"}}})
        pipeline.append({"$match": query}) if query else None
        pipeline.append(
            {
                "$lookup": {
                    "from": self._aggregation_collection_name,
                    "localField": "tid",
                    "foreignField": "_id",
                    "as": "integrations",
                }
            }
        )
        pipeline.append({"$unwind": "$integrations"})
        # remove the tid field
        pipeline.append({"$project": {"tid": 0}})
        pipeline.append(
            {
                "$group": {
                    "_id": "$_id",
                    "created_at": {"$first": "$created_at"},
                    "updated_at": {"$first": "$updated_at"},
                    "name": {"$first": "$name"},
                    "starts_at": {"$first": "$starts_at"},
                    "ends_at": {"$first": "$ends_at"},
                    "modifier": {"$first": "$modifier"},
                    "integrations": {
                        "$push": {
                            "id": "$integrations._id",
                            "name": "$integrations.name",
                            "status": "$integrations.status",
                        }
                    },
                },
            }
        )

        # for the sort
        if sort_field is not None and sort_direction is not None:
            direction = (
                pymongo.DESCENDING
                if sort_direction == SortDirection.DESC
                else pymongo.ASCENDING
            )
            if sort_field == SilenceSortField.STATUS:
                current_time = datetime.now(DEFAULT_TIME_ZONE)
                pipeline.append(
                    {
                        "$addFields": {
                            "status": {
                                "$switch": {
                                    "branches": [
                                        {
                                            "case": {
                                                "$and": [
                                                    {
                                                        "$gt": [
                                                            "$starts_at",
                                                            current_time,
                                                        ]
                                                    },
                                                    {"$gt": ["$ends_at", current_time]},
                                                ]
                                            },
                                            "then": "Planed",
                                        },
                                        {
                                            "case": {
                                                "$and": [
                                                    {
                                                        "$gt": [
                                                            "$starts_at",
                                                            current_time,
                                                        ]
                                                    },
                                                    {"$lt": ["$ends_at", current_time]},
                                                ]
                                            },
                                            "then": "Active",
                                        },
                                        {
                                            "case": {
                                                "$and": [
                                                    {
                                                        "$lt": [
                                                            "$starts_at",
                                                            current_time,
                                                        ]
                                                    },
                                                    {"$lt": ["$ends_at", current_time]},
                                                ]
                                            },
                                            "then": "Expired",
                                        },
                                    ],
                                    "default": "Unknown",
                                }
                            }
                        }
                    },
                )
                pipeline.append({"$sort": {"status": direction}})
            else:
                pipeline.append({"$sort": {sort_field.value: direction}})

        if skip is not None:
            pipeline.append({"$skip": skip})
        if limit is not None:
            pipeline.append({"$limit": limit})

        if is_count:
            pipeline.append({"$count": "total"})

        return pipeline

    def count(
        self,
        *,
        name: Optional[str] = None,
        statuses: Optional[list[SilenceStatus]] = None,
        integration_id: Optional[str] = None,
    ) -> int:
        """Count all alert channels

        Args:
            params (dict): query parameters

        Returns:
            int: count of Silence instances

        Example:

        """
        query = self.__find_query(
            name=name, statuses=statuses, integration_id=integration_id
        )

        log.debug(f"Query: {query}")

        count = self._collection.count_documents(query)

        return count

    def update(self, silence: Silence) -> Silence:
        """Update one alert silence

        Args:
            silence (Silence): alert silence instance

        Returns:
            Silence: Silence instance

        Raises:
            InvalidObjectIDException: if silence id is invalid
            ObjectNotFoundException: if silence not found
        """

        # check if integration id is valid
        for __integration_id in silence.integrations:
            try:
                ObjectId(__integration_id)
            except InvalidId as e:
                raise InvalidObjectIDException(e)

        try:
            query = {"_id": ObjectId(silence.id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        if silence.updated_at is None:
            silence.updated_at = datetime.now(DEFAULT_TIME_ZONE)

        silence_dict = silence.model_dump(by_alias=True, exclude=["id", "created_at"])
        silence_dict.update(
            {
                "updated_at": silence.updated_at,
                "starts_at": silence.starts_at,
                "ends_at": silence.ends_at,
            }
        )
        update = {"$set": silence_dict}
        # update = {"$set": silence.model_dump(by_alias=True, exclude=['id', 'created_at'])}

        log.debug(f"Update silence: {silence.id}")
        log.debug(f"Update data: {update}")

        document = self._collection.find_one_and_update(
            query, update=update, return_document=pymongo.ReturnDocument.AFTER
        )

        if document is None:
            raise ObjectNotFoundException(object_id=silence.id)

        return Silence(**document)

    def find_by_integration_id(self, integration_id: str) -> list[Silence]:
        """Find all alert silences by integration id

        Args:
            integration_id (str): integration id

        Returns:
            List[Silence]: list of Silence instances
        """
        query = {"integrations": {"$in": [integration_id]}}
        cursor = self._collection.find(query)

        return [Silence(**document) for document in cursor if document is not None]

    def find_by_id(self, silence_id: str) -> Silence:
        """Find one alert silence by silence id

        This object does not include the integrations data
        so if you need the integrations data you need to call the find_all_by_ids of the integration repository

        Args:
            silence_id (str): silence id

        Returns:
            Silence: Silence instance

        Raises:
            InvalidObjectIDException: if silence id is invalid
            ObjectNotFoundException: if silence not found
        """
        try:
            query = {"_id": ObjectId(silence_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        document = self._collection.find_one(query)

        if document is None:
            raise ObjectNotFoundException(object_id=silence_id)

        return Silence(**document)

    def delete_by_id(self, silence_id: str) -> bool:
        """Delete silence by silence id

        Args:
            silence_id (str): silence id

        Returns:
            bool: True if deleted successfully
        """
        try:
            query = {"_id": ObjectId(silence_id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)
        result = self._collection.find_one_and_delete(query)

        if result is None:
            raise ObjectNotFoundException(f"Silence not found: {silence_id}")

        return True

    def find_all_active_by_integration_id(self, integration_id: str) -> list[Silence]:
        """Find all active silences by integration id

        Args:
            integration_id (str): integration id

        Returns:
            List[Silence]: list of Silence instances
        """
        pipeline = self.__get_aggregate_pipeline(
            statuses=[SilenceStatus.ACTIVE], integration_id=integration_id
        )

        log.debug(f"Pipeline: {pipeline}")

        cursor = self._collection.aggregate(pipeline=pipeline)

        return [Silence(**document) for document in cursor if document is not None]
