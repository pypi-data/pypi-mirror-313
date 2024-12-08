from .base import BusinessLogicEventData, BusinessLogicEvent
from .event_types import EventType
from enum import StrEnum

class NewChatData(BusinessLogicEventData):
    is_inbound : bool

class NewChatEvent(BusinessLogicEvent):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    type: EventType = EventType.NEW_CHAT
    data: NewChatData