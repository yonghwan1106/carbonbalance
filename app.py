import streamlit as st
import sqlite3
import hashlib
from pathlib import Path
from pages import home, basic_info, carbon_calculator, carbon_map, visualization, credit_manager, marketplace, profile, eco_game

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
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    result = c.fetchone()
    conn.close()
    return result is not None

# 메인 앱
def main():
    st.set_page_config(page_title="탄소중립 코리아", page_icon="🌿", layout="wide")
    
    # 세션 상태 초기화
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # 사이드바에 로그인/로그아웃 버튼
    if st.session_state.logged_in:
        if st.sidebar.button("로그아웃"):
            st.session_state.logged_in = False
            st.experimental_rerun()
    
    # 로그인 상태에 따른 화면 표시
    if not st.session_state.logged_in:
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
            if authenticate_user(username, password):
                st.session_state.logged_in = True
                st.success("로그인 성공!")
                st.experimental_rerun()
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
    st.title("🌿 탄소중립 코리아")
    
    # 사이드바에 메뉴 추가
    menu = st.sidebar.selectbox(
        "메뉴를 선택하세요",
        ["홈", "기본 정보", "탄소 계산기", "탄소 지도", "데이터 시각화", 
         "탄소 크레딧", "마켓플레이스", "프로필", "에코 게임"]
    )
    
    # 선택된 메뉴에 따라 해당 페이지 표시
    if menu == "홈":
        home.show()
    elif menu == "기본 정보":
        basic_info.show()
    elif menu == "탄소 계산기":
        carbon_calculator.show()
    elif menu == "탄소 지도":
        carbon_map.show()
    elif menu == "데이터 시각화":
        visualization.show()
    elif menu == "탄소 크레딧":
        credit_manager.show()
    elif menu == "마켓플레이스":
        marketplace.show()
    elif menu == "프로필":
        profile.show()
    elif menu == "에코 게임":
        eco_game.show()

if __name__ == "__main__":
    init_db()
    main()