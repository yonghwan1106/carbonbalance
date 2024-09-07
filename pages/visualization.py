
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io 

def clean_numeric(x):
    if isinstance(x, str):
        return float(x.replace(',', '').replace('-', '0'))
    return float(x)

@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "gyeonggi_carbon_data_2022.csv")
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='cp949')
    
    numeric_columns = ['배출_건물_전기', '배출_건물_지역난방', '배출_건물_가스', '탄소배출_수송', '탄소흡수_산림']
    
    for col in numeric_columns:
        df[col] = df[col].apply(clean_numeric)
    
    df['총배출량'] = df[numeric_columns[:4]].sum(axis=1)
    df['순배출량'] = df['총배출량'] - df['탄소흡수_산림']
    
    return df

def plot_carbon_neutrality_progress(df):
    """
    각 지자체의 탄소 배출량과 흡수량을 비교하여 탄소 중립 달성 정도를 시각화합니다.
    """
    df['탄소중립달성도'] = (df['탄소흡수_산림'] / df['총배출량'] * 100).clip(upper=100)
    df = df.sort_values('탄소중립달성도', ascending=False)

    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['지자체명'],
        y=df['총배출량'],
        name='탄소 배출량',
        marker_color='red'
    ))
    
    fig.add_trace(go.Bar(
        x=df['지자체명'],
        y=df['탄소흡수_산림'],
        name='탄소 흡수량',
        marker_color='green'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['지자체명'],
        y=df['탄소중립달성도'],
        name='탄소 중립 달성도 (%)',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='경기도 지자체별 탄소 중립 달성 현황',
        xaxis_title='지자체',
        yaxis_title='탄소량 (천톤 CO2eq)',
        yaxis2=dict(
            title='탄소 중립 달성도 (%)',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        barmode='group',
        legend=dict(x=1.1, y=1),
        height=600
    )
    
    return fig

def plot_top_carbon_neutral_cities(df, top_n=5):
    """
    탄소 중립 달성도가 가장 높은 상위 N개 도시를 시각화합니다.
    """
    df['탄소중립달성도'] = (df['탄소흡수_산림'] / df['총배출량'] * 100).clip(upper=100)
    df = df.sort_values('탄소중립달성도', ascending=False).head(top_n)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['지자체명'],
        y=df['총배출량'],
        name='탄소 배출량',
        marker_color='red'
    ))
    
    fig.add_trace(go.Bar(
        x=df['지자체명'],
        y=df['탄소흡수_산림'],
        name='탄소 흡수량',
        marker_color='green'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['지자체명'],
        y=df['탄소중립달성도'],
        name='탄소 중립 달성도 (%)',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color='blue', width=2),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f'탄소 중립 달성도 상위 {top_n}개 지자체',
        xaxis_title='지자체',
        yaxis_title='탄소량 (천톤 CO2eq)',
        yaxis2=dict(
            title='탄소 중립 달성도 (%)',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
        barmode='group',
        legend=dict(x=1.1, y=1),
        height=500
    )
    
    return fig

def show():
    st.title("경기도 지자체별 탄소 배출 및 흡수량 분석 (2022년)")

    df = load_data()

    # 데이터 개요
    st.subheader("데이터 개요")
    st.write(df.describe())

    # 데이터 타입 및 결측값 확인
    st.subheader("데이터 정보")
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
    
    st.subheader("결측값 확인")
    st.write(df.isnull().sum())

    # 상위 5개 행 표시
    st.subheader("데이터 미리보기")
    st.write(df.head())

    # 지자체 선택 옵션
    selected_municipalities = st.multiselect(
        "비교할 지자체를 선택하세요", 
        options=df['지자체명'].unique(),
        default=df['지자체명'].unique()[:5]  # 기본적으로 상위 5개 지자체 선택
    )

    filtered_df = df[df['지자체명'].isin(selected_municipalities)]

    # 총 배출량 비교 막대 차트
    st.subheader("지자체별 총 탄소 배출량 비교")
    fig_total = px.bar(filtered_df, x="지자체명", y="총배출량", 
                       title="지자체별 총 탄소 배출량",
                       color="총배출량",
                       color_continuous_scale=px.colors.sequential.Viridis)
    fig_total.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_total)

    # 배출 원인별 비교 막대 차트
    st.subheader("지자체별 탄소 배출 원인 비교")
    fig_sources = px.bar(filtered_df, x="지자체명", 
                         y=["배출_건물_전기", "배출_건물_지역난방", "배출_건물_가스", "탄소배출_수송"],
                         title="지자체별 탄소 배출 원인 비교",
                         barmode="stack")
    fig_sources.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_sources)

    # 순 배출량 (배출량 - 흡수량) 비교
    st.subheader("지자체별 순 탄소 배출량 비교")
    fig_net = px.bar(filtered_df, x="지자체명", y="순배출량", 
                     title="지자체별 순 탄소 배출량 (총 배출량 - 흡수량)",
                     color="순배출량",
                     color_continuous_scale=px.colors.diverging.RdYlGn_r)
    fig_net.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_net)

    # 산점도: 총 배출량 vs 흡수량
    st.subheader("총 탄소 배출량 vs 흡수량 관계")
    fig_scatter = px.scatter(filtered_df, x="총배출량", y="탄소흡수_산림", 
                             size="순배출량", color="지자체명",
                             hover_name="지자체명", log_x=True, log_y=True,
                             title="총 탄소 배출량 vs 흡수량 (로그 스케일)")
    st.plotly_chart(fig_scatter)

    # 상위 5개 지자체와 하위 5개 지자체 비교
    st.subheader("순 탄소 배출량 상위 5개 및 하위 5개 지자체")
    top_5 = df.nlargest(5, '순배출량')
    bottom_5 = df.nsmallest(5, '순배출량')
    comparison_df = pd.concat([top_5, bottom_5])

    fig_comparison = go.Figure(data=[
        go.Bar(name='배출량', x=comparison_df['지자체명'], y=comparison_df['총배출량']),
        go.Bar(name='흡수량', x=comparison_df['지자체명'], y=comparison_df['탄소흡수_산림'])
    ])
    fig_comparison.update_layout(barmode='group', title="순 탄소 배출량 상위 5개 및 하위 5개 지자체 비교")
    fig_comparison.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_comparison)

    # 새로운 시각화: 탄소 중립 달성 정도
    st.subheader("경기도 지자체별 탄소 중립 달성 현황")
    fig_neutrality = plot_carbon_neutrality_progress(df)
    st.plotly_chart(fig_neutrality)

    # 새로운 시각화: 상위 탄소 중립 도시
    st.subheader("탄소 중립 달성도 상위 지자체")
    top_n = st.slider("표시할 상위 지자체 수를 선택하세요", min_value=3, max_value=10, value=5)
    fig_top_neutral = plot_top_carbon_neutral_cities(df, top_n)
    st.plotly_chart(fig_top_neutral)

    # 결론 및 인사이트
    st.subheader("결론 및 인사이트")
    st.write("""
    - 대부분의 지자체에서 건물 전기 사용으로 인한 탄소 배출이 가장 큰 비중을 차지하고 있습니다.
    - 일부 지자체는 수송으로 인한 탄소 배출이 상대적으로 높습니다. 이는 해당 지역의 교통 특성을 반영합니다.
    - 산림을 통한 탄소 흡수량은 지자체별로 큰 차이를 보입니다. 일부 지역은 높은 흡수량으로 순 배출량을 크게 줄이고 있습니다.
    - 순 배출량을 기준으로 볼 때, 산림 면적이 넓은 지자체들이 상대적으로 유리한 위치에 있습니다.
    - 탄소 중립 달성도를 보면, 일부 지자체는 이미 높은 수준의 탄소 중립을 달성하고 있으나, 대부분의 지자체는 아직 갈 길이 멀어 보입니다.
    - 탄소 중립을 위해서는 배출량 감소와 흡수량 증가를 동시에 고려한 정책이 필요해 보입니다.
    """)

    # 데이터 출처 및 주의사항
    st.info("데이터 출처: 경기도 환경정책과, 2022년 기준")
    st.warning("본 데이터는 2022년 기준으로, 최신 상황과 다를 수 있습니다.")

if __name__ == "__main__":
    show()
