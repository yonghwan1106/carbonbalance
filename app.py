import streamlit as st
import sys
import os
import streamlit as st
from pages import home, basic_info, carbon_calculator, carbon_map, visualization, policy_suggestions, eco_game, marketplace, profile, carbon_credit
# 아직 개발 중 carbon_credit,  community, challenges, education_hub
from utils.db_manager import init_db
from pages import marketplace
    
    # 데이터베이스 초기화
    init_db()
    
# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    st.set_page_config(page_title="Carbon Footprint Korea", page_icon="🍃", layout="wide")
    
    menu = ["Home", "Basic Info", "My Carbon Footprint", "Carbon Map", "Data Visualization", 
            "Carbon Credits", "Marketplace", "Profile", "Community", "Challenges", 
            "Education Hub", "Policy Suggestions", "Eco Game"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        home.show()
    elif choice == "Basic Info":
        basic_info.show_basic_info()
    elif choice == "Visualization":
        visualization.show()
    elif choice == "Carbon Map":
        carbon_map.show_carbon_map()
    elif choice == "Carbon Calculator":
        carbon_calculator.show()
    elif choice == "Policy Suggestions":
        policy_suggestions.show()
    elif choice == "Eco Game":
        eco_game.show()

if __name__ == "__main__":
    main()
