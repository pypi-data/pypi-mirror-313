from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, field_validator
from zoneinfo import ZoneInfo
from enum import StrEnum

from .....utils.types import Status

class MetaConversationOriginType(StrEnum):
    authentication = "authentication"
    marketing = "marketing"
    utility = "utility"
    service = "service"
    referral_conversion = "referral_conversion"

class Origin(BaseModel):
    type: MetaConversationOriginType

class Conversation(BaseModel):
    id: str
    expiration_timestamp: Optional[str] = None
    origin: Optional[Origin] = None

class Pricing(BaseModel):
    billable: bool
    pricing_model: str
    category: str

class ErrorData(BaseModel):
    details: str

class ErrorDetail(BaseModel):
    code: int
    title: str
    message: Optional[str] = None
    error_data: Optional[ErrorData] = None
    href: Optional[str] = None

class StatusNotification(BaseModel):
    id: str
    status: Status
    timestamp: datetime
    recipient_id: str
    conversation: Optional[Conversation] = None
    pricing: Optional[Pricing] = None
    errors: Optional[List[ErrorDetail]] = None

    @field_validator('timestamp')
    def ensure_utc(cls, v):
        if isinstance(v, str):
            v = datetime.fromtimestamp(int(v))
        if isinstance(v, datetime):
            return v.replace(tzinfo=ZoneInfo("UTC")) if v.tzinfo is None else v.astimezone(ZoneInfo("UTC"))
        raise ValueError('must be a datetime')