import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from config import SECRET_KEY
from models.user import User
from utils.db_manager import get_db_session


def authenticate_user(username, password):
    session = get_db_session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and check_password_hash(user.password_hash, password):
        return user
    else:
        # 인증 실패 시 로그인 페이지 표시
        show_login_page()
        return None

def create_token(user_id):
    expiration = datetime.utcnow() + timedelta(hours=24)
    payload = {'user_id': user_id, 'exp': expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        return user_id
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        # 토큰 검증 실패 시 로그인 페이지 표시
        show_login_page()
        return None

def is_user_authenticated(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        session = get_db_session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        if user:
            return user
        else:
            # 사용자 인증 실패 시 로그인 페이지 표시
            show_login_page()
            return None
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        # 토큰 검증 실패 시 로그인 페이지 표시
        show_login_page()
        return None

def login_user(username, password):
    session = get_db_session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and check_password_hash(user.password_hash, password):
        token = create_token(user.id)
        return user, token
    else:
        # 로그인 실패 시 로그인 페이지 표시
        show_login_page()
        return None, None

def logout_user(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        # 로그아웃 처리 구현
        return True
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        # 토큰 검증 실패 시 로그인 페이지 표시
        show_login_page()
        return False
