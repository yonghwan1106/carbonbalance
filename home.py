import streamlit as st
import pandas as pd
from utils.data_processor import get_latest_national_data
from utils.ai_helper import get_daily_eco_tip

def show():
    st.title("🍃 Carbon Footprint Korea")
    
    # 환영 메시지
    st.write("""
    환영합니다! Carbon Footprint Korea는 당신의 탄소 발자국을 이해하고 줄이는 데 도움을 주는 플랫폼입니다.
    함께 더 나은 미래를 만들어 갑시다.
    """)
    
    # 주요 기능 소개
    st.header("주요 기능")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🧮 탄소 발자국 계산")
        st.write("개인의 일상 활동에 따른 탄소 발자국을 계산해보세요.")
        if st.button("계산하기"):
            st.switch_page("pages/carbon_calculator.py")
    
    with col2:
        st.subheader("🗺️ 전국 탄소 지도")
        st.write("대한민국 전체의 탄소 배출 현황을 한눈에 확인하세요.")
        if st.button("지도 보기"):
            st.switch_page("pages/carbon_map.py")
    
    with col3:
        st.subheader("💰 탄소 크레딧 거래")
        st.write("여러분의 노력을 크레딧으로 보상받고 거래해보세요.")
        if st.button("마켓플레이스"):
            st.switch_page("pages/marketplace.py")
    
    # 최신 국가 데이터
    st.header("🇰🇷 대한민국 최신 탄소 배출 현황")
    national_data = get_latest_national_data()
    st.metric(label="총 탄소 배출량", value=f"{national_data['total_emissions']:,} 톤 CO2e",
              delta=f"{national_data['emissions_change']}% 전년 대비")
    
    # 일일 에코 팁
    st.header("🌱 오늘의 에코 팁")
    daily_tip = get_daily_eco_tip()
    st.info(daily_tip)
    
    # 최신 뉴스 또는 업데이트
    st.header("📰 최신 소식")
    news_items = [
        "정부, 2050 탄소중립 로드맵 발표",
        "서울시, 도시 전체 태양광 패널 설치 계획 추진",
        "기업들의 ESG 경영 확대로 탄소 배출 감소 추세"
    ]
    for item in news_items:
        st.write(f"• {item}")
    
    # 사용자 참여 유도
    st.header("함께 만들어가는 녹색 미래")
    st.write("여러분의 작은 실천이 큰 변화를 만듭니다. 지금 시작해보세요!")
    if st.button("도전 과제 참여하기"):
        st.switch_page("pages/challenges.py")

if __name__ == "__main__":
    show()
