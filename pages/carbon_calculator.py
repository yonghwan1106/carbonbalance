import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
from datetime import datetime
import requests

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Groq API 설정
MODEL = "llama-3.1-70b-versatile"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# 탄소 발자국 계산 함수 개선
def calculate_carbon_footprint(transportation, energy_usage, food_habits, consumer_goods, waste):
    # 교통 (주간 자동차 사용 km)
    transport_footprint = (transportation * 52 * 0.12) / 1000  # 연간으로 환산, kg CO2/km, 톤 단위로 변환

    # 에너지 사용 (월간 전기 사용량 kWh, 4인 가구 기준)
    energy_footprint = (energy_usage * 12 * 0.4) / 1000  # 연간으로 환산, kg CO2/kWh, 톤 단위로 변환

    # 식습관 (주간 육류 소비 횟수)
    food_footprint = (food_habits * 52 * 3.3) / 1000  # 연간으로 환산, kg CO2e/식사, 톤 단위로 변환

    # 소비재 (월간 새 물건 구매 횟수)
    consumer_goods_footprint = (consumer_goods * 12 * 10) / 1000  # 연간으로 환산, kg CO2e/구매, 톤 단위로 변환

    # 폐기물 (주간 재활용하지 않는 쓰레기 kg)
    waste_footprint = (waste * 52 * 0.5) / 1000  # 연간으로 환산, kg CO2e/kg 쓰레기, 톤 단위로 변환
    
    total_footprint = (
        transport_footprint +
        energy_footprint +
        food_footprint +
        consumer_goods_footprint +
        waste_footprint
    )
    
    return total_footprint, {
        "교통": transport_footprint,
        "에너지": energy_footprint,
        "식습관": food_footprint,
        "소비재": consumer_goods_footprint,
        "폐기물": waste_footprint
    }

