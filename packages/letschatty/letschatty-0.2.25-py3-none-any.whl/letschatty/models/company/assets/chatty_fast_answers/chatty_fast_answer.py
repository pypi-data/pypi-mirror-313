from __future__ import annotations
from pydantic import ConfigDict, model_validator
from typing import List
from ....messages.chatty_messages import MessageDraft
from ....base_models.chatty_asset_model import ChattyAssetModel
from ....messages.chatty_messages.schema import ChattyContext
from ....utils.types.message_types import MessageSubtype
from ....utils.types.serializer_type import SerializerType
class ChattyFastAnswer(ChattyAssetModel):
    name: str
    messages: List[MessageDraft]
    
    exclude_fields = {
        SerializerType.FRONTEND_ASSET_PREVIEW: {"messages"}
    }
    
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    @model_validator(mode='after')
    def set_context_and_subtype_on_messages(self):
        for message in self.messages:
            message.context = ChattyContext(response_id=self.id)
            message.subtype = MessageSubtype.CHATTY_FAST_ANSWER
        return self
