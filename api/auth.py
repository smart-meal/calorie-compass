from typing import Callable

from flask import (
    Blueprint, request, session, jsonify
)
from marshmallow import Schema, fields, ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from api.user.model import User
from api.user.service import get_user_by_username


def require_session(func: Callable):
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            # Session data is valid, continue with the request
            return func(*args, **kwargs)
        else:
            # Session data is not valid, redirect to a login page or perform another action
            return jsonify({"error": "Unauthorized"}), 401

    return wrapper


bp = Blueprint('auth', __name__, url_prefix='/auth')


class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class RegisterSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    repeat_password = fields.Str(required=True)
    # TODO add a validator method to check if password and repeat password are the same
    # TODO add a validator for minimum requirements of password(length, symbols, letters, numbers)


@bp.route('/register', methods=('POST',))
def register():
    register_schema = RegisterSchema()
    try:
        request_json = request.get_json()
        register_schema.load(request_json)
    except ValidationError as err:
        return err.messages, 422
    username = request_json['username']
    password = request_json['password']
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    user = get_user_by_username(username)
    if user is not None:
        error = f"User {username} is already registered."
    if error is None:
        user = User(username=username, password_hash=generate_password_hash(password))
        user.save()
        return jsonify(user)

    result = {
        "error": error
    }
    return jsonify(result), 400


@bp.route('/login', methods=('POST',))
def login():
    register_schema = LoginSchema()
    try:
        request_json = request.get_json()
        register_schema.load(request_json)
    except ValidationError as err:
        return err.messages, 422
    username = request_json['username']
    password = request_json['password']

    error = None
    user = get_user_by_username(username)
    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user.password_hash, password):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = str(user['id'])
        return jsonify(user)
    session.clear()
    result = {
        "error": error
    }
    return jsonify(result), 400


@bp.route("/logout", methods=("POST",))
@require_session
def logout():
    session.clear()
    return jsonify({"message": "Successfully logged out"})
