from enum import StrEnum

class SourceType(StrEnum):
    OTHER_SOURCE = "other_source"
    PURE_AD = "pure_ad"
    DEFAULT_SOURCE = "default_source"
    WHATSAPP_DEFAULT_SOURCE = "whatsapp_default_source"
    TOPIC_DEFAULT_SOURCE = "topic_default_source"
    UTM_SOURCE = "utm_source"

from enum import StrEnum

class SourceCheckerType(StrEnum):
    SMART_MESSAGES = "smart_messages"
    SIMILARITY = "similarity"
    FIRST_CONTACT = "first_contact"
    REFERRAL = "referral"
    LITERAL = "literal"

source_checker_types_schema = {
    SourceCheckerType.SMART_MESSAGES: {
        "label": "Smart Messages de Chatty (recomendado)",
        "description": "Chatty administra y asigna mensajes de forma inteligente para hacer el seguimiento de la fuente de origen del contacto."
    },
    SourceCheckerType.SIMILARITY: {
        "label": "Coincidencia por significado con IA",
        "description": "Existirá match cuando el texto disparador sea similar en significado (evaluado con técnicas de IA) al mensaje que envíe el usuario."
    },
    SourceCheckerType.LITERAL: {
        "label": "Coincidencia exacta dentro del mensaje",
        "description": "Existirá match sólo cuando el texto disparador esté literalmente incluido en el mensaje que envíe el usuario."
    },
    SourceCheckerType.FIRST_CONTACT: {
        "label": "Primer contacto (nuevo chat) sin fuente de origen",
        "description": "Método interno de Chatty utilizado para asignar la fuente de origen predeterminada de WhatsApp a nuevos contactos que no tienen una fuente de origen específica."
    },
    SourceCheckerType.REFERRAL: {
        "label": "Anuncios Click to WhatsApp (META)",
        "description": "Chatty reconoce directamente los anuncios de Click to WhatsApp de META como fuentes de origen, identificando el ID del anuncio."
    },
}

def get_label(source_checker_type: SourceCheckerType) -> str:
    return ""
    return source_checker_types_schema[source_checker_type]["label"]

def get_description(source_checker_type: SourceCheckerType) -> str:
    return source_checker_types_schema[source_checker_type]["description"]