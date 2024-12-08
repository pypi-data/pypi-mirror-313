from .base import BusinessLogicEventData, BusinessLogicEvent
from .event_types import EventType
from ...utils.types.identifier import StrObjectId
from enum import StrEnum

class CPSubtype(StrEnum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"

class ContactPointData(BusinessLogicEventData):
    source_id: StrObjectId
    new_chat : bool

class ContactPointEvent(BusinessLogicEvent):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    type: EventType = EventType.CONTACT_POINT
    data: ContactPointData
    subtype: CPSubtype