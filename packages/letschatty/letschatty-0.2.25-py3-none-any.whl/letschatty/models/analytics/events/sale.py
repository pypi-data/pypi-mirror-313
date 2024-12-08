from .base import BusinessLogicEventData, BusinessLogicEvent
from .event_types import EventType
from enum import StrEnum

class SaleSubtype(StrEnum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"

class SaleData(BusinessLogicEventData):
    sale_id: str
    
class SaleEvent(BusinessLogicEvent):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    type: EventType = EventType.SALE
    data: SaleData
    subtype: SaleSubtype