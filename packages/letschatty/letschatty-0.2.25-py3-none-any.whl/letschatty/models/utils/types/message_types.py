from enum import StrEnum

"""https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/components"""

class MessageType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
    STICKER = "sticker"
    AUDIO = "audio"
    REACTION="reaction"
    CENTRAL="central"
    CONTACT = "contacts"
    LOCATION = "location"
    UNKNOWN = "unknown"
    UNSUPPORTED = "unsupported"
    INTERACTIVE = "interactive"
    SYSTEM = "system"
    ERRORS = "errors"
    
    @staticmethod
    def values():
        return [member.value for member in MessageType]
    
    @staticmethod
    def special_system_messages():
        return [MessageType.SYSTEM, MessageType.ERRORS, MessageType.UNKNOWN, MessageType.UNSUPPORTED]
    
    @staticmethod
    def uncontrolled_messages():
        return [MessageType.INTERACTIVE, MessageType.LOCATION]
    
    @staticmethod
    def controlled_messages():
        return [member.value for member in MessageType if member not in MessageType.special_system_messages() + MessageType.uncontrolled_messages()]
    
class MessageSubtype(StrEnum):
    TEMPLATE = "template"
    CHATTY_FAST_ANSWER = "chatty_fast_answer"
    NONE = ""
