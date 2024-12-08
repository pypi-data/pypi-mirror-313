from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentLocation

class LocationMessage(Message):
    type: str = MessageType.LOCATION.value
    content: ChattyContentLocation