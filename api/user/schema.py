import re
from datetime import date
from marshmallow import Schema, fields, validates_schema, ValidationError

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    repeat_password = fields.Str(required=True)

    @validates_schema
    def validate_numbers(self, data, **kwargs):  # pylint: disable=unused-argument

        if data["password"] != data["repeat_password"]:
            raise ValidationError("Password do not match")

        if len(data["password"]) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", data["password"]):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", data["password"]):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", data["password"]):
            raise ValidationError("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", data["password"]):
            raise ValidationError("Password must contain at least one special character")

class UpdatePasswordSchema(Schema):
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True)
    repeat_password = fields.Str(required=True)

    @validates_schema
    def validate_numbers(self, data, **kwargs):  # pylint: disable=unused-argument
        if data["new_password"] != data["repeat_password"]:
            raise ValidationError("Password do not match")

        if len(data["new_password"]) < 8:
            raise ValidationError("Password must be at least 8 characters long")

        if not re.search(r"[A-Z]", data["new_password"]):
            raise ValidationError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", data["new_password"]):
            raise ValidationError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", data["new_password"]):
            raise ValidationError("Password must contain at least one digit")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", data["new_password"]):
            raise ValidationError("Password must contain at least one special character")

class MealSchema(Schema):
    title = fields.Str(required=True)
    meal_date = fields.Date(required=True)
    description = fields.Str()
    weight = fields.Float()
    calories = fields.Float()
    fat = fields.Float()
    carbs = fields.Float()
    proteins = fields.Float()
    picture_url = fields.Str()

    @validates_schema
    def validate_date(self, data, **kwargs):
        if "meal_date" in data and data["meal_date"] is not None:
            if data["meal_date"] > date.today():
                raise ValidationError("Date cannot be in the future")
