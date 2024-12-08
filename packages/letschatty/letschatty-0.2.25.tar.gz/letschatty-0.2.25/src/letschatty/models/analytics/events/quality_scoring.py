from .base import BusinessLogicEventData, BusinessLogicEvent
from .event_types import EventType
from enum import StrEnum

class QualityScore(StrEnum):
    BAD = "bad"
    GOOD = "good"
    NEUTRAL = "neutral"

class QualityScoringData(BusinessLogicEventData):
    score : QualityScore

class QualityScoringEvent(BusinessLogicEvent):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    type: EventType = EventType.QUALITY_SCORING
    data: QualityScoringData