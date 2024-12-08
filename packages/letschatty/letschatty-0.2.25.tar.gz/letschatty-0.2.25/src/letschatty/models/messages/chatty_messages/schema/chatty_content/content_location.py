from pydantic import BaseModel

class ChattyContentLocation(BaseModel):
    latitude: float
    longitude: float
