from pydantic import BaseModel, Field, model_validator
from typing import Optional
from .content_media import ChattyContentMedia

class ChattyContentDocument(ChattyContentMedia):
    filename: Optional[str] = Field(default=None, description="Name of the document")
    
    @model_validator(mode='after')
    def validate_filename(cls, values):
        if not values.filename and values.url:
            values.filename = values.url.split("/")[-1]
        return values