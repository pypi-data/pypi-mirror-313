from datetime import datetime

from ....models.utils import Status, MessageSubtype
from ....models.messages import TextMessage
from ....models.messages.chatty_messages.schema import ChattyContentText, ChattyContext

class fromTemplateFactory:
    """This factory takes a message request and instantiates the corresponding ChattyMessage"""
    @staticmethod
    def from_template(message_id: str, body: str, template_name: str, campaign_id: str, agent_email: str, created_at: datetime, updated_at: datetime, status: Status) -> TextMessage:
        return fromTemplateFactory.instantiate_message(message_id=message_id, body=body, template_name=template_name, campaign_id=campaign_id, agent_email=agent_email, created_at=created_at, updated_at=updated_at, status=status)

    @staticmethod
    def instantiate_message(message_id: str, body: str, template_name: str, campaign_id: str | None, agent_email: str, created_at: datetime, updated_at: datetime, status: Status) -> TextMessage:
        return TextMessage(
            id=message_id,
            created_at=created_at,
            updated_at=updated_at,
            content=ChattyContentText(body=body),
            status=status,
            is_incoming_message=False,
            context=ChattyContext(template_name=template_name, campaign_id=campaign_id),
            sent_by=agent_email,
            subtype=MessageSubtype.TEMPLATE
        )