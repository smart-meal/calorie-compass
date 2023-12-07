import re
from functools import wraps
from flask import request
from marshmallow import Schema, fields, validates_schema, ValidationError

class UserSchema(Schema):
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    age = fields.Int(required=False)
    height = fields.Decimal(required=False)
    weight = fields.Decimal(required=False)
    goal =  fields.Str(required=False)
    lifestyle = fields.Str(required=False)
    allergies = fields.Str(required=False)
    body_type = fields.Str(required=False)
    bmi = fields.Decimal(required=False)

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
        if data["goal"].upper() != "MAINTAIN WEIGHT" and data["goal"].upper() != "LOSE WEIGHT" and data["goal"].upper() != "GAIN WEIGHT":
            raise ValidationError("Invalid option choosen.")
        if data["lifestyle"].upper() != "LAZY" and data["lifestyle"].upper() != "SEDENTARY" and data["lifestyle"].upper() != "ACTIVE" and data["lifestyle"] != "MODERATE":
            raise ValidationError("Invalid option choosen.")



class UsernameSchema(Schema):
    username = fields.Str(required=True)

    @validates_schema
    def validate_username(self, data, **kwargs):  # pylint: disable=unused-argument
    
      if not re.search(r"[!@#$%^&*(_-=+;?/`~),.?\":{}|<>]", data["username"]):
            raise ValidationError("Username should not contain any special character")
          
      if not re.search(r"[0-9]", data["username"]):
            raise ValidationError("Username must contain atlst one number")

      
      if len(data["username"]) > 25:
         raise ValidationError("Username should not be more than 25 characters")
      


def validate_with_schema(schema_cls):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                request_json = request.get_json()
                validated_data = schema_cls().load(request_json)
                # Add the validated data to kwargs so it can be used in the route
                kwargs['validated_data'] = validated_data
            except ValidationError as err:
                return err.messages, 422
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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
