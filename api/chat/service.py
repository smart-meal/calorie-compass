from typing import Dict, List

from api.chat.model import Message, MessageType
from api.util.auth import get_user_id_from_session
from api.util.chatbot import get_chat_from_messages
from api.util.log import logger


def get_assistant_response(m: Message, context: List[Message]):
    c = get_chat_from_messages(context)
    response = c.send_message(m.text)
    return response


def send_message(message: str):
    user_id = get_user_id_from_session()
    m = Message(user_id=user_id, text=message, type=MessageType.USER)
    context = get_previous_conversation_context(user_id)
    response_text = get_assistant_response(m, context)
    response = Message(user_id=user_id, text=response_text, type=MessageType.ASSISTANT)
    m.save()
    response.save()
    return response


def get_previous_conversation_context(user_id):
    most_recent_filter = {
        "page": 1,
        "per_page": 3,
        "newest_first": True,
        "types": MessageType.get_all_types()
    }
    previous_messages = get_messages(most_recent_filter)
    system_filter = {
        "page": 1,
        "per_page": 3,
        "newest_first": True,
        "types": [MessageType.SYSTEM]
    }
    system_messages = get_messages(system_filter)
    logger.info(
        "Found '%s' previous and '%s' system messages for '%s'",
        len(previous_messages),
        len(system_messages),
        user_id
    )
    context = []
    context.extend(system_messages)
    context.extend(previous_messages)
    return context


def get_messages(message_filter: Dict):
    user_id = get_user_id_from_session()
    page = message_filter['page']
    per_page = message_filter['per_page']
    skip = (page - 1) * per_page
    ascending = not message_filter['newest_first']
    ascending = "+" if ascending else "-"
    types = message_filter['types']

    # pylint: disable=no-member
    return Message \
        .objects(user_id=user_id, type__in=types) \
        .order_by(ascending + "date") \
        .skip(skip) \
        .limit(per_page)


def clean_user_chat_history():
    user_id = get_user_id_from_session()
    # pylint: disable=no-member
    result = Message.objects(user_id=user_id).delete()
    logger.info("Deleted '%s' messages for '%s'", result, user_id)
