from __future__ import annotations
from typing import Dict, TYPE_CHECKING
from ...models.analytics.sources import Source, WhatsAppDefaultSource, TopicDefaultSource, PureAd, OtherSource
from ...models.utils.custom_exceptions.custom_exceptions import ConflictedSource, DuplicatedMessage
if TYPE_CHECKING:
    from ...models.analytics.smart_messages.topic import Topic

class SourcesAndTopicsValidator:
    """This class provides methods to validate sources and topics."""
    @staticmethod
    def source_validation_check(sources : Dict[str,Source], topics : Dict[str,Topic], source : Source) -> None:
        """Checks validation of a source against other sources and topics."""
        SourcesAndTopicsValidator.validate_source_against_sources(sources = sources, source = source)
        SourcesAndTopicsValidator.validate_source_against_topics(topics = topics, source = source)        
        return None
    
    @staticmethod
    def topic_validation_check(topics : Dict[str,Topic], sources: Dict[str,Source], topic : Topic) -> None:
        SourcesAndTopicsValidator.validate_topic_against_sources(sources = sources, topic = topic)
        SourcesAndTopicsValidator.validate_topic_against_topics(topics = topics, topic = topic)
        return None
    
    @staticmethod
    def validate_source_against_sources(sources : Dict[str,Source], source : Source) -> None:
        """This method checks that no duplicated source is created.
        For Pure Ads, it checks that the ad_id is unique and doesn't exist already.
        For Other Sources, it checks that exact trigger doesn't exist already. """
        for source_id, source_to_check in sources.items():
            if source_id == source.id:
                continue
            if source == source_to_check:
                if isinstance(source, OtherSource):
                    raise ConflictedSource(f":warning: *Conflict while adding source: Trigger already exists* \n New source '{source.name}' \n- Id {source._id} \n- Trigger {source.trigger[:30]} \n Existing source '{source_to_check.name}' \n- Id {source_to_check._id} \n- Trigger '{source_to_check.trigger[:30]}'")
                if isinstance(source, PureAd):
                    raise ConflictedSource(f":warning: Source '{source.name}' with that #ad_id {source.ad_id} ({type(source.ad_id)}) already exists for source {source_to_check.name}, #ad_id {source_to_check.ad_id} ({type(source_to_check.ad_id)})")
                if isinstance(source, TopicDefaultSource):
                    raise ConflictedSource(f":warning: Source '{source.name}' with that topic_id '{source.topic_id}' already exists for source '{source_to_check.name}', id={source_id}")
                if isinstance(source, WhatsAppDefaultSource):
                    raise ConflictedSource(f":warning: WhatsApp default source already exists, id={source_id}")
        return None    
    
    @staticmethod
    def validate_source_against_topics(topics : Dict[str,Topic], source : Source) -> None:
        """This method compares the messages of a topic with the trigger of a source.
        If a message of the topic is found in the source trigger, it raises a ConflictedSource exception."""
        if not hasattr(source, "trigger") or source.trigger == "":
            return None
        for topic_id, topic in topics.items():
            SourcesAndTopicsValidator.validate_topic_against_trigger(topic, source)
    
    @staticmethod
    def validate_topic_against_sources(sources : Dict[str,Source], topic : Topic) -> None:
        """This method compares the messages of a topic with the trigger of a source.
        If a message of the topic is found in the source trigger, it raises a ConflictedSource exception."""
        for source_id, source_to_check in sources.items():
            if not hasattr(source_to_check, "trigger") or source_to_check.trigger == "":
                continue
            SourcesAndTopicsValidator.validate_topic_against_trigger(topic, source_to_check)
    
    @staticmethod
    def validate_topic_against_topics(topics : Dict[str,Topic], topic : Topic) -> None:
        """This method compares the messages of a topic with the messages of other topics.
        If a message of the topic is found in the messages of other topics, it raises a DuplicatedMessage exception."""
        for topic_id, topic_to_check in topics.items():
            if topic_id == topic.id:
                continue
            SourcesAndTopicsValidator.validate_topic_one_on_one(topic, topic_to_check)

    @staticmethod
    def validate_topic_one_on_one(topic: Topic, other: Topic) -> None:
        for message in other.messages:
            if message in topic.messages:
                raise DuplicatedMessage(f"Topic {other.name} #id {other.id} has a conflcit with topic {topic.name} #id {topic.id} in message {message.content}")
            
    @staticmethod
    def validate_topic_against_trigger(topic: Topic, source : Source) -> None:
        trigger : str = source.trigger
        for message in topic.messages:
            if message.content in trigger or trigger in message.content or message.content == trigger:
                raise DuplicatedMessage(f"Topic {topic.name} has a conflcit with trigger {trigger} in source #id {source.id} in message {message.content}")
