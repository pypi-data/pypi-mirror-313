from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Generic, TypeVar, Type
from bson.objectid import ObjectId
from pymongo.collection import Collection
from pymongo.database import Database
from ...models.base_models.chatty_asset_model import ChattyAssetModel
from ...models.utils.types import StrObjectId
from ...models.utils.types.serializer_type import SerializerType
from ...models.utils.types.deletion_type import DeletionType
from datetime import datetime
from zoneinfo import ZoneInfo
from ...models.utils.custom_exceptions.custom_exceptions import NotFoundError
import logging

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .mongo_connection import MongoConnection
    
T = TypeVar('T', bound=ChattyAssetModel)

class ChattyAssetCollectionInterface(Generic[T], ABC):
    def __init__(self, database: str, collection: str, connection: MongoConnection, type: Type[T]):
        self.db: Database = connection.client[database]
        self.collection: Collection = self.db[collection]
        self.type = type
    @abstractmethod
    def create_instance(self, data: dict) -> T:
        """Factory method to create instance from data"""
        pass

    def insert(self, asset: T) -> StrObjectId:
        if not isinstance(asset, self.type):
            raise ValueError(f"Asset must be of type {self.type.__name__}")
        document = asset.model_dump(serializer=SerializerType.DATABASE)
        result = self.collection.insert_one(document)
        if not result.inserted_id:
            raise Exception("Failed to insert document")
        logger.debug(f"Inserted document with id {result.inserted_id}")
        return result.inserted_id
        
    def update(self, asset: T) -> StrObjectId:
        logger.debug(f"Updating document with id {asset.id}")
        if not isinstance(asset, self.type):
            raise ValueError(f"Asset must be of type {self.type.__name__}")
        document = asset.model_dump(serializer=SerializerType.DATABASE)
        document.pop('_id', None)  # Still needed
        result = self.collection.update_one({"_id": ObjectId(asset.id)}, {"$set": document})
        if result.modified_count == 0:
            raise NotFoundError(f"No document found with id {asset.id}")
        return asset.id
        
    def get_by_id(self, doc_id: str) -> T | None:
        doc = self.collection.find_one({"_id": ObjectId(doc_id)})
        if doc:
            return self.create_instance(doc)
        else:
            raise NotFoundError(f"No document found with id {doc_id} in db collection {self.collection.name}")

    def get_docs(self, query = {}, limit = 0) -> List[T]:
        docs = self.collection.find(query).limit(limit)
        return [self.create_instance(doc) for doc in docs]    
    
    def delete(self, doc_id: str, deletion_type : DeletionType = DeletionType.LOGICAL) -> StrObjectId:
        logger.debug(f"Deleting document with id {doc_id} - deletion type: {deletion_type}")
        if deletion_type == DeletionType.LOGICAL:
            result = self.collection.update_one({"_id": ObjectId(doc_id)}, {"$set": {"deleted_at": datetime.now(ZoneInfo("UTC"))}})
            if result.modified_count == 0:
                raise NotFoundError(f"No document found with id {doc_id}")
            return doc_id
        elif deletion_type == DeletionType.PHYSICAL:
            result = self.collection.delete_one({"_id": ObjectId(doc_id)})
            if result.deleted_count == 0:
                raise NotFoundError(f"No document found with id {doc_id}")
            return doc_id
        else:
            raise ValueError(f"Invalid deletion type: {deletion_type}")
    
        