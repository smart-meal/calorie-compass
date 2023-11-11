from typing import Callable

from flask import session, jsonify
from functools import wraps


def require_session(func: Callable):
    @wraps(func) # avoid "View function mapping is overwriting an existing endpoint function"
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            # Session data is valid, continue with the request
            return func(*args, **kwargs)
        else:
            # Session data is not valid, redirect to a login page or perform another action
            return jsonify({"error": "Unauthorized"}), 401

    return wrapper

