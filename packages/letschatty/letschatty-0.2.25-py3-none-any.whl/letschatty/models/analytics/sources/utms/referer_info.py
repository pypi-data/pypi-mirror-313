from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from ....utils.types.identifier import StrObjectId
from enum import StrEnum

class DeviceType(StrEnum):
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    UNKNOWN = "unknown"

class RefererInfo(BaseModel):
    url: str
    topic_id: StrObjectId
    button_id: str
    timestamp: datetime
    button_name: str = Field(default="")
    device_type: DeviceType = Field(default=DeviceType.UNKNOWN)
    contact_point_id: StrObjectId = Field(default_factory=lambda: str(ObjectId()))
    
