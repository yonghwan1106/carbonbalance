import streamlit as st
import sqlite3
import hashlib
from pathlib import Path
from pages import home, basic_info, carbon_calculator, carbon_map, visualization, credit_manager, marketplace, profile, eco_game
import importlib
from streamlit_cookies_manager import CookieManager

# 페이지 모듈 동적 임포트 함수
def import_page(page_name):
    try:
        # 디버그 정보 출력
        st.write(f"Trying to import: pages.{page_name}")
        
        module = importlib.import_module(f"pages.{page_name}")
        
        # 성공적으로 임포트된 경우
        st.write(f"Successfully imported: pages.{page_name}")
        
        if hasattr(module, 'show'):
            return module.show
        else:
            st.error(f"'{page_name}' 페이지에 'show' 함수가 정의되어 있지 않습니다.")
            return None
    except ImportError as e:
        st.error(f"'{page_name}' 페이지 모듈을 찾을 수 없습니다. 오류: {str(e)}")
        return None

# 세션 상태 초기화 함수
def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect('carbon_neutral.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
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
    st.set_page_config(page_title="탄소중립 코리아", page_icon="🌿", layout="wide")
    
    cookie_manager = CookieManager()
    
    if not cookie_manager.ready():
        st.stop()

    # 쿠키에서 로그인 정보 확인
    if 'logged_in' not in st.session_state and cookie_manager.get('logged_in'):
        st.session_state.logged_in = True
        st.session_state.user_data = json.loads(cookie_manager.get('user_data'))
        
    init_session_state()

    # 디버그 정보 출력
    st.sidebar.write("Session State:", st.session_state)

    # 사이드바에 로그인/로그아웃 버튼
    if st.session_state.get('logged_in', False):
        if st.sidebar.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.user_data = {}
            st.rerun()
    
    # 로그인 상태에 따른 화면 표시
    if not st.session_state.get('logged_in', False):
        show_login_page()
    else:
        show_main_app()

def show_login_page():
    st.title("🌿 탄소중립 코리아에 오신 것을 환영합니다")
    
    tab1, tab2 = st.tabs(["로그인", "회원가입"])
    
    with tab1:
        username = st.text_input("사용자명")
        password = st.text_input("비밀번호", type="password")
        if st.button("로그인"):
            st.write("로그인 시도 중...")  # 디버그 정보
            user_id = authenticate_user(username, password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_data = {
                    'user_id': user_id,
                    'username': username
                }
                st.success("로그인 성공!")
                st.write("로그인 후 세션 상태:", st.session_state)  # 디버그 정보
                time.sleep(2)  # 사용자가 메시지를 볼 수 있도록 잠시 대기
                st.rerun()
            else:
                st.error("잘못된 사용자명 또는 비밀번호입니다.")
                st.write("로그인 실패 후 세션 상태:", st.session_state)  # 디버그 정보
    
    with tab2:
        new_username = st.text_input("새 사용자명")
        new_password = st.text_input("새 비밀번호", type="password")
        if st.button("회원가입"):
            if register_user(new_username, new_password):
                st.success("회원가입 성공! 이제 로그인할 수 있습니다.")
            else:
                st.error("이미 존재하는 사용자명입니다.")

def show_main_app():
    st.title("🌿 탄소중립 코리아")
    
    # 사이드바에 메뉴 추가
    menu = st.sidebar.selectbox(
        "메뉴를 선택하세요",
        ["home", "basic_info", "carbon_calculator", "carbon_map", "visualization", 
         "credit_manager", "marketplace", "profile", "eco_game"]
    )
    
    # 메뉴에 따른 페이지 표시 
    page_func = import_page(menu)
    if page_func:
        page_func()

    # 세션 상태를 통한 데이터 공유 예시
    st.sidebar.write(f"현재 로그인: {st.session_state.user_data.get('username', '알 수 없음')}")

if __name__ == "__main__":
    init_db()
    main()