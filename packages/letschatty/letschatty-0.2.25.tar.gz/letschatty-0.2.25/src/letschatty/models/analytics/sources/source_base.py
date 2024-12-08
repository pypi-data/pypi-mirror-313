from typing import List, Optional, Dict
from pydantic import Field, model_validator, field_validator
from abc import abstractmethod

from ...utils.types.source_types import SourceType, SourceCheckerType
from ...utils.custom_exceptions import InvalidSourceChecker
from ...utils.types.identifier import StrObjectId
from .helpers import SourceHelpers
from ...base_models import ChattyAssetModel

class SourceBase(ChattyAssetModel):
    agent_email: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default="")
    tags: List[StrObjectId] = Field(default_factory=list)
    products: List[StrObjectId] = Field(default_factory=list)
    flow: List[StrObjectId] = Field(default_factory=list)
    trackeable: bool = Field(default=True)
    category: str = Field(default="")
    source_checker: SourceCheckerType
    name: str = Field()
    
    def model_dump(self, *args, **kwargs) -> Dict:
        kwargs["by_alias"] = True
        data = super().model_dump(*args, **kwargs)
        data["type"] = self.type
        return data    
    
    @field_validator('source_checker', mode="before")
    @classmethod
    def lowercase_source_checker(cls, v: str) -> str:
        return v.lower()
    
    @model_validator(mode='after')
    def validate_source(self):
        if not SourceHelpers.is_valid_source_checker(source_type=self.type,source_checker=self.source_checker):
            raise InvalidSourceChecker(f"Source checker {self.source_checker} not valid for source type {self.type} | Allowed ones are {SourceHelpers.get_source_checkers(self.type)}")
        if self.category == "":
            self.category = self.type
        return self
    
    @property
    @abstractmethod
    def type(self) -> SourceType:
        pass