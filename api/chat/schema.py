from marshmallow import Schema, fields, validate


class NewMessageSchema(Schema):
    message = fields.Str(required=True, validate=validate.Length(max=400))
