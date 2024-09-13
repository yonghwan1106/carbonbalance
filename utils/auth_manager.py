# 🔐 Auth Manager
# This file manages user authentication using Supabase

from supabase import create_client, Client
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from config import SECRET_KEY, SUPABASE_URL, SUPABASE_KEY

# Supabase 클라이언트 초기화
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def authenticate_user(username, password):
    response = supabase.table('users').select('*').eq('username', username).execute()
    if response.data:
        user = response.data[0]
        if check_password_hash(user['password_hash'], password):
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
        user_id = payload['user_id']
        return user_id
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def is_user_authenticated(token):
    user_id = verify_token(token)
    if user_id:
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        if response.data:
            return response.data[0]
    return None

def login_user(username, password):
    user = authenticate_user(username, password)
    if user:
        token = create_token(user['id'])
        return user, token
    return None, None

def logout_user(token):
    # Supabase에서는 서버 측 세션을 관리하지 않으므로,
    # 클라이언트 측에서 토큰을 삭제하는 것으로 충분합니다.
    return True