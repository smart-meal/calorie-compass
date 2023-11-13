from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.chat.schema import MessageFilterSchema, NewMessageSchema
from api.chat.service import get_messages, send_message
from api.util.auth import require_session

chat_blueprint = Blueprint('chat', __name__, url_prefix='/chat')


@chat_blueprint.route('/history', methods=('POST',))
@require_session
def get_filtered_messages():
    schema = MessageFilterSchema()
    try:
        request_json = request.get_json()
        validated_data = schema.load(request_json)
    except ValidationError as err:
        return err.messages, 422
    messages = get_messages(validated_data)
    messages_converted = [i.to_dict() for i in messages]
    return jsonify(messages_converted)


@chat_blueprint.route('/new', methods=('POST',))
@require_session
def send_new_message():
    schema = NewMessageSchema()
    try:
        request_json = request.get_json()
        validated_data = schema.load(request_json)
    except ValidationError as err:
        return err.messages, 422
    message = validated_data['message']
    response = send_message(message)
    return jsonify(response)
