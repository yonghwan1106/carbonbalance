import streamlit as st
import sys
import os
from pages import visualization, carbon_calculator, policy_suggestions, eco_game, carbon_map

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="탄소중립 경기도!", page_icon="🌱", layout="wide")

def main():
    st.title("🌱 CarbonBalance Gyeonggi")
    
    menu = ["Home", "Visualization", "Carbon Map", "Carbon Calculator", "Policy Suggestions", "Eco Game"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.write("이 앱은 경기도에서 당신의 탄소 배출을 관리하고 이해하도록 돕는 사이트입니다.")
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
