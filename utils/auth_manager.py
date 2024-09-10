import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from config import SECRET_KEY
from models.user import User
from utils.db_manager import get_db_session

def create_user(username, password, email):
    session = get_db_session()
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password, email=email)
    session.add(new_user)
    session.commit()
    session.close()

def authenticate_user(username, password):
    session = get_db_session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None

def create_token(user_id):
    expiration = datetime.utcnow() + timedelta(hours=24)
    payload = {'user_id': user_id, 'exp': expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
