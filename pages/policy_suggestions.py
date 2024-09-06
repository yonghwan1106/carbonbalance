import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ai_helper import get_policy_suggestions
from utils.data_processor import load_gyeonggi_data, analyze_emissions_trend

def show():
    st.title("지역 맞춤형 친환경 정책 제안 플랫폼")

    # 데이터 로드
    df = load_gyeonggi_data()

    # 지역 선택
    regions = df['지역'].unique()
    selected_region = st.selectbox("분석할 지역을 선택하세요", regions)

    if selected_region:
        # 선택된 지역의 데이터
        region_data = df[df['지역'] == selected_region]

        # 데이터 시각화
        st.subheader(f"{selected_region} 탄소 배출 현황")
        fig = px.line(region_data, x='연도', y='탄소배출량', title=f"{selected_region} 연간 탄소 배출량 추이")
        st.plotly_chart(fig)

        # 부문별 배출량 비교
        sectors = ['가정', '상업', '산업', '수송', '공공', '기타']
        sector_data = region_data[sectors].iloc[-1]  # 최근 연도의 데이터
        fig_sector = px.pie(values=sector_data.values, names=sector_data.index, title=f"{selected_region} 부문별 탄소 배출 비중")
        st.plotly_chart(fig_sector)

        # 배출 트렌드 분석
        trend_analysis = analyze_emissions_trend(region_data)
        st.subheader("배출 트렌드 분석")
        st.write(trend_analysis)

        # AI 기반 정책 제안
        st.subheader("AI 기반 정책 제안")
        emissions_data = {
            'total_emissions': region_data['탄소배출량'].iloc[-1],
            'trend': trend_analysis,
            'sector_breakdown': sector_data.to_dict()
        }
        policy_suggestions = get_policy_suggestions(selected_region, emissions_data)

        for i, suggestion in enumerate(policy_suggestions, 1):
            st.write(f"{i}. {suggestion}")

        # 정책 효과 시뮬레이션 (간단한 예시)
        st.subheader("정책 효과 시뮬레이션")
        selected_policy = st.selectbox("시뮬레이션할 정책을 선택하세요", policy_suggestions)
        reduction_percentage = st.slider("예상 감축률 (%)", 0, 100, 10)

        current_emissions = region_data['탄소배출량'].iloc[-1]
        simulated_emissions = current_emissions * (1 - reduction_percentage / 100)

        fig_simulation = px.bar(x=['현재 배출량', '정책 적용 후 예상 배출량'], 
                                y=[current_emissions, simulated_emissions],
                                title="정책 적용 효과 시뮬레이션")
        st.plotly_chart(fig_simulation)

        st.write(f"선택한 정책 '{selected_policy}'를 적용하면 ")
        st.write(f"현재 배출량 {current_emissions:.2f}에서 {simulated_emissions:.2f}로")
        st.write(f"{reduction_percentage}% 감소할 것으로 예상됩니다.")

if __name__ == "__main__":
    show()