# AI를 이용한 맞춤형 팁 제공 함수
def get_emission_reduction_tips(footprint, transportation, energy_usage, food_habits, consumer_goods, waste):
    prompt = f"""
    개인의 탄소 발자국 정보:
    - 총 탄소 발자국: {footprint:.2f} 톤 CO2e
    - 교통: {transportation} km/주 (자동차 사용)
    - 에너지 사용: {energy_usage} kWh/월 (4인 가구 기준)
    - 식습관: 주 {food_habits}회 육류 소비
    - 소비재: 월 {consumer_goods}회 새 물건 구매
    - 폐기물: 주 {waste}kg 재활용하지 않는 쓰레기

    위 정보를 바탕으로, 이 개인이 탄소 발자국을 줄이기 위해 실천할 수 있는 구체적이고 실용적인 팁 5가지를 제공해주세요. 
    각 팁은 간결하고 실행 가능해야 하며, 개인의 현재 상황을 고려해야 합니다.
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].split("\n")
    else:
        return ["AI 팁을 가져오는 데 문제가 발생했습니다. 나중에 다시 시도해주세요."]

# 사용자 데이터 저장 및 불러오기 함수
def save_user_data(data):
    if 'user_data' not in st.session_state:
        st.session_state.user_data = []
    st.session_state.user_data.append(data)

def load_user_data():
    return st.session_state.get('user_data', [])

def show():
    st.title("🌍 개인 탄소 발자국 계산기")

    st.write("일상생활에서의 탄소 발자국을 자세히 계산하고 추적해보세요.")

    # 탭 생성
    tabs = st.tabs(["🧮 계산기", "📊 히스토리", "📈 통계"])

    with tabs[0]:  # 계산기 탭
        # 사용자 입력 받기 (기존 항목 + 새로운 항목)
        transportation = st.slider("🚗 교통 (주간 자동차 사용 km)", 0, 1000, 100, help="평균: 주 250km")
        energy_usage = st.slider("💡 에너지 사용 (월간 전기 사용량 kWh, 4인 가구 기준)", 0, 1000, 300, help="4인 가구 평균: 월 350kWh")
        food_habits = st.slider("🍖 식습관 (주간 육류 소비 횟수)", 0, 21, 7, help="평균: 주 9회")
        consumer_goods = st.slider("🛍️ 소비재 (월간 새 물건 구매 횟수)", 0, 50, 10, help="평균: 월 15회")
        waste = st.slider("🗑️ 폐기물 (주간 재활용하지 않는 쓰레기 kg)", 0, 50, 5, help="평균: 주 7kg")

        if st.button("탄소 발자국 계산하기"):
            # 탄소 발자국 계산
            footprint, footprint_breakdown = calculate_carbon_footprint(
                transportation, energy_usage, food_habits, consumer_goods, waste
            )

            st.subheader(f"당신의 연간 탄소 발자국: {footprint:.2f} 톤 CO2e")

            # 지역 평균과 비교 (예시 데이터, 실제 데이터로 대체 필요)
            region_average = 5.0  # 톤 CO2e
            comparison = (footprint - region_average) / region_average * 100

            if comparison > 0:
                st.write(f"당신의 탄소 발자국은 지역 평균보다 {comparison:.1f}% 높습니다.")
            else:
                st.write(f"당신의 탄소 발자국은 지역 평균보다 {abs(comparison):.1f}% 낮습니다.")

            # 각 항목별 탄소발자국 발생량 표시
            st.subheader("🏷️ 항목별 탄소발자국 발생량:")
            for category, amount in footprint_breakdown.items():
                st.write(f"{category}: {amount:.2f} 톤 CO2e")

            # 탄소 발자국 내역 시각화
            fig = px.pie(
                values=list(footprint_breakdown.values()),
                names=list(footprint_breakdown.keys()),
                title='탄소 발자국 내역'
            )
            st.plotly_chart(fig)

            # 비교 시각화
            fig = px.bar(x=['Your Footprint', 'Region Average'], y=[footprint, region_average],
                         labels={'x': '', 'y': 'Carbon Footprint (tons CO2e)'},
                         title='당신의 탄소발자국 vs 지역 평균')
            st.plotly_chart(fig)

            # AI 맞춤형 팁 제공
            st.subheader("💡 AI의 탄소 배출 감소를 위한 맞춤형 팁:")
            with st.spinner("AI가 맞춤형 팁을 생성하고 있습니다..."):
                tips = get_emission_reduction_tips(footprint, transportation, energy_usage, food_habits, consumer_goods, waste)
            for tip in tips:
                st.write(f"- {tip}")
                
            # 추가 정보 제공
            st.info("이 팁들은 AI에 의해 생성되었으며, 귀하의 개인 상황에 맞춰 제안되었습니다. 실행 가능성을 고려하여 적용해 보세요.")

            # 결과 저장
            save_user_data({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "footprint": footprint,
                "breakdown": footprint_breakdown,
                "transportation": transportation,
                "energy_usage": energy_usage,
                "food_habits": food_habits,
                "consumer_goods": consumer_goods,
                "waste": waste
            })

            # 계산 방법 설명
            st.subheader("ℹ️ 계산 방법 설명")
            st.write("""
            각 항목별 CO2e 환산 계산 방법:
            - 🚗 교통: (주간 km * 52주 * 0.12 kg CO2/km) / 1000 = 연간 톤 CO2e
            - 💡 에너지: (월간 kWh * 12개월 * 0.4 kg CO2/kWh) / 1000 = 연간 톤 CO2e
            - 🍖 식습관: (주간 육류 소비 횟수 * 52주 * 3.3 kg CO2e/식사) / 1000 = 연간 톤 CO2e
            - 🛍️ 소비재: (월간 구매 횟수 * 12개월 * 10 kg CO2e/구매) / 1000 = 연간 톤 CO2e
            - 🗑️ 폐기물: (주간 kg * 52주 * 0.5 kg CO2e/kg) / 1000 = 연간 톤 CO2e
            
            이 계산 방법은 일반적인 추정치를 사용한 것으로, 실제 상황에 따라 다를 수 있습니다.
            더 정확한 계산을 위해서는 지역별, 상황별 특성을 고려한 세부적인 데이터가 필요합니다.
            """)

    with tabs[1]:  # 히스토리 탭
        st.subheader("📊 탄소 발자국 히스토리")
        user_data = load_user_data()
        if user_data:
            df = pd.DataFrame(user_data)
            fig = px.line(df, x="date", y="footprint", title="탄소 발자국 변화 추이")
            st.plotly_chart(fig)

            # 항목별 추이 그래프
            categories = ["transportation", "energy_usage", "food_habits", "consumer_goods", "waste"]
            fig = go.Figure()
            for category in categories:
                fig.add_trace(go.Scatter(x=df["date"], y=df[category], mode='lines+markers', name=category))
            fig.update_layout(title="항목별 사용량 추이", xaxis_title="날짜", yaxis_title="사용량")
            st.plotly_chart(fig)

            # 데이터 테이블 표시
            st.subheader("상세 데이터")
            st.dataframe(df)
        else:
            st.write("아직 저장된 데이터가 없습니다.")

    with tabs[2]:  # 통계 탭
        st.subheader("📈 탄소 발자국 통계")
        user_data = load_user_data()
        if user_data:
            df = pd.DataFrame(user_data)
            avg_footprint = df['footprint'].mean()
            max_footprint = df['footprint'].max()
            min_footprint = df['footprint'].min()

            st.write(f"평균 탄소 발자국: {avg_footprint:.2f} 톤 CO2e")
            st.write(f"최대 탄소 발자국: {max_footprint:.2f} 톤 CO2e")
            st.write(f"최소 탄소 발자국: {min_footprint:.2f} 톤 CO2e")

            # 탄소 발자국 분포 히스토그램
            fig = px.histogram(df, x="footprint", nbins=20, title="탄소 발자국 분포")
            st.plotly_chart(fig)

            # 항목별 평균 기여도
            avg_breakdown = df[["transportation", "energy_usage", "food_habits", "consumer_goods", "waste"]].mean()
            fig = px.pie(values=avg_breakdown.values, names=avg_breakdown.index, title="항목별 평균 기여도")
            st.plotly_chart(fig)

            # 상관관계 히트맵
            corr_matrix = df[["footprint", "transportation", "energy_usage", "food_habits", "consumer_goods", "waste"]].corr()
            fig = px.imshow(corr_matrix, title="항목간 상관관계")
            st.plotly_chart(fig)
        else:
            st.write("아직 저장된 데이터가 없습니다.")

if __name__ == "__main__":
    show()