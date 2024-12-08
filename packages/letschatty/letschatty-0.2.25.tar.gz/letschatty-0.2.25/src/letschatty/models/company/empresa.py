from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from ...models.users.user import User

class EmpresaModel(BaseModel):
    id: str = Field(description="The id of the company for mongo", alias="_id")
    created_at: datetime
    updated_at: datetime
    name: str
    industry: Optional[str] = Field(default = "")
    url: Optional[str] = Field(default = "")
    allowed_origins: Optional[list[str]] = Field(default_factory=lambda: [])
    company_email: Optional[str] = Field(default = "")
    contributor_count: Optional[str] = Field(default = "")
    purpose_of_use_chatty: Optional[List[str]] = Field(default_factory=lambda: [])
    current_wpp_approach: Optional[str] = Field(default = "")
    main_reason_to_use_chatty: Optional[str] = Field(default = "")
    active: Optional[bool] = Field(default = True)
    friendly_aliases: Optional[list[str]] = Field(description="The friendly aliases of the company used for the enviamewhats.app links", default = [])
    terms_of_service_agreement: Optional[bool] = Field(default = False)
    root_user: User = Field(description="The root user of the company")
    display_phone_number: Optional[str] = Field(description="The display phone number user's write to", default = "")
    phone_number_id: Optional[str] = Field(description="The phone number id of the company", default = "", alias = "company_id")
    bussiness_account_id: Optional[str] = Field(description="The WABA - WhatsApp Business Account id of the company", default = "")
    photo_url: str = Field(default = "")
    meta_token: Optional[str] = Field(default = None)
    slack_channel_id: Optional[str] = Field(default=None)
    phone_numbers_for_testing: list[str] = Field(default_factory=lambda: [])
    
    model_config = ConfigDict(
        populate_by_name=True
    )
    
    @field_validator("name", mode="before")
    def validate_name(cls, v):
        return v.replace(" ", "_")
    
    