from .base.message_base import Message
from ...utils.types.message_types import MessageType
from .schema import ChattyContentContacts

class ContactMessage(Message):
    type: MessageType = MessageType.CONTACT
    content: ChattyContentContacts