import json
from app.config import redis_client
from flask import request, g
from .model import User
from functools import wraps
from http import HTTPStatus


def get_current_user():
    """ Gets the current user in the session
    """

    session_id = request.cookies.get("session_id")

    if not session_id:
        return None
    
    session_data = redis_client.get(f"session:{session_id}")

    if not session_data:
        return None
    
    session = json.loads(session_data)

    return User.query.get(session["user_id"])


def login_required(f):
    """ Wrapper function for protectes routes.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        user = get_current_user()

        if not user:
            return {"error": "Unauthorize"}, HTTPStatus.UNAUTHORIZED
        
        g.user = user

        return f(*args, **kwargs)
    
    return wrapper