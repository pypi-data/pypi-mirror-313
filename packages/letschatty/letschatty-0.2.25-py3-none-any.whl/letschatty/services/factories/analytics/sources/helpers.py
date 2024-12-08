from typing import Type
from .....models.utils.types.source_types import SourceType
from .....models.analytics.sources import OtherSource, PureAd, WhatsAppDefaultSource, TopicDefaultSource, UTMSource, Source

class SourceFactoryHelpers:
    @staticmethod
    def source_type_to_class(source_type: SourceType) -> Type[Source]:
        return {
            SourceType.OTHER_SOURCE: OtherSource,
            SourceType.PURE_AD: PureAd,
            SourceType.WHATSAPP_DEFAULT_SOURCE: WhatsAppDefaultSource,
            SourceType.TOPIC_DEFAULT_SOURCE: TopicDefaultSource,
            SourceType.UTM_SOURCE: UTMSource
        }[source_type]