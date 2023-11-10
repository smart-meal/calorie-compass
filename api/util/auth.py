from typing import Callable

from flask import session, jsonify


def get_user_id_from_session():
    if 'user_id' in session:
        return session['user_id']
    raise RuntimeError("No session")


def require_session(func: Callable):
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            # Session data is valid, continue with the request
            return func(*args, **kwargs)
        else:
            # Session data is not valid, redirect to a login page or perform another action
            return jsonify({"error": "Unauthorized"}), 401

    return wrapper
