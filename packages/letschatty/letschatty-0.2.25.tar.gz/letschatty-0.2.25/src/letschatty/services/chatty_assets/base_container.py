from typing import Dict, Generic, TypeVar, Type, List
from abc import ABC
from ...models.base_models.chatty_asset_model import ChattyAssetModel
from ...models.utils.custom_exceptions.custom_exceptions import NotFoundError
from ...models.utils.types import StrObjectId
T = TypeVar('T', bound=ChattyAssetModel)

class ChattyAssetBaseContainer(Generic[T], ABC):
    """
    Base class for containers that store ChattyAssetModel items.
    
    Type Parameters:
        T: The type of items stored in the container. Must be a ChattyAssetModel.
    """
    def __init__(self, item_type: Type[T]):
        """
        Initialize the container with a specific item type.
        
        Args:
            item_type: The class type of items to be stored
        """
        self.items: Dict[str, T] = {}
        self.item_type = item_type

    def insert(self, item: T) -> T:
        """
        Add an item to the container.
        
        Args:
            item: The item to add. Must be of type T.
        
        Raises:
            TypeError: If the item is not of the correct type
        """
        if not isinstance(item, self.item_type):
            raise TypeError(
                f"Expected item of type {self.item_type.__name__}, "
                f"got {type(item).__name__}"
            )
        
        self.items[item.id] = item
        return item
    def update(self, item_id: str, new_item: T) -> T:
        """
        Update an item in the container.
        
        Args:
            item_id: The ID of the item to update
            new_item: The new item data
            
        Raises:
            NotFoundError: If the item_id doesn't exist
            TypeError: If the new_item is not of the correct type
        """
        if item_id not in self.items:
            raise NotFoundError(
                f"Item with id {item_id} not found in {self.__class__.__name__}."
            )
            
        if not isinstance(new_item, self.item_type):
            raise TypeError(
                f"Expected item of type {self.item_type.__name__}, "
                f"got {type(new_item).__name__}"
            )
            
        original_item = self.items[item_id]
        updated_item = original_item.update(new_item)
        self.items[item_id] = updated_item
        return updated_item
    
    def delete(self, item_id: str) -> StrObjectId:
        """
        Delete an item from the container.
        
        Args:
            item_id: The ID of the item to delete
            
        Raises:
            NotFoundError: If the item_id doesn't exist
        """
        if item_id not in self.items:
            raise NotFoundError(
                f"Item with id {item_id} not found in {self.__class__.__name__}."
            )
        del self.items[item_id]
        return item_id

    def get_by_id(self, item_id: str) -> T:
        """
        Get an item from the container.
        
        Args:
            item_id: The ID of the item to retrieve
            
        Returns:
            The requested item
            
        Raises:
            NotFoundError: If the item_id doesn't exist
        """
        if item_id not in self.items:
            raise NotFoundError(
                f"Item with id {item_id} not found in {self.__class__.__name__}."
            )
        return self.items[item_id]
    
    def get_all(self) -> List[T]:
        return list(self.items.values())