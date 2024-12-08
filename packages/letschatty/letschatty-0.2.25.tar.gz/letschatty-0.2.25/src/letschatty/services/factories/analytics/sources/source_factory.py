from __future__ import annotations
from typing import Dict, Type, TYPE_CHECKING
import logging

from .....models.analytics.sources import WhatsAppDefaultSource, TopicDefaultSource, PureAd, Source
from .....models.utils.types.source_types import SourceType
from .helpers import SourceFactoryHelpers

if TYPE_CHECKING:
    from .....models.messages import ChattyMessage
    from .....models.analytics.smart_messages.topic import Topic
    
logger = logging.getLogger(__name__)

class SourceFactory:

    @staticmethod
    def instantiate_source(source_data: dict) -> Source:
        """Instantiate a source from a dictionary.
        1) from mongo
        2) from a request (if its new, it creates the id for posterior mongo insertion)
        """
        source_type = source_data.get("type")
        source_class : Source = SourceFactoryHelpers.source_type_to_class(source_type)
        try:
            return source_class(**source_data)
        except Exception as e:
            logger.error(f"Error creating source of type {source_type}: {str(e)}")
            raise e
    
    @staticmethod
    def create_whatsapp_default_source() -> WhatsAppDefaultSource:
        return WhatsAppDefaultSource()

    @staticmethod
    def create_topic_default_source(topic: Topic) -> TopicDefaultSource:
        return TopicDefaultSource(topic_id=topic.id, name = f"{topic.name} Topic Default Source", _id = topic.default_source_id, description= "Message matched the Topic but there was no direct source to attribute it to.", created_at=topic.created_at, updated_at=topic.updated_at)
    
    @staticmethod
    def create_new_pure_ad_not_loaded(message: ChattyMessage) -> PureAd:
        body = message.referral.body
        headline = message.referral.headline
        source_url = message.referral.source_url
        ad_id = message.referral.source_id
        name_for_ad = f"Anuncio Meta no identificado {ad_id} {headline}"
        description = f"El anuncio fue creado con el nombre '{name_for_ad}' y puede ser editado en la configuración de fuentes de origen. \n Info del anuncio: {source_url} - {body}"
        
        source_data = {
            "agent_email": "source_checker@letschatty.com",
            "name": name_for_ad,
            "type": SourceType.PURE_AD,
            "ad_id": ad_id,
            "description": description,
            "trackeable": True
        }

        return SourceFactory.instantiate_source(source_data)