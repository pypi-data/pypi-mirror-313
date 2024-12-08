from letschatty.models.analytics.smart_messages.topic import Topic
from letschatty.models.analytics.smart_messages.topic_message import MessageTopic
class TopicFactory:
    
    @staticmethod
    def instantiate_topic(topic_data: dict) -> Topic:
        topic_messages = []
        for m in topic_data['messages']:
            m = MessageTopic(**m)
            for topic_message in topic_messages:
                m.check_message_conflict(topic_message)
            topic_messages.append(m)
        topic_data['messages'] = topic_messages
        return Topic(**topic_data)
