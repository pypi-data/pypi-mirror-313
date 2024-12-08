from typing import Optional
from pydantic import Field, model_validator

from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType
from ...utils.types.identifier import StrObjectId
from .utms.utm_query_params import QueryUTMParams

class UTMSource(SourceBase):
    topic_id: StrObjectId
    utm_parameters: QueryUTMParams
    source_checker: SourceCheckerType = Field(default=SourceCheckerType.SMART_MESSAGES)

    @property
    def type(self) -> SourceType:
        return SourceType.UTM_SOURCE
    
    @model_validator(mode='before')
    @classmethod
    def validate_utm_parameters(cls, data: dict) -> dict:
        """Validate and convert utm_parameters if needed"""
        utm_params = data.get('utm_parameters')
        if not utm_params:
            raise ValueError("UTM parameters are required")
        if not isinstance(utm_params, QueryUTMParams):
            data['utm_parameters'] = QueryUTMParams(**utm_params)
        return data

    def get_utm(self) -> str:
        """Get the full UTM URL"""
        return self.utm_parameters.get_utm()
    
    def model_dump(self, *args, serializer: str = "json", **kwargs) -> dict:
        """Custom serialization based on context"""
        data = super().model_dump(*args, **kwargs)
        
        match serializer:
            case "frontend":
                data["full_url"] = self.get_utm()
        return data
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UTMSource):
            return False
        return self.utm_parameters == other.utm_parameters
    
    def __hash__(self) -> int:
        return hash(self.utm_parameters)