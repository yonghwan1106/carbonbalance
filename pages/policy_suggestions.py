import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests
import json

# Groq API 설정
MODEL = "llama-3.1-70b-versatile"
URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "gyeonggi_carbon_data_2022.csv")
    df = pd.read_csv(file_path)
    return df

def get_ai_policy_suggestions(region, emissions_data):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    지역: {region}
    총 탄소 배출량: {emissions_data['total_emissions']}
    배출 현황: {emissions_data['breakdown']}

    위 정보를 바탕으로 {region}의 탄소 배출량을 줄이기 위한 구체적인 정책을 제안해주세요. 
    각 정책은 지역 특성을 고려하고, 실행 가능해야 합니다. 정책의 수에는 제한이 없으며, 
    가능한 한 상세하고 다양한 정책을 제안해주세요.
    """

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return "API 요청 중 오류가 발생했습니다."

def show():
    st.title("🌿 지역 맞춤형 친환경 정책 제안 플랫폼")

    # 데이터 로드
    df = load_data()

    # 지역 선택
    regions = df['지자체명'].unique()
    selected_region = st.selectbox("🏙️ 분석할 지역을 선택하세요", regions)

    if selected_region:
        # 선택된 지역의 데이터
        region_data = df[df['지자체명'] == selected_region].iloc[0]

        # 데이터 시각화
        st.subheader(f"📊 {selected_region} 탄소 배출 현황")
        
        # 배출원별 데이터 준비
        emission_sources = ['배출_건물_전기', '배출_건물_지역난방', '배출_건물_가스', '탄소배출_수송']
        emission_values = region_data[emission_sources]
        
        fig = px.pie(values=emission_values, names=emission_sources, title=f"{selected_region} 부문별 탄소 배출 비중")
        st.plotly_chart(fig)

        # 총 배출량 및 흡수량 계산
        total_emissions = emission_values.sum()
        absorption = region_data['탄소흡수_산림']
        net_emissions = total_emissions - absorption

        st.write(f"총 배출량: {total_emissions:,.0f} tCO2eq")
        st.write(f"탄소 흡수량: {absorption:,.0f} tCO2eq")
        st.write(f"순 배출량: {net_emissions:,.0f} tCO2eq")

        # AI 기반 정책 제안 버튼
        if st.button("🤖 AI 정책 제안 생성"):
            with st.spinner("AI가 정책을 생성 중입니다..."):
                emissions_data = {
                    'total_emissions': total_emissions,
                    'breakdown': region_data[emission_sources + ['탄소흡수_산림']].to_dict()
                }
                policy_suggestions = get_ai_policy_suggestions(selected_region, emissions_data)
            
            st.subheader("💡 AI 기반 정책 제안")
            st.write(policy_suggestions)

        # 정책 효과 시뮬레이션
        st.subheader("🔬 정책 효과 시뮬레이션")
        reduction_percentage = st.slider("예상 감축률 (%)", 0, 100, 10)
        simulated_emissions = net_emissions * (1 - reduction_percentage / 100)

        fig_simulation = px.bar(x=['현재 순배출량', '정책 적용 후 예상 순배출량'], 
                                y=[net_emissions, simulated_emissions],
                                title="정책 적용 효과 시뮬레이션")
        st.plotly_chart(fig_simulation)

        st.write(f"현재 순배출량 {net_emissions:,.0f} tCO2eq에서 {simulated_emissions:,.0f} tCO2eq로")
        st.write(f"{reduction_percentage}% 감소할 것으로 예상됩니다.")

if __name__ == "__main__":
    show()
