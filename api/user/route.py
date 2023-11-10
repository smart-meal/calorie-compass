from flask import (
    Blueprint, request, session, jsonify
)
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from api.user.model import User
from api.user.schema import RegisterSchema, LoginSchema
from api.user.service import get_user_by_username
from api.util.auth import require_session, get_user_id_from_session
from api.util.log import logger

user_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@user_blueprint.route('/register', methods=('POST',))
def register():
    register_schema = RegisterSchema()
    try:
        request_json = request.get_json()
        validated_data = register_schema.load(request_json)
    except ValidationError as err:
        return err.messages, 422
    username = validated_data['username']
    password = validated_data['password']
    logger.info("Registering '%s'", username)

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
        result = user.to_dict()
        return jsonify(result)

    result = {
        "error": error
    }
    return jsonify(result), 400


@user_blueprint.route('/login', methods=('POST',))
def login():
    login_schema = LoginSchema()
    try:
        request_json = request.get_json()
        login_schema.load(request_json)
    except ValidationError as err:
        return err.messages, 422
    username = request_json['username']
    password = request_json['password']

    error = None
    user = get_user_by_username(username)
    if user is None:
        logger.info("Incorrect username '%s'", username)
        error = 'Incorrect username.'
    elif not check_password_hash(user.password_hash, password):
        logger.info("Incorrect password for '%s'", username)

        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = str(user['id'])
        logger.info("'%s' successfully logged in", get_user_id_from_session())

        result = user.to_dict()
        return jsonify(result)
    session.clear()
    result = {
        "error": error
    }
    return jsonify(result), 400


@user_blueprint.route("/logout", methods=("POST",))
@require_session
def logout():
    logger.info("Logging out '%s'", get_user_id_from_session())
    session.clear()
    return jsonify({"message": "Successfully logged out"})
