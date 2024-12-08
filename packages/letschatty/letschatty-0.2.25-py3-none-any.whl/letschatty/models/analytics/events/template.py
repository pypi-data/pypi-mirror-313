from .base import BusinessLogicEventData, BusinessLogicEvent
from .event_types import EventType
from enum import StrEnum

class TemplateSubtype(StrEnum):
    WAITING = "waiting"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"

class TemplateData(BusinessLogicEventData):
    message_id: str
    template_name: str
    
class TemplateEvent(BusinessLogicEvent):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    type: EventType = EventType.TEMPLATE
    data: TemplateData
    subtype: TemplateSubtype