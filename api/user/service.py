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

def get_user_by_id(uid: str) -> Optional[User]:
    """
    Return the user model by its id
    If no user found, return None
    """
    # https://stackoverflow.com/questions/9988352/how-to-search-document-by-oid-in-mongoengine
    users_result = User.objects(pk=uid)
    count = users_result.count()
    if count > 1:
        # TODO log the number of results
        raise RuntimeError("Something went wrong")
    if count == 0:
        return None
    return users_result.get()