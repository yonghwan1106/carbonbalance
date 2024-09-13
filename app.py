import streamlit as st

# 페이지 설정을 스크립트 최상단에 배치
st.set_page_config(page_title="Carbon neutrality Korea", page_icon="🌿", layout="wide")

from supabase import create_client, Client
import hashlib
from pathlib import Path
from pages import home, basic_info, carbon_calculator, carbon_map, visualization, credit_manager, marketplace, profile, eco_game
import importlib
import uuid
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supabase 클라이언트 초기화
@st.cache_resource
def init_connection() -> Client:
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

# 전역 변수로 Supabase 클라이언트 설정
supabase = init_connection()

# 페이지 모듈 동적 임포트 함수
def import_page(page_name):
    try:
        st.write(f"페이지 로드 시도: {page_name}")
        module = importlib.import_module(f"pages.{page_name}")
        if hasattr(module, 'show'):
            st.write(f"'{page_name}' 페이지 로드 성공")
            return module.show
        else:
            st.error(f"'{page_name}' 페이지에 'show' 함수가 정의되어 있지 않습니다.")
            return None
    except ImportError as e:
        st.error(f"'{page_name}' 페이지 모듈을 찾을 수 없습니다. 오류: {str(e)}")
        return None
    except Exception as e:
        st.error(f"'{page_name}' 페이지 로드 중 예상치 못한 오류 발생: {str(e)}")
        return None

# 세션 상태 초기화 함수
def init_session_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None

# 비밀번호 해싱
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 사용자 등록
def register_user(username, password):
    hashed_password = hash_password(password)
    try:
        response = supabase.table('users').insert({"username": username, "password": hashed_password}).execute()
        if response.data:
            return True
        else:
            st.error("회원가입 실패: 응답에 데이터가 없습니다.")
            return False
    except Exception as e:
        st.error(f"회원가입 중 오류 발생: {str(e)}")
        if '23505' in str(e):  # 고유 제약 조건 위반 오류 코드
            st.error("이미 존재하는 사용자명입니다.")
        elif '42501' in str(e):  # 권한 부족 오류 코드
            st.error("데이터베이스 권한 오류. 관리자에게 문의하세요.")
        return False
        
# 사용자 인증
def authenticate_user(username, password):
    hashed_password = hash_password(password)
    response = supabase.table('users').select("id").eq("username", username).eq("password", hashed_password).execute()
    return response.data[0]['id'] if response.data else None

# 세션 생성
def create_session(user_id, username):
    session_id = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=1)
    logger.info(f"Attempting to create session for user {username}")
    try:
        response = supabase.table('sessions').insert({
            "session_id": session_id,
            "user_id": user_id,
            "username": username,
            "expires_at": expires_at.isoformat()
        }).execute()
        
        logger.info(f"Session creation response: {response}")
        
        if response.data:
            return session_id
        else:
            logger.error("Session creation failed: No data in response")
            return None
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        if hasattr(e, 'json'):
            error_details = e.json()
            logger.error(f"Detailed error: {error_details}")
        return None

# 세션 확인
def get_session(session_id):
    response = supabase.table('sessions').select("*").eq("session_id", session_id).gte("expires_at", datetime.now().isoformat()).execute()
    return response.data[0] if response.data else None

# 세션 삭제
def delete_session(session_id):
    supabase.table('sessions').delete().eq("session_id", session_id).execute()



# 메인 앱
def main():

    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        show_main_app()
    else:
        show_login_page()

def show_login_page():
    st.title("🌿 Carbon neutrality Korea에 오신 것을 환영합니다")
    
    tab1, tab2 = st.tabs(["로그인", "회원가입"])
    
    with tab1:
        username = st.text_input("사용자명")
        password = st.text_input("비밀번호", type="password")
        if st.button("로그인"):
            user_id = authenticate_user(username, password)
            if user_id:
                session_id = create_session(user_id, username)
                st.session_state.user = {
                    'id': user_id,
                    'username': username,
                    'session_id': session_id
                }
                st.success("로그인 성공!")
                st.rerun()
            else:
                st.error("잘못된 사용자명 또는 비밀번호입니다.")
    
    with tab2:
        new_username = st.text_input("새 사용자명")
        new_password = st.text_input("새 비밀번호", type="password")
        if st.button("회원가입"):
            if register_user(new_username, new_password):
                st.success("회원가입 성공! 이제 로그인할 수 있습니다.")
            else:
                st.error("회원가입 실패. 이미 존재하는 사용자명일 수 있습니다.")

def show_main_app():
    st.sidebar.write("디버그 정보:")
    st.sidebar.write(f"사용자 데이터: {st.session_state.user}")

    # 사이드바에 메뉴 추가
    menu = st.sidebar.selectbox(
        "메뉴를 선택하세요",
        ["home", "basic_info", "carbon_calculator", "carbon_map", "visualization", 
         "credit_manager", "marketplace", "profile", "eco_game"]
    )
    
    # 메뉴에 따른 페이지 표시 
    #  try:
       #   page_func = import_page(menu)
         # if page_func:
     #         page_func()
       #   else:
         #     st.error(f"'{menu}' 페이지를 로드할 수 없습니다.")
     # except Exception as e:
      #    st.error(f"페이지 로드 중 오류 발생: {str(e)}")

    # 기본 페이지 (홈) 표시
    if menu == "home":
        st.title("🌿 Carbon neutrality Korea")
        st.write("탄소중립 코리아에 오신 것을 환영합니다!")
        # 여기에 홈 페이지 내용을 추가하세요

    # 세션 상태를 통한 데이터 공유 예시
    st.sidebar.write(f"현재 로그인: {st.session_state.user['username']}")

    if st.sidebar.button("로그아웃"):
        delete_session(st.session_state.user['session_id'])
        st.session_state.user = None
        st.rerun()

if __name__ == "__main__":
    main()
