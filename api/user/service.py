from typing import Optional

from api.user.model import User
from api.util.log import logger


def get_user_by_username(username: str) -> Optional[User]:
    """
    Return the user model by its username
    If no user found, return None
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
