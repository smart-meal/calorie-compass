"""
This module defines routes for user authentication and management.
It includes endpoints for user registration, login, password update.
"""
import os
import string
import random

from flask import (
    Blueprint, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from api.user.model import User, UserProfile
from api.user.schema import validate_with_schema, RegisterSchema, LoginSchema, UserSchema, UpdatePasswordSchema
from api.user.service import get_user_by_username, get_user_by_id, calculate_bmi
from api.util.auth import require_session, get_user_id_from_session
from api.util.log import logger
from api import config

user_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@user_blueprint.route('/register', methods=('POST',))
@validate_with_schema(RegisterSchema)
def register(validated_data):
    """
    Handle user registration.
    """
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
    """
    Handle user login.
    Validates the provided credentials and sets the user session if successful.
    Returns a JSON response with the user's data or an error message.
    """
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

@user_blueprint.route('/profile', methods=('POST',))
@require_session
def create_profile():
    user_id = session.get('user_id')
    logger.info("User ID from session: %s", user_id)

    user = get_user_by_id(user_id)
    if user is None:
        logger.error("User not found for ID: %s", user_id)
        return jsonify({"error": "User not found."}), 404

    profile_schema = UserSchema()
    try:
        request_json = request.get_json()
        validated_data = profile_schema.load(request_json)
    except ValidationError as err:
        logger.error("Validation error: %s", err.messages)
        return err.messages, 422

    height = validated_data.get('height')
    weight = validated_data.get('weight')
    if height and weight:
        bmi = calculate_bmi(height, weight)
        validated_data['bmi'] = bmi
    
    user.user_profile.first_name = validated_data['first_name']
    user.user_profile.last_name = validated_data['last_name']
    user.user_profile.age = validated_data['age']
    user.user_profile.height = validated_data['height']
    user.user_profile.weight = validated_data['weight']
    user.user_profile.goal = validated_data['goal']
    user.user_profile.lifestyle = validated_data['lifestyle']
    user.user_profile.allergies = validated_data['allergies']
    user.save()

    return jsonify(user.user_profile), 201


@user_blueprint.route('/profile', methods=('GET',))
@require_session
def get_profile():
    user = get_user_by_id(session['user_id'])
    if user is None:
        return jsonify({"error": "User not found."}), 404

    if not user.user_profile:
        return jsonify({"error": "Profile not found."}), 404

    return jsonify(user.user_profile), 200

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
@validate_with_schema(UpdatePasswordSchema)
def update_password(validated_data):
    """
    Update password for a user.
    Require logged-in session.
    Returns a JSON response with the updated user's data or an error message.
    """

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

from azure.storage.blob import BlobServiceClient, BlobClient
blob_service_client = BlobServiceClient.from_connection_string(config.AZURE_CONN)

@user_blueprint.route("/upload", methods=("POST",))
def upload():
    """
    upload a photo to azure blob storage. 
    """
    def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    fileextension = filename.rsplit('.',1)[1]
    randomfilename = id_generator()
    filename = randomfilename + '.' + fileextension
    try:

        container = config.AZURE_CONTAINER
        account = config.AZURE_ACCOUNT
        blob_client = blob_service_client.get_blob_client(container=config.AZURE_CONTAINER, blob=filename)

        blob_client.upload_blob(file)
        url =  'http://'+ account + '.blob.core.windows.net/' + container + '/' + container + '/' + filename
        return jsonify({
            'message': 'File uploaded successfully', 
            'filename': file.filename,
            'url': url})

    except Exception as e:
        print(e)
        pass
