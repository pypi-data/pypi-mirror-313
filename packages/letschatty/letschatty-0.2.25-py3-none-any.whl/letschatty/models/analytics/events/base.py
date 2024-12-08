from pydantic import BaseModel, Field
from enum import StrEnum
from bson import ObjectId
from datetime import datetime, timezone
from typing import Dict, Any
from .event_types import EventType
from ...utils.types.identifier import StrObjectId
import re

class ChattyCloudEvent(BaseModel):
    id: StrObjectId = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    source: str = Field(..., pattern=r"com\.chatty/[a-z-]+/[a-zA-Z0-9-]+")
    specversion: str = Field(default="1.0")
    type: EventType
    time: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc))
    datacontenttype: str = Field(default="application/json")
    data: Dict[str, Any]

class ClientEvent(ChattyCloudEvent):
    """Used for client related events, either management wise like an agent event or a business logic event like a new_chat."""
    source: str = Field(..., pattern=r"com\.chatty/clients/[a-zA-Z0-9-]+")

    @property
    def client_id(self) -> str:
        match = re.search(r"com\.chatty/clients/([a-zA-Z0-9-]+)", self.source)
        if match:
            return match.group(1)
        raise ValueError("Invalid source format")

class InternalEvent(ChattyCloudEvent):
    """Used for internal events such as a new client, some billing, etc."""
    source: str = Field(..., pattern=r"com\.chatty/internal/[a-z-]+")

class BusinessLogicEvent(ClientEvent):
    """Used for business logic events, such as a quality scoring."""
    source: str = Field(..., pattern=r"com\.chatty/business-logic/[a-zA-Z0-9-]+")

class BusinessLogicEventData(BaseModel):
    channel_id : str
    chat_id : StrObjectId
    client_channel_user_id : str = Field(..., alias="waid")
    company_phone_number_id : str
    subtype : StrEnum

    
