import logging
from abc import abstractmethod
from typing import Optional

from pymongo import MongoClient

import app.settings as settings

# logging.config.fileConfig(settings.LOGGER_CONFIG, disable_existing_loggers=False)
logging.getLogger("pymongo").setLevel(logging.INFO)
# logging.getLogger('pymongo.command').setLevel(logging.DEBUG)

log = logging.getLogger("appLogger")


class BaseRepository:
    """BaseRepository class to handle MongoDB operation

    Naming convention of the child class:
    - find: find all alert requests
    - find_by_id: find one alert request
    - insert: insert one alert request
    - update: update one alert request
    - delete_by_id: delete one alert request
    """

    def __init__(self, *, collection: str, aggregation_collection: Optional[str]):
        self._client = MongoClient(settings.MONGODB_URI, tz_aware=True)
        self._db = self._client.get_database(settings.MONGODB_DATABASE)
        self._collection = self._db.get_collection(collection)
        self._aggregation_collection_name = aggregation_collection

        log.debug(
            f"MONGODB_URI: {settings.MONGODB_URI}, "
            f"DATABASE: {settings.MONGODB_DATABASE}, "
            f"COLLECTION: {collection}, "
            f"AGGREGATION_COLLECTION: {aggregation_collection}"
        )
        log.info(f"{__name__} MongoClient Initialized")

    @abstractmethod
    def from_config(cls, *, collection: str): ...

    @abstractmethod
    def from_config_with_aggregation(
        cls, *, collection: str, aggregation_collection: str
    ): ...

    @property
    def collection(self):
        return self._collection

    @property
    def aggregation_collection_name(self):
        return self._aggregation_collection_name
