from pydantic import BaseModel, Field
from typing import Optional

class MetaRegister(BaseModel):
    waba_id: str
    phone_number_id: str
    code: str
    root_user_email: str
    root_user_name: str
    access_token: Optional[str] = Field(default=None)
    company_id: Optional[str] = Field(default=None)
    company_name: Optional[str] = Field(default=None)