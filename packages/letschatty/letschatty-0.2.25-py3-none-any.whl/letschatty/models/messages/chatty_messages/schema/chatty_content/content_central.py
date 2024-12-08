from pydantic import BaseModel

# Soolo se generan DESDE LA BASE DE DATOS
class ChattyContentCentral(BaseModel):
    body: str