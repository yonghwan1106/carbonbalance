import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show():
    st.title("경기도 탄소 중립 진행 상황 시각화")
    
    @st.cache_data
    def load_data():
        return pd.read_csv("c_emi_b_electricity_gg_2022.csv")
    
    df = load_data()
    
    # 데이터 개요
    st.subheader("데이터 개요")
    st.write(df.describe())
    
    # 지자체 선택 옵션
    selected_municipalities = st.multiselect(
        "비교할 지자체를 선택하세요", 
        options=df['지자체'].unique(),
        default=df['지자체'].unique()[:5]  # 기본적으로 상위 5개 지자체 선택
    )
    
    filtered_df = df[df['지자체'].isin(selected_municipalities)]
    
    # 배출량과 흡수량 비교 바 차트
    st.subheader("지자체별 탄소 배출량 및 흡수량 비교")
    fig = px.bar(filtered_df, x="지자체", y=["탄소배출량", "탄소흡수량"], 
                 title="지자체별 탄소 배출량 및 흡수량",
                 barmode="group")
    st.plotly_chart(fig)
    
    # 탄소 중립 달성도 계산 및 시각화
    filtered_df['탄소중립달성도'] = (filtered_df['탄소흡수량'] / filtered_df['탄소배출량']) * 100
    
    st.subheader("지자체별 탄소 중립 달성도")
    fig_neutrality = px.bar(filtered_df, x="지자체", y="탄소중립달성도",
                            title="지자체별 탄소 중립 달성도 (%)",
                            color="탄소중립달성도",
                            color_continuous_scale=px.colors.sequential.Viridis)
    fig_neutrality.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
    st.plotly_chart(fig_neutrality)
    
    # 파이 차트: 전체 배출량 중 각 지자체의 비중
    st.subheader("전체 탄소 배출량 중 각 지자체의 비중")
    fig_pie = px.pie(filtered_df, values='탄소배출량', names='지자체',
                     title="지자체별 탄소 배출량 비중")
    st.plotly_chart(fig_pie)
    
    # 산점도: 배출량 vs 흡수량
    st.subheader("탄소 배출량 vs 흡수량 관계")
    fig_scatter = px.scatter(filtered_df, x="탄소배출량", y="탄소흡수량", 
                             size="탄소배출량", color="지자체",
                             hover_name="지자체", log_x=True, log_y=True,
                             title="탄소 배출량 vs 흡수량 (로그 스케일)")
    st.plotly_chart(fig_scatter)
    
    # 상위 5개 지자체와 하위 5개 지자체 비교
    st.subheader("탄소 배출량 상위 5개 및 하위 5개 지자체")
    top_5 = df.nlargest(5, '탄소배출량')
    bottom_5 = df.nsmallest(5, '탄소배출량')
    comparison_df = pd.concat([top_5, bottom_5])
    
    fig_comparison = go.Figure(data=[
        go.Bar(name='탄소배출량', x=comparison_df['지자체'], y=comparison_df['탄소배출량']),
        go.Bar(name='탄소흡수량', x=comparison_df['지자체'], y=comparison_df['탄소흡수량'])
    ])
    fig_comparison.update_layout(barmode='group', title="탄소 배출량 상위 5개 및 하위 5개 지자체 비교")
    st.plotly_chart(fig_comparison)
    
    # 결론 및 인사이트
    st.subheader("결론 및 인사이트")
    st.write("""
    - 대부분의 지자체에서 탄소 배출량이 흡수량을 크게 상회하고 있습니다.
    - 탄소 중립 달성을 위해서는 배출량 감소와 흡수량 증가를 위한 노력이 동시에 필요합니다.
    - 배출량이 높은 지자체들은 특히 산업 구조 개선과 친환경 정책 도입이 시급해 보입니다.
    - 흡수량이 상대적으로 높은 지자체의 사례를 벤치마킹할 필요가 있습니다.
    """)
    
    # 데이터 출처 및 주의사항
    st.info("데이터 출처: 경기도 환경정책과, 2022년 기준")
    st.warning("본 데이터는 2022년 기준으로, 최신 상황과 다를 수 있습니다.")

if __name__ == "__main__":
    show()
