import logging
from datetime import datetime
from typing import Optional

import pymongo
from bson import ObjectId
from bson.errors import InvalidId

from app.db.base_repository import BaseRepository
from app.db.exceptions import InvalidObjectIDException, ObjectNotFoundException
from app.model.kakaotalk_model import KakaoTalkToken
from app.utils.encryption_utils import decrypt, encrypt
from app.utils.time_utils import DEFAULT_TIME_ZONE

log = logging.getLogger("appLogger")


class KakaoTaklTokenRepository(BaseRepository):
    def __init__(
        self, *, collection: str, aggregation_collection: Optional[str] = None
    ):
        super().__init__(
            collection=collection, aggregation_collection=aggregation_collection
        )

    @classmethod
    def from_config(cls, *, collection: str) -> "KakaoTaklTokenRepository":
        """Create KakaoTaklTokenRepository instance from configuration"""
        return cls(collection=collection)

    @classmethod
    def from_config_with_aggregation(
        cls, *, collection: str, aggregation_collection: str
    ) -> "KakaoTaklTokenRepository":
        """Create SilenceRepository instance from configuration"""
        return cls(collection=collection, aggregation_collection=aggregation_collection)

    def insert(self, kakaotalk_token: KakaoTalkToken) -> str:
        """Insert one kakao token

        Parameters
        ----------
        kakaotalk_token : KakaoToken

        Returns
        -------
        str
            returns the inserted id

        Raises
        ------
        InvalidObjectIDException
        """

        if kakaotalk_token.created_at is None:
            kakaotalk_token.created_at = datetime.now(DEFAULT_TIME_ZONE)

        # encrypt the token data
        kakaotalk_token.access_token = encrypt(kakaotalk_token.access_token).hex()
        kakaotalk_token.refresh_token = encrypt(kakaotalk_token.refresh_token).hex()
        kakaotalk_token.id_token = encrypt(kakaotalk_token.id_token).hex()

        kakaotalk_token_dict = kakaotalk_token.model_dump(by_alias=True, exclude=["id"])
        kakaotalk_token_dict.update({"created_at": kakaotalk_token.created_at})

        return str(self._collection.insert_one(kakaotalk_token_dict).inserted_id)
        # return str(
        #     self._collection.insert_one(
        #         kakaotalk_token.model_dump(by_alias=True, exclude=['id'])
        #     ).inserted_id
        # )

    def update(self, kakaotalk_token: KakaoTalkToken) -> KakaoTalkToken:
        """Update one kakao token

        Parameters
        ----------
        kakaotalk_token : KakaoToken

        Returns
        -------
        KakaoToken
            returns the updated KakaoToken instance

        Raises
        ------
        InvalidObjectIDException
        ObjectNotFoundException
        """
        try:
            filters = {"_id": ObjectId(kakaotalk_token.id)}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        if kakaotalk_token.updated_at is None:
            kakaotalk_token.updated_at = datetime.now(DEFAULT_TIME_ZONE)

        # encrypt the token data
        kakaotalk_token.access_token = encrypt(kakaotalk_token.access_token).hex()
        kakaotalk_token.refresh_token = encrypt(kakaotalk_token.refresh_token).hex()
        kakaotalk_token.id_token = encrypt(kakaotalk_token.id_token).hex()

        kakaotalk_token_dict = kakaotalk_token.model_dump(
            by_alias=True, exclude=["id", "created_at"]
        )
        kakaotalk_token_dict.update({"updated_at": kakaotalk_token.updated_at})

        update = {"$set": kakaotalk_token_dict}
        # update = {
        #     "$set": kakaotalk_token.model_dump(
        #         by_alias=True,
        #         exclude=['id', 'created_at']
        #     )
        # }

        log.debug(f"Update kakaotalk token: {kakaotalk_token.id}")
        log.debug(f"Update data: {update}")

        document = self._collection.find_one_and_update(
            filters, update=update, return_document=pymongo.ReturnDocument.AFTER
        )

        if document is None:
            raise ObjectNotFoundException(object_id=kakaotalk_token.id)

        kakaotalk_token = KakaoTalkToken(**document)

        # decrypt the token data
        kakaotalk_token.access_token = decrypt(
            bytes.fromhex(kakaotalk_token.access_token)
        )
        kakaotalk_token.refresh_token = decrypt(
            bytes.fromhex(kakaotalk_token.refresh_token)
        )
        kakaotalk_token.id_token = decrypt(bytes.fromhex(kakaotalk_token.id_token))

        return kakaotalk_token

    def find_by_channel_id(self, channel_id: str) -> KakaoTalkToken:
        """Find one kakao token by id

        Parameters
        ----------
        channel_id : str

        Returns
        -------
        KakaoToken
            returns the KakaoToken instance

        Raises
        ------
        InvalidObjectIDException
        ObjectNotFoundException
        """
        try:
            query = {"channel_id": channel_id}
        except InvalidId as e:
            raise InvalidObjectIDException(e)

        document = self._collection.find_one(query)

        if document is None:
            raise ObjectNotFoundException(object_id=channel_id)

        kakaotalk_token = KakaoTalkToken(**document)

        # decrypt the token data
        kakaotalk_token.access_token = decrypt(
            bytes.fromhex(kakaotalk_token.access_token)
        )
        kakaotalk_token.refresh_token = decrypt(
            bytes.fromhex(kakaotalk_token.refresh_token)
        )
        kakaotalk_token.id_token = decrypt(bytes.fromhex(kakaotalk_token.id_token))

        return kakaotalk_token

    def delete_by_channel_id(self, channel_id: str) -> bool:
        """Delete one kakao token

        Parameters
        ----------
        channel_id : str

        Returns
        -------
        bool
            returns True if the delete is successful

        Raises
        ------
        InvalidObjectIDException
        ObjectNotFoundException
        """
        try:
            query = {"channel_id": channel_id}
        except InvalidId as e:
            raise InvalidObjectIDException(e)
        result = self._collection.find_one_and_delete(query)

        if result is None:
            raise ObjectNotFoundException(
                f"Kakao token not found using channel id: {channel_id}"
            )

        return True
