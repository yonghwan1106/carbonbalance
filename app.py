import streamlit as st
import sqlite3
import hashlib
from pathlib import Path
from pages import home, basic_info, carbon_calculator, carbon_map, visualization, credit_manager, marketplace, profile, eco_game
import importlib
import uuid
from datetime import datetime, timedelta
from streamlit_cookies_manager import CookieManager

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
    try:
        if 'cookie_manager' not in st.session_state:
            st.session_state.cookie_manager = CookieManager()
        
        if not st.session_state.cookie_manager.ready():
            st.stop()
    except Exception as e:
        st.error(f"쿠키 관리자 초기화 중 오류 발생: {str(e)}")
        st.session_state.cookie_manager = None

    if 'session_id' not in st.session_state:
        # URL 쿼리 파라미터에서 세션 ID 확인
        query_params = st.experimental_get_query_params()
        session_id = query_params.get('session_id', [None])[0]
        st.session_state.session_id = session_id

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('carbon_neutral.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (session_id TEXT PRIMARY KEY, user_id INTEGER, username TEXT, expires_at DATETIME)''')
    conn.commit()
    conn.close()

# 비밀번호 해싱
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 사용자 등록
def register_user(username, password):
    conn = sqlite3.connect('carbon_neutral.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# 사용자 인증
def authenticate_user(username, password):
    conn = sqlite3.connect('carbon_neutral.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed_password))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

# 세션 생성
def create_session(user_id, username):
    session_id = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=1)
    conn = sqlite3.connect('carbon_neutral.db')
    c = conn.cursor()
    c.execute("INSERT INTO sessions (session_id, user_id, username, expires_at) VALUES (?, ?, ?, ?)",
              (session_id, user_id, username, expires_at))
    conn.commit()
    conn.close()
    
    # 쿠키에 세션 ID 저장
    if st.session_state.cookie_manager:
        st.session_state.cookie_manager.set('session_id', session_id)
    
    # URL에 세션 ID 추가
    st.experimental_set_query_params(session_id=session_id)
    
    return session_id

# 세션 확인
def get_session(session_id):
    conn = sqlite3.connect('carbon_neutral.db')
    c = conn.cursor()
    c.execute("SELECT * FROM sessions WHERE session_id = ? AND expires_at > ?", (session_id, datetime.now()))
    session = c.fetchone()
    conn.close()
    return session

# 세션 삭제
def delete_session(session_id):
    conn = sqlite3.connect('carbon_neutral.db')
    c = conn.cursor()
    c.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

def check_database():
    conn = sqlite3.connect('carbon_neutral.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    if c.fetchone():
        st.success("users 테이블이 존재합니다.")
        c.execute("SELECT COUNT(*) FROM users")
        count = c.fetchone()[0]
        st.write(f"현재 users 테이블에 {count}개의 레코드가 있습니다.")
    else:
        st.error("users 테이블이 존재하지 않습니다.")
    conn.close()

# 메인 앱
def main():
    st.set_page_config(page_title="Carbon neutrality Korea", page_icon="🌿", layout="wide")
    
    init_db()
    init_session_state()

    if st.session_state.session_id:
        session = get_session(st.session_state.session_id)
        if session:
            st.session_state.logged_in = True
            st.session_state.user_data = {'user_id': session[1], 'username': session[2]}
            # 세션이 유효한 경우 쿠키 갱신
            if st.session_state.cookie_manager:
                st.session_state.cookie_manager.set('session_id', st.session_state.session_id)
            show_main_app()
        else:
            # 세션이 유효하지 않은 경우 초기화
            st.session_state.session_id = None
            st.session_state.logged_in = False
            st.session_state.user_data = {}
            if st.session_state.cookie_manager:
                st.session_state.cookie_manager.delete('session_id')
            show_login_page()
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
                st.session_state.session_id = session_id
                st.session_state.logged_in = True
                st.session_state.user_data = {
                    'user_id': user_id,
                    'username': username
                }
                # 쿠키에 세션 ID 저장
                if st.session_state.cookie_manager:
                    st.session_state.cookie_manager.set('session_id', session_id)
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
                st.error("이미 존재하는 사용자명입니다.")

def show_main_app():
    st.sidebar.write("디버그 정보:")
    st.sidebar.write(f"세션 ID: {st.session_state.session_id}")
    st.sidebar.write(f"로그인 상태: {st.session_state.logged_in}")
    st.sidebar.write(f"사용자 데이터: {st.session_state.user_data}")

    # 사이드바에 메뉴 추가
    menu = st.sidebar.selectbox(
        "메뉴를 선택하세요",
        ["home", "basic_info", "carbon_calculator", "carbon_map", "visualization", 
         "credit_manager", "marketplace", "profile", "eco_game"]
    )
    
    # 메뉴에 따른 페이지 표시 
    try:
        page_func = import_page(menu)
        if page_func:
            page_func()
        else:
            st.error(f"'{menu}' 페이지를 로드할 수 없습니다.")
    except Exception as e:
        st.error(f"페이지 로드 중 오류 발생: {str(e)}")

    # 기본 페이지 (홈) 표시
    if menu == "home":
        st.title("🌿 Carbon neutrality Korea")
        st.write("탄소중립 코리아에 오신 것을 환영합니다!")
        # 여기에 홈 페이지 내용을 추가하세요

    # 세션 상태를 통한 데이터 공유 예시
    st.sidebar.write(f"현재 로그인: {st.session_state.user_data.get('username', '알 수 없음')}")

    if st.sidebar.button("로그아웃"):
        delete_session(st.session_state.session_id)
        st.session_state.cookie_manager.delete('session_id')
        st.session_state.session_id = None
        st.session_state.logged_in = False
        st.session_state.user_data = {}
        st.experimental_set_query_params()  # URL에서 세션 ID 제거
        st.rerun()

if __name__ == "__main__":
    main()