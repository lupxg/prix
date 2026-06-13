from functools import wraps
from flask import request
from http import HTTPStatus
from app.api.auth.utils import verify_token
from app.api.auth.model import User

def token_required(f):
    """JWT authentication decorator
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = True
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[0]
        if not token:
            return {'message': 'Token is missing'}, HTTPStatus.BAD_REQUEST

        try:
            payload = verify_token(token)
            if payload['type'] != 'access':
                return {'message': 'Invalid token type'}, HTTPStatus.BAD_REQUEST
            current_user = User.query.get(payload['sub'])
            if not current_user:
                return {'message': 'Invalid user'}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'messaage': str(e)}, HTTPStatus.BAD_REQUEST
        
        return f(current_user, *args, **kwargs)
    
    
    return decorated