from typing import Optional

from api.user.model import User
from api.util.log import logger


def get_user_by_username(username: str) -> Optional[User]:
    """
    Return the user model by its username
    If no user found, return None

    Args:
        username (str): The username

    Returns:
        Optional[User]: The User object if found; otherwise, None.
    """
    # pylint: disable=no-member
    users_result = User.objects(username=username)
    count = users_result.count()
    if count > 1:
        logger.error("%s users matched by username '%s'", count, username)
        raise RuntimeError("Something went wrong")
    if count == 0:
        return None
    return users_result.get()

def get_user_by_id(uid: str) -> Optional[User]:
    """
    Return the user model by its id
    If no user found, return None
    
    Args:
        uid (str): The unique identifier of the user to retrieve.

    Returns:
        Optional[User]: The User object if found; otherwise, None.
    """
    # pylint: disable=no-member
    users_result = User.objects(id=uid)
    print(users_result)
    count = users_result.count()
    if count > 1:
        logger.error("%s users matched by user id '%s'", count, uid)
        raise RuntimeError("Something went wrong")
    if count == 0:
        return None
    return users_result.get()

def calculate_bmi(height, weight):
    # Ensure that height is in meters
    height_in_meters = height / 100
    bmi = weight / (height_in_meters * height_in_meters)

    return bmi
