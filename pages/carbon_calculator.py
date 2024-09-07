import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ai_helper import get_emission_reduction_tips


def calculate_carbon_footprint(transportation, energy_usage, food_habits, consumer_goods):
    # 이 함수는 실제 계산 로직으로 대체되어야 합니다.
    # 현재는 간단한 예시 계산만 수행합니다.
    footprint = (
        transportation * 0.5 +
        energy_usage * 0.3 +
        food_habits * 0.15 +
        consumer_goods * 0.05
    )
    return footprint

def show():
    st.title("개인 탄소 발자국 계산기")

    st.write("일상생활에서의 탄소 발자국을 계산해보세요.")

    # 사용자 입력 받기
    transportation = st.slider("교통 (주간 자동차 사용 km)", 0, 1000, 100)
    energy_usage = st.slider("에너지 사용 (월간 전기 사용량 kWh)", 0, 1000, 300)
    food_habits = st.slider("식습관 (주간 육류 소비 횟수)", 0, 21, 7)
    consumer_goods = st.slider("소비재 (월간 새 물건 구매 횟수)", 0, 50, 10)

    if st.button("탄소 발자국 계산하기"):
        # 탄소 발자국 계산
        footprint = calculate_carbon_footprint(transportation, energy_usage, food_habits, consumer_goods)

        st.subheader(f"당신의 연간 탄소 발자국: {footprint:.2f} 톤 CO2e")

        # 지역 평균과 비교 (예시 데이터, 실제 데이터로 대체 필요)
        region_average = 5.0  # 톤 CO2e
        comparison = (footprint - region_average) / region_average * 100

        if comparison > 0:
            st.write(f"당신의 탄소 발자국은 지역 평균보다 {comparison:.1f}% 높습니다.")
        else:
            st.write(f"당신의 탄소 발자국은 지역 평균보다 {-comparison:.1f}% 낮습니다.")

        # 비교 시각화
        fig = px.bar(x=['Your Footprint', 'Region Average'], y=[footprint, region_average],
                     labels={'x': '', 'y': 'Carbon Footprint (tons CO2e)'},
                     title='Your Carbon Footprint vs Region Average')
        st.plotly_chart(fig)

        # AI를 이용한 맞춤형 팁 제공
        tips = get_emission_reduction_tips(footprint, transportation, energy_usage, food_habits, consumer_goods)
        st.subheader("탄소 배출 감소를 위한 맞춤형 팁:")
        for tip in tips:
            st.write(f"- {tip}")

        # 추가 정보 제공
        st.info("이 계산은 대략적인 추정치입니다. 정확한 탄소 발자국 계산을 위해서는 더 자세한 생활 습관 분석이 필요합니다.")

if __name__ == "__main__":
    show()
