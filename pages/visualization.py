import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show():
    st.title("경기도 지자체별 탄소 배출량 분석 (2022년)")

    @st.cache_data
    def load_data():
        # 데이터 프레임 생성
        data = {
            '지자체': ['수원시 장안구', '수원시 권선구', '수원시 팔달구', '수원시 영통구', ...],  # 모든 지자체 이름
            '건물_전기': [6633735, 8509063, 5599474, 9428241, ...],  # 건물_전기_탄소배출량 데이터
            '지역난방': [460565, 305978, 173425, 1389085, ...],  # 지역난방_탄소배출량 데이터
            '수송': [491502, 880990, 334440, 745867, ...]  # 수송으로 인한 탄소배출량 데이터
        }
        df = pd.DataFrame(data)
        df['총배출량'] = df['건물_전기'] + df['지역난방'] + df['수송']
        return df

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

    # 총 배출량 비교 막대 차트
    st.subheader("지자체별 총 탄소 배출량 비교")
    fig_total = px.bar(filtered_df, x="지자체", y="총배출량", 
                       title="지자체별 총 탄소 배출량",
                       color="총배출량",
                       color_continuous_scale=px.colors.sequential.Viridis)
    fig_total.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_total)

    # 배출 원인별 비교 막대 차트
    st.subheader("지자체별 탄소 배출 원인 비교")
    fig_sources = px.bar(filtered_df, x="지자체", y=["건물_전기", "지역난방", "수송"],
                         title="지자체별 탄소 배출 원인 비교",
                         barmode="stack")
    fig_sources.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_sources)

    # 파이 차트: 전체 배출량 중 각 지자체의 비중
    st.subheader("전체 탄소 배출량 중 각 지자체의 비중")
    fig_pie = px.pie(filtered_df, values='총배출량', names='지자체',
                     title="지자체별 탄소 배출량 비중")
    st.plotly_chart(fig_pie)

    # 산점도: 건물_전기 vs 수송 배출량
    st.subheader("건물_전기 vs 수송 탄소 배출량 관계")
    fig_scatter = px.scatter(filtered_df, x="건물_전기", y="수송", 
                             size="총배출량", color="지자체",
                             hover_name="지자체", log_x=True, log_y=True,
                             title="건물_전기 vs 수송 탄소 배출량 (로그 스케일)")
    st.plotly_chart(fig_scatter)

    # 상위 5개 지자체와 하위 5개 지자체 비교
    st.subheader("총 탄소 배출량 상위 5개 및 하위 5개 지자체")
    top_5 = df.nlargest(5, '총배출량')
    bottom_5 = df.nsmallest(5, '총배출량')
    comparison_df = pd.concat([top_5, bottom_5])

    fig_comparison = go.Figure(data=[
        go.Bar(name='건물_전기', x=comparison_df['지자체'], y=comparison_df['건물_전기']),
        go.Bar(name='지역난방', x=comparison_df['지자체'], y=comparison_df['지역난방']),
        go.Bar(name='수송', x=comparison_df['지자체'], y=comparison_df['수송'])
    ])
    fig_comparison.update_layout(barmode='stack', title="탄소 배출량 상위 5개 및 하위 5개 지자체 비교")
    fig_comparison.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_comparison)

    # 결론 및 인사이트
    st.subheader("결론 및 인사이트")
    st.write("""
    - 대부분의 지자체에서 건물_전기로 인한 탄소 배출이 가장 큰 비중을 차지하고 있습니다.
    - 일부 지자체는 수송으로 인한 탄소 배출이 상대적으로 높습니다. 이는 해당 지역의 교통 특성을 반영합니다.
    - 지역난방으로 인한 탄소 배출은 지자체별로 큰 차이를 보입니다. 일부 지역은 지역난방 시설이 없거나 적은 것으로 보입니다.
    - 탄소 배출량 감축을 위해서는 각 지자체의 특성에 맞는 맞춤형 정책이 필요해 보입니다.
    - 특히 건물_전기 부문의 에너지 효율 개선과 친환경 교통 수단 도입이 중요할 것으로 판단됩니다.
    """)

    # 데이터 출처 및 주의사항
    st.info("데이터 출처: 경기도 환경정책과, 2022년 기준")
    st.warning("본 데이터는 2022년 기준으로, 최신 상황과 다를 수 있습니다.")

if __name__ == "__main__":
    show()
