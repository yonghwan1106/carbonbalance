import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
import requests
import json

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_processor import load_gyeonggi_data, analyze_emissions_trend

# Groq API 설정
MODEL = "llama-3.1-70b-versatile"
URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def get_ai_policy_suggestions(region, emissions_data):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    지역: {region}
    총 탄소 배출량: {emissions_data['total_emissions']}
    배출 트렌드: {emissions_data['trend']}
    부문별 배출 비중: {emissions_data['sector_breakdown']}

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
    df = load_gyeonggi_data()

    # 지역 선택
    regions = df['지역'].unique()
    selected_region = st.selectbox("🏙️ 분석할 지역을 선택하세요", regions)

    if selected_region:
        # 선택된 지역의 데이터
        region_data = df[df['지역'] == selected_region]

        # 데이터 시각화
        st.subheader(f"📊 {selected_region} 탄소 배출 현황")
        fig = px.line(region_data, x='연도', y='탄소배출량', title=f"{selected_region} 연간 탄소 배출량 추이")
        st.plotly_chart(fig)

        # 부문별 배출량 비교
        sectors = ['가정', '상업', '산업', '수송', '공공', '기타']
        sector_data = region_data[sectors].iloc[-1]  # 최근 연도의 데이터
        fig_sector = px.pie(values=sector_data.values, names=sector_data.index, title=f"{selected_region} 부문별 탄소 배출 비중")
        st.plotly_chart(fig_sector)

        # 배출 트렌드 분석
        trend_analysis = analyze_emissions_trend(region_data)
        st.subheader("📈 배출 트렌드 분석")
        st.write(trend_analysis)

        # AI 기반 정책 제안 버튼
        if st.button("🤖 AI 정책 제안 생성"):
            with st.spinner("AI가 정책을 생성 중입니다..."):
                emissions_data = {
                    'total_emissions': region_data['탄소배출량'].iloc[-1],
                    'trend': trend_analysis,
                    'sector_breakdown': sector_data.to_dict()
                }
                policy_suggestions = get_ai_policy_suggestions(selected_region, emissions_data)
            
            st.subheader("💡 AI 기반 정책 제안")
            st.write(policy_suggestions)

        # 정책 효과 시뮬레이션 (간단한 예시)
        st.subheader("🔬 정책 효과 시뮬레이션")
        reduction_percentage = st.slider("예상 감축률 (%)", 0, 100, 10)
        current_emissions = region_data['탄소배출량'].iloc[-1]
        simulated_emissions = current_emissions * (1 - reduction_percentage / 100)

        fig_simulation = px.bar(x=['현재 배출량', '정책 적용 후 예상 배출량'], 
                                y=[current_emissions, simulated_emissions],
                                title="정책 적용 효과 시뮬레이션")
        st.plotly_chart(fig_simulation)

        st.write(f"현재 배출량 {current_emissions:.2f}에서 {simulated_emissions:.2f}로")
        st.write(f"{reduction_percentage}% 감소할 것으로 예상됩니다.")

if __name__ == "__main__":
    show()

