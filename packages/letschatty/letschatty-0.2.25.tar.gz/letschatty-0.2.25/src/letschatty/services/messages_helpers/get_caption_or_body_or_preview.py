from ...models.messages.chatty_messages import ChattyMediaMessage, TextMessage, ChattyMessage, ImageMessage, VideoMessage, AudioMessage, DocumentMessage, StickerMessage, ReactionMessage, ContactMessage, LocationMessage

class MessageTextOrCaptionOrPreview:
    @staticmethod
    def get_caption_or_body(message: ChattyMessage) -> str:
        if isinstance(message, ChattyMediaMessage):
            if hasattr(message.content, "caption"):
                return message.content.caption
            else:
                return ""
        elif isinstance(message, TextMessage):
            return message.content.body
        else:
            return ""
        
    @staticmethod
    def get_content_preview(message: ChattyMessage) -> str:
        if isinstance(message, TextMessage):
            return message.content.body
        elif isinstance(message, ContactMessage):
            return "👥 Envió un contacto" if message.is_incoming_message else "👥 Enviaste un contacto"
        elif isinstance(message, LocationMessage):
            return "📍 Envió una ubicación" if message.is_incoming_message else "📍 Enviaste una ubicación" 
        elif isinstance(message, ImageMessage):
            return "🖼️ Envió una imagen" if message.is_incoming_message else "🖼️ Enviaste una imagen"
        elif isinstance(message, VideoMessage):
            return "🎥 Envió un video" if message.is_incoming_message else "🎥 Enviaste un video"
        elif isinstance(message, AudioMessage):
            return "🔊 Envió un audio" if message.is_incoming_message else "🔊 Enviaste un audio"
        elif isinstance(message, DocumentMessage):
            return "📄 Envió un documento" if message.is_incoming_message else "📄 Enviaste un documento"
        elif isinstance(message, StickerMessage):
            return "😀 Envió un sticker" if message.is_incoming_message else "😀 Enviaste un sticker"
        elif isinstance(message, ReactionMessage):
            return "❤️ Reaccionó a un mensaje" if message.is_incoming_message else "❤️ Reaccionaste a un mensaje"
        else:
            return "preview content"
