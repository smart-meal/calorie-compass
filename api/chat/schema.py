from marshmallow import Schema, fields, validate, validates, ValidationError

from api.chat.model import MessageType


class NewMessageSchema(Schema):
    message = fields.Str(required=True, validate=validate.Length(max=400))


class MessageFilterSchema(Schema):
    per_page = fields.Integer(required=False, default=3, missing=3)
    page = fields.Integer(required=False, default=1, missing=1)
    types = fields.List(
        fields.Enum(enum=MessageType, required=True),
        required=False,
        missing=MessageType.get_regular_message_types,
    )
    newest_first = fields.Boolean(required=False, default=True, missing=True)

    @validates('per_page')
    def validate_per_page(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValidationError("Field must be a positive integer.")

    @validates('page')
    def validate_page(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValidationError("Field must be a positive integer.")
