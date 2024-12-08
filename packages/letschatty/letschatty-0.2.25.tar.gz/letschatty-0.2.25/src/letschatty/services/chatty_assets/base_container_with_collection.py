from typing import TypeVar, Type, List
from abc import ABC
from ...models.base_models.chatty_asset_model import ChattyAssetModel
from .base_container import ChattyAssetBaseContainer
from ...models.data_base.collection_interface import ChattyAssetCollectionInterface
from ...models.utils.custom_exceptions.custom_exceptions import NotFoundError
from ...models.utils.types.deletion_type import DeletionType
from ...models.utils.types import StrObjectId
T = TypeVar('T', bound=ChattyAssetModel)

class ChattyAssetContainerWithCollection(ChattyAssetBaseContainer[T], ABC):
    """
    Base class for containers that store ChattyAssetModel items.
    
    Type Parameters:
        T: The type of items stored in the container. Must be a ChattyAssetModel.
    """
    def __init__(self, item_type: Type[T], collection: ChattyAssetCollectionInterface[T]):
        """
        Initialize the container with a specific item type.
        
        Args:
            item_type: The class type of items to be stored
            collection: The collection interface to use for database operations
        """
        if not isinstance(collection, ChattyAssetCollectionInterface):
            raise TypeError(
                f"Expected collection of type ChattyAssetCollectionInterface, "
                f"got {type(collection).__name__}"
            )
        super().__init__(item_type)
        self.collection = collection
        self.load_from_db()
    def insert(self, item: T) -> T:
        """
        Add an item to the container and insert it into the database collection.
        
        Args:
            item: The item to add. Must be of type T.
        
        Raises:
            TypeError: If the item is not of the correct type
            Exception: If insertion into database collection fails
        """
        inserted_item = super().insert(item)
        self.collection.insert(inserted_item)
        return inserted_item
        
    def update(self, id: str, new_item: T) -> T:
        """
        Update an item in the container and in the database collection.
        
        Args:
            item_id: The ID of the item to update
            new_item: The new item data
            
        Raises:
            NotFoundError: If the item_id doesn't exist in both container and collection
            TypeError: If the new_item is not of the correct type
            
        Note:
            If the item exists in the collection but not in the container,
            it will be updated in both places. If it exists in neither,
            a NotFoundError will be raised.
        """
        try:
            updated_item = super().update(id, new_item)
            self.collection.update(updated_item)
            return updated_item
            
        except NotFoundError as e:
            outdated_item = self.collection.get_by_id(id)
            if outdated_item:
                updated_item = outdated_item.update(new_item)
                self.items[id] = updated_item
                self.collection.update(updated_item)
                return updated_item
            else:
                raise NotFoundError(
                f"Item with id {id} not found in {self.__class__.__name__} nor in collection DB"
            )        

    def delete(self, id: str, deletion_type : DeletionType = DeletionType.LOGICAL) -> StrObjectId:
        """
        Delete an item from the container and the collection.
        
        Args:
            item_id: The ID of the item to delete
            deletion_type: The type of deletion to perform (logical or physical)
            
        Raises:
            NotFoundError: If the item_id doesn't exist in both container and collection
            ValueError: If an invalid deletion type is provided
        """
        try:
            super().delete(id)
            return self.collection.delete(id, deletion_type)
        except NotFoundError as e:
            return self.collection.delete(id, deletion_type)
        
    def get_by_id(self, id: str) -> T:
        """
        Get an item from the container.
        
        Args:
            item_id: The ID of the item to retrieve
            
        Returns:
            The requested item
            
        Raises:
            NotFoundError: If the item_id doesn't exist
        """
        try:
            return super().get_by_id(id)
        except NotFoundError as e:
            return self.collection.get_by_id(id)
        
    def get_all(self) -> List[T]:
        return super().get_all() + self.collection.get_docs({"deleted_at": None})
    
    def get_deleted(self) -> List[T]:
        return self.collection.get_docs({"deleted_at": {"$ne": None}})
    
    def load_from_db(self):
        self.items = {item.id: item for item in self.collection.get_docs({"deleted_at": None})}
    
    def restore(self, id: str) -> T:
        if id in self.items:
            raise ValueError(f"Item with id {id} already exists in {self.__class__.__name__}")
        restored_item = self.collection.get_by_id(id)
        if restored_item is None:
            raise NotFoundError(f"Item with id {id} not found in collection DB")
        restored_item.deleted_at = None
        restored_item.update_now()
        self.items[id] = restored_item
        self.collection.update(restored_item)
        return restored_item
