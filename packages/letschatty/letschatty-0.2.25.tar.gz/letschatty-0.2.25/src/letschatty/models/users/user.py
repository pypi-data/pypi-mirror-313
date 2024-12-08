from pydantic import BaseModel, Field, ConfigDict

class User(BaseModel):
    name: str = Field(alias="nombre")
    email: str
    is_admin: bool

    model_config = ConfigDict(
        populate_by_name=True
    )