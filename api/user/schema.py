import re

from marshmallow import Schema, fields, validates_schema, ValidationError

class UserSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=False)
    age = fields.Int(required=False)
    height = fields.Int(required=False)
    weight = fields.Int(required=False)
    goal =  fields.Str(required=False)
    lifestyle = fields.Str(required=False)
    allergies = fields.Str(required=False)
    body_type = fields.Str(required=False)
    bmi = fields.Int(required=False)

    @validates_schema
    def validate_user(self, data, **kwargs):  # pylint: disable=unused-argument

        if not re.search(r"[A-Za-z'-]", data["first_name"]):
            raise ValidationError("Invalid character used in first name.")
        if not re.search(r"[A-Za-z'-]", data["last_name"]):
            raise ValidationError("Invalid character used in last name.")
        if data["age"]<0:
            raise ValidationError("Age can not be less than zero.")
        if data["height"]<0:
            raise ValidationError("Height can not be less than zero.")
        if data["weight"]<0:
            raise ValidationError("Weight can not be less than zero.")
        if data["goal"].upper() == "MAINTAIN THE WEIGHT" or data["goal"].upper() == "LOSE WEIGHT" or data["goal"].upper() == "GAIN WEIGHT":
            raise ValidationError("Invalid option choosen.")
        if data["lifestyle"].upper() == "LAZY" or data["lifestyle"].upper() == "SEDENTARY" or data["lifestyle"].upper() == "ACTIVE" or data["lifestyle"] == "MODERATE":
            raise ValidationError("Invalid option choosen.")
          

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
