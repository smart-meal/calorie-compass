import os
from flask import (
    Blueprint, request, session, jsonify
)
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from api.user.model import User
from api.user.schema import RegisterSchema, LoginSchema, UpdatePasswordSchema
from api.user.service import get_user_by_username, get_user_by_id
from api.util.auth import require_session

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
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    user = get_user_by_username(username)
    if user is not None:
        error = f"User {username} is already registered."
    if error is None:
        salt = os.urandom(16).hex()
        password_salt_combined = password + salt
        user = User(username=username, 
            password_hash=generate_password_hash(password_salt_combined),
            salt=salt)
        user.save()
        return jsonify(user)

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
        error = 'Incorrect username.'
    else:
        salt = user.salt
        password_salt_combined = password + salt
        if not check_password_hash(user.password_hash, password_salt_combined):
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


@user_blueprint.route("/logout", methods=("POST",))
@require_session
def logout():
    session.clear()
    return jsonify({"message": "Successfully logged out"})

@user_blueprint.route("/delete", methods=("POST",))
@require_session
def delete_account():
    error = None
    if 'user_id' not in session:
        error = "Not logged in"
        return jsonify({"error": error}), 400

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    if not user:
        error = "User id:{} not found".format(user_id)
        return jsonify({"error": error}), 400
    
    user.delete()
    if error is None:
        session.pop('user_id', None)
        return jsonify({"message": "Successfully deleted"})

    result = {
        "error": error
    }
    return jsonify(result), 400

@user_blueprint.route("/update_password", methods=("POST",))
@require_session
def update_password():
    update_schema = UpdatePasswordSchema()
    try:
        request_json = request.get_json()
        update_schema.load(request_json)
    except ValidationError as err:
        return err.messages, 422

    old_password = request_json['old_password']
    new_password = request_json['new_password']
    repeat_password = request_json['repeat_password']
    error = None

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
    return jsonify(user)
