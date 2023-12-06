from flask import (
    Blueprint, request
)
from api.util.log import logger

user_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@user_blueprint.route('/calCalorie', method=('POST',))
def calCalories():
    request_json = request.get_json()
    image_url = request_json['image_url']
    logger.info("Image URL " + image_url + " received for calculating calories.")
    # Call function to calculate the calorie of the meal using image.
