import jwt
from datetime import datetime, timedelta

def create_token(user_id, secret_key):
    expiration = datetime.utcnow() + timedelta(hours=24)
    payload = {'user_id': user_id, 'exp': expiration}
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def verify_token(token, secret_key):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
