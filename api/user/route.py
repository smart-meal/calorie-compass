import os

from flask import (
    Blueprint, request, session, jsonify
)
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from api.user.model import User
from api.user.schema import validate_with_schema, RegisterSchema, LoginSchema, UpdatePasswordSchema
from api.user.service import get_user_by_username, get_user_by_id
from api.util.auth import require_session, get_user_id_from_session
from api.util.log import logger

user_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@user_blueprint.route('/register', methods=('POST',))
@validate_with_schema(RegisterSchema)
def register(validated_data):
    username = validated_data['username']
    password = validated_data['password']
    logger.info("Registering '%s'", username)

    error = None

    user = get_user_by_username(username)
    if user is not None:
        error = f"User {username} is already registered."
    if error is None:
        salt = os.urandom(16).hex()
        password_salt_combined = password + salt
        user = User(
            username=username,
            password_hash=generate_password_hash(password_salt_combined),
            salt=salt)
        user.save()
        result = user.to_dict()
        return jsonify(result)

    result = {
        "error": error
    }
    return jsonify(result), 400


@user_blueprint.route('/login', methods=('POST',))
@validate_with_schema(LoginSchema)
def login(validated_data):
    username = validated_data['username']
    password = validated_data['password']

    error = None
    user = get_user_by_username(username)
    if user is None:
        logger.info("Incorrect username '%s'", username)
        error = 'Incorrect username.'
    else:
        salt = user.salt
        password_salt_combined = password + salt
        if not check_password_hash(user.password_hash, password_salt_combined):
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

@user_blueprint.route("/delete", methods=("POST",))
@require_session
def delete_account():
    user_id = get_user_id_from_session()
    user = get_user_by_id(user_id)

    if not user:
        error = f"UserId {user_id} not found."
        return jsonify({"error": error}), 400

    user.delete()

    session.clear()
    return jsonify({"message": "Successfully deleted"})

@user_blueprint.route("/update_password", methods=("POST",))
@require_session
@validate_with_schema(UpdatePasswordSchema)
def update_password(validated_data):

    old_password = validated_data['old_password']
    new_password = validated_data['new_password']

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    salt = user.salt
    password_salt_combined = old_password + salt
    if not check_password_hash(user.password_hash, password_salt_combined):
        error = 'Incorrect password.'
        result = {
            "error": error
        }
        return jsonify(result), 400

    new_password_salt_combined = new_password + salt
    new_hash = generate_password_hash(new_password_salt_combined)
    user.password_hash = new_hash
    user.save()
    session.clear()
    session['user_id'] = str(user['id'])
    return jsonify(user.to_dict())
