"""
This module defines routes for user authentication and management.
It includes endpoints for user registration, login, password update.
"""
import os

from flask import (
    Blueprint, request, session, jsonify
)
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

from api.user.model import User
from api.user.schema import RegisterSchema, LoginSchema, UpdatePasswordSchema
from api.user.service import get_user_by_username, get_user_by_id
from api.util.auth import require_session, get_user_id_from_session
from api.util.log import logger
from api import config

user_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@user_blueprint.route('/register', methods=('POST',))
def register():
    """
    Handle user registration.
    """
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
def login():
    """
    Handle user login.
    Validates the provided credentials and sets the user session if successful.
    Returns a JSON response with the user's data or an error message.
    """
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
    """
    Clears the current user session.
    """
    logger.info("Logging out '%s'", get_user_id_from_session())
    session.clear()
    return jsonify({"message": "Successfully logged out"})

@user_blueprint.route("/delete", methods=("POST",))
@require_session
def delete_account():
    """
    Deletes the user's account and clears the session.
    Require logged-in session.
    Returns a JSON response indicating successful deletion.
    """
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
def update_password():
    """
    Update password for a user.
    Require logged-in session.
    Returns a JSON response with the updated user's data or an error message.
    """
    update_schema = UpdatePasswordSchema()
    try:
        request_json = request.get_json()
        update_schema.load(request_json)
    except ValidationError as err:
        return err.messages, 422

    old_password = request_json['old_password']
    new_password = request_json['new_password']

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

from azure.storage.blob import BlobServiceClient, BlobClient

blob_service_client = BlobServiceClient.from_connection_string(config.AZURE_CONN)

@user_blueprint.route("/upload", methods=("POST",))
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        blob_client = blob_service_client.get_blob_client(container=config.AZURE_CONTAINER, blob=file.filename)
        blob_client.upload_blob(file)
        return jsonify({'message': 'File uploaded successfully', 'filename': file.filename})
