import streamlit as st
import sys
import os
from utils.db_manager import init_db
from utils.auth_manager import is_user_authenticated, login_user, logout_user
from pages import home, basic_info, carbon_calculator, carbon_map, visualization, policy_suggestions, eco_game, marketplace, profile, carbon_credit

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    st.set_page_config(page_title="Carbon Footprint Korea", page_icon="🍃", layout="wide")
    
    # 데이터베이스 초기화
    init_db()

    # 사용자 인증 상태 확인
    if not is_user_authenticated():
        show_login_page()
    else:
        show_main_application()

def show_login_page():
    st.title("🔐 로그인")
    username = st.text_input("사용자명")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if login_user(username, password):
            st.success("로그인 성공!")
            st.experimental_rerun()
        else:
            st.error("잘못된 사용자명 또는 비밀번호입니다.")

def show_main_application():
    menu = ["Home", "Basic Info", "My Carbon Footprint", "Carbon Map", "Data Visualization", 
            "Carbon Credits", "Marketplace", "Profile", "Policy Suggestions", "Eco Game"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        home.show()
    elif choice == "Basic Info":
        basic_info.show_basic_info()
    elif choice == "My Carbon Footprint":
        carbon_calculator.show()
    elif choice == "Carbon Map":
        carbon_map.show_carbon_map()
    elif choice == "Data Visualization":
        visualization.show()
    elif choice == "Carbon Credits":
        carbon_credit.show()
    elif choice == "Marketplace":
        marketplace.show()
    elif choice == "Profile":
        profile.show()
    elif choice == "Policy Suggestions":
        policy_suggestions.show()
    elif choice == "Eco Game":
        eco_game.show()

    if st.sidebar.button("로그아웃"):
        logout_user()
        st.experimental_rerun()

if __name__ == "__main__":
    main()
