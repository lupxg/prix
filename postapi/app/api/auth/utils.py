import jwt
from datetime import datetime, timedelta, timezone
from jwt import ExpiredSignatureError, InvalidTokenError
from ...config import jwt_token_expires, jwt_refresh_token_expires, SECRET_KEY

encoded_key = SECRET_KEY.encode('utf-8')

def generate_token(user_id, token_type='access'):
    """Generate JWT token"""

    now = datetime.now(tz=timezone.utc)
    if token_type == 'access':
        expires_in = jwt_token_expires
    else:
        expires_in = jwt_refresh_token_expires

    payload = {
        'sub': str(user_id),
        'iat': int(now.timestamp()),
        'exp': int((now + timedelta(seconds=expires_in)).timestamp()),
        'type': token_type
    }

    return jwt.encode(payload, encoded_key, algorithm='HS256')


def verify_token(token):
    """Verify token"""
    try:
        payload = jwt.decode(token, encoded_key, algorithms=['HS256'])
        return payload
    except ExpiredSignatureError: 
        raise Exception('Token expired')
    except InvalidTokenError as e:
        raise Exception(f'Invalid token: {str(e)}')
