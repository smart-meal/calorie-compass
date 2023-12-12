import os
import json
from flask_cors import CORS, cross_origin
from flask import (
    Blueprint, session, jsonify, request
)
from werkzeug.security import check_password_hash, generate_password_hash
from marshmallow import ValidationError
from api.user.model import User, Meal
from api.user.schema import (
    validate_with_schema, RegisterSchema, LoginSchema, UserSchema, UpdatePasswordSchema,
    MealSchema,
)
from api.user.service import get_user_by_username, get_user_by_id, calculate_bmi, get_image_info
from api.util.auth import require_session, get_user_id_from_session
from api.util.log import logger

user_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@user_blueprint.route('/register', methods=('POST',))
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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

@user_blueprint.route('/profile', methods=('POST',))
@cross_origin(supports_credentials=True)
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
    user.user_profile.bmi = validated_data['bmi']
    user.save()

    return jsonify(user.user_profile), 201


@user_blueprint.route('/profile', methods=('GET',))
@cross_origin(supports_credentials=True)
@require_session
def get_profile():
    user = get_user_by_id(session['user_id'])
    if user is None:
        return jsonify({"error": "User not found."}), 404

    if not user.user_profile:
        return jsonify({"error": "Profile not found."}), 404

    return jsonify(user.user_profile), 200

@user_blueprint.route("/logout", methods=("POST",))
@cross_origin(supports_credentials=True)
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


@user_blueprint.route('/add_meal', methods=('POST',))
@cross_origin(supports_credentials=True)
@require_session
def add_meal():
    meal_schema = MealSchema()
    request_json = request.get_json()
    meal_info = json.loads(get_image_info(request_json.get("image_url")))
    combined_meal = {**request_json, **meal_info}
    keys_to_convert = ['weight', 'calories', 'fat', 'proteins', 'carbs']
    for key in keys_to_convert:
        combined_meal[key] = float(combined_meal[key])
    try:
        meal_data = meal_schema.load(combined_meal)
    except ValidationError as err:
        return err.messages, 422

    user_id = session['user_id']
    user = get_user_by_id(user_id)

    if not user:
        error = f"User with ID {user_id} not found."
        return jsonify({"error": error}), 400
    meal = Meal(user=user, **meal_data)
    meal.save()

    result = meal.to_dict()
    return jsonify(result)

@user_blueprint.route('/get_meals', methods=('GET',))
@cross_origin(supports_credentials=True)
@require_session
def get_meals():
    user_id = session['user_id']
    user = get_user_by_id(user_id)

    if not user:
        error = f"User with ID {user_id} not found."
        return jsonify({"error": error}), 400

    # pylint: disable=no-member
    meals = Meal.objects(user=user).order_by('-meal_date')
    meal_list = [meal.to_dict() for meal in meals]

    return jsonify(meal_list)


@user_blueprint.route("/update_password", methods=("POST",))
@cross_origin(supports_credentials=True)
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
