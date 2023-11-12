from flask import Blueprint, request
from marshmallow import ValidationError

from api.chat.schema import NewMessageSchema
from api.chat.service import send_message
from api.util.auth import require_session

chat_blueprint = Blueprint('chat', __name__, url_prefix='/chat')


@chat_blueprint.route('/history', methods=('GET',))
@require_session
def get_messages():
    schema = NewMessageSchema()
    try:
        request_json = request.get_json()
        validated_data = schema.load(request_json)
    except ValidationError as err:
        return err.messages, 422
    message = validated_data['message']

    return send_message(message)
