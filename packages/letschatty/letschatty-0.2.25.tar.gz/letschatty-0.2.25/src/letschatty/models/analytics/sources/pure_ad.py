from __future__ import annotations
from pydantic import Field, ConfigDict
from .source_base import SourceBase
from ...utils.types.source_types import SourceType, SourceCheckerType

class PureAd(SourceBase):
    ad_id: str
    source_checker: SourceCheckerType = Field(default=SourceCheckerType.REFERRAL)
    
    model_config = ConfigDict(extra='ignore')

    @property
    def type(self) -> SourceType:
        return SourceType.PURE_AD
    
    def __eq__(self, other: PureAd) -> bool:
        if not isinstance(other, PureAd):
            return False
        return bool(self.ad_id and other.ad_id and self.ad_id == other.ad_id)
    
    def __hash__(self) -> int:
        return hash(self.ad_id)