from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, ValidationInfo

from typing import List, Dict, Optional, Any
from datetime import datetime

from ....utils.types.message_types import MessageType, MessageSubtype
from ..schema import ChattyContent, ChattyContext, ChattyContentText, ChattyContentImage, ChattyContentVideo, ChattyContentDocument, ChattyContentSticker, ChattyContentAudio, ChattyContentContacts, ChattyContentLocation, ChattyContentCentral, ChattyContentReaction

    
class MessageDraft(BaseModel):
    """This class validates and represents the content of a message that's not yet instantiated.
    It's used to validate either a message request from the frontend, or the messages inside a ChattyResponse"""
    type: MessageType
    content: ChattyContent
    context: Optional[ChattyContext] = Field(default_factory=ChattyContext.default)
    subtype: Optional[MessageSubtype] = Field(default=MessageSubtype.NONE)

    @field_validator('content', mode='before')
    def validate_content(cls, v, values: ValidationInfo):
        if isinstance(v,ChattyContent):
            return v
        message_type = values.data.get('type')
        content_class = {
            MessageType.TEXT: ChattyContentText,
            MessageType.IMAGE: ChattyContentImage,
            MessageType.VIDEO: ChattyContentVideo,
            MessageType.DOCUMENT: ChattyContentDocument,
            MessageType.STICKER: ChattyContentSticker,
            MessageType.AUDIO: ChattyContentAudio,
            MessageType.CONTACT: ChattyContentContacts,
            MessageType.LOCATION: ChattyContentLocation,
            MessageType.CENTRAL: ChattyContentCentral,
            MessageType.REACTION: ChattyContentReaction,
        }.get(message_type)

        if content_class is None:
            raise ValueError(f"Invalid message type: {message_type} - valid types: {MessageType.values()}")

        return content_class(**v)

    @field_validator('context', mode='before')
    def validate_context(cls, v):
        if isinstance(v,ChattyContext):
            return v
        if v is not None:
            return ChattyContext(**v)
        return v    

class SendMessagesFromAgentToChat(BaseModel):
    agent_email: str
    chat_id: str
    messages: List[MessageDraft]