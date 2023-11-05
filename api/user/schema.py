from marshmallow import Schema, fields


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    repeat_password = fields.Str(required=True)
    # TODO add a validator method to check if password and repeat password are the same
    # TODO add a validator for minimum requirements of password(length, symbols, letters, numbers)
