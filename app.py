
import streamlit as st
from carbonbalance/pages import visualization, carbon_calculator, policy_suggestions, eco_game

st.set_page_config(page_title="CarbonBalance Gyeonggi", page_icon="🌱", layout="wide")

def main():
    st.title("CarbonBalance Gyeonggi")
    
    menu = ["Home", "Visualization", "Carbon Calculator", "Policy Suggestions", "Eco Game"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.write("Welcome to CarbonBalance Gyeonggi!")
        st.write("This app helps you understand and manage carbon emissions in Gyeonggi Province.")
    elif choice == "Visualization":
        visualization.show()
    elif choice == "Carbon Calculator":
        carbon_calculator.show()
    elif choice == "Policy Suggestions":
        policy_suggestions.show()
    elif choice == "Eco Game":
        eco_game.show()

if __name__ == "__main__":
    main()
