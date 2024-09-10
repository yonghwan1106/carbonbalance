import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io 
import requests

# Groq API 설정
MODEL = "llama-3.1-70b-versatile"
API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

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

def get_ai_insights(df):
    prompt = f"""
    다음은 경기도 지자체별 탄소 배출 및 흡수량 데이터의 주요 통계입니다:

    총배출량 평균: {df['총배출량'].mean():.2f}
    총배출량 최대: {df['총배출량'].max():.2f} (지자체: {df.loc[df['총배출량'].idxmax(), '지자체명']})
    총배출량 최소: {df['총배출량'].min():.2f} (지자체: {df.loc[df['총배출량'].idxmin(), '지자체명']})
    
    탄소흡수량 평균: {df['탄소흡수_산림'].mean():.2f}
    탄소흡수량 최대: {df['탄소흡수_산림'].max():.2f} (지자체: {df.loc[df['탄소흡수_산림'].idxmax(), '지자체명']})
    탄소흡수량 최소: {df['탄소흡수_산림'].min():.2f} (지자체: {df.loc[df['탄소흡수_산림'].idxmin(), '지자체명']})

    이 데이터를 바탕으로 경기도의 탄소 배출 및 흡수 현황에 대한 주요 인사이트와 결론을 5개의 항목으로 제시해주세요. 
    각 인사이트는 데이터에 기반한 구체적인 내용이어야 하며, 정책적 제안이나 개선 방향도 포함해 주세요.
    """

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 2000
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].split("\n")
    else:
        return ["AI 인사이트를 가져오는 데 문제가 발생했습니다. 나중에 다시 시도해주세요."]
    
def show():
    st.title("🌍 경기도 지자체별 탄소 배출 및 흡수량 분석 (2022년)")

    df = load_data()

    # 데이터 개요
     # st.subheader("📊 데이터 개요")
     # st.write(df.describe())

    # 데이터 타입 및 결측값 확인
     # st.subheader("ℹ️ 데이터 정보")
     # buffer = io.StringIO()
     # df.info(buf=buffer)
     # s = buffer.getvalue()
     # st.text(s)
    
     # st.subheader("🔍 결측값 확인")
     # st.write(df.isnull().sum())

    # 상위 5개 행 표시
     # st.subheader("👀 데이터 미리보기")
     # st.write(df.head())

    # 지자체 선택 옵션
    selected_municipalities = st.multiselect(
        "비교할 지자체를 선택하세요", 
        options=df['지자체명'].unique(),
        default=df['지자체명'].unique()[:10]  # 기본적으로 상위 10개 지자체 선택
    )

    filtered_df = df[df['지자체명'].isin(selected_municipalities)]

    # 총 배출량 비교 막대 차트
    st.subheader("📊 지자체별 총 탄소 배출량 비교")
    fig_total = px.bar(filtered_df, x="지자체명", y="총배출량", 
                       title="지자체별 총 탄소 배출량",
                       color="총배출량",
                       color_continuous_scale=px.colors.sequential.Viridis)
    fig_total.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_total)

    # 배출 원인별 비교 막대 차트
    st.subheader("ℹ️ 지자체별 탄소 배출 원인 비교")
    fig_sources = px.bar(filtered_df, x="지자체명", 
                         y=["배출_건물_전기", "배출_건물_지역난방", "배출_건물_가스", "탄소배출_수송"],
                         title="지자체별 탄소 배출 원인 비교",
                         barmode="stack")
    fig_sources.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_sources)

    # 순 배출량 (배출량 - 흡수량) 비교
    st.subheader("👀 지자체별 순 탄소 배출량 비교")
    fig_net = px.bar(filtered_df, x="지자체명", y="순배출량", 
                     title="지자체별 순 탄소 배출량 (총 배출량 - 흡수량)",
                     color="순배출량",
                     color_continuous_scale=px.colors.diverging.RdYlGn_r)
    fig_net.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_net)

    # 산점도: 총 배출량 vs 흡수량
    st.subheader("🔍 총 탄소 배출량 vs 흡수량 관계")
    fig_scatter = px.scatter(filtered_df, x="총배출량", y="탄소흡수_산림", 
                             size="순배출량", color="지자체명",
                             hover_name="지자체명", log_x=True, log_y=True,
                             title="총 탄소 배출량 vs 흡수량 (로그 스케일)")
    st.plotly_chart(fig_scatter)

    # 상위 5개 지자체와 하위 5개 지자체 비교
    st.subheader("📊 순 탄소 배출량 상위 5개 및 하위 5개 지자체")
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
    st.subheader("ℹ️ 경기도 지자체별 탄소 중립 달성 현황")
    fig_neutrality = plot_carbon_neutrality_progress(df)
    st.plotly_chart(fig_neutrality)

    # 새로운 시각화: 상위 탄소 중립 도시
    st.subheader("🔍 탄소 중립 달성도 상위 지자체")
    top_n = st.slider("표시할 상위 지자체 수를 선택하세요", min_value=3, max_value=10, value=5)
    fig_top_neutral = plot_top_carbon_neutral_cities(df, top_n)
    st.plotly_chart(fig_top_neutral)

    # 결론 및 인사이트
    st.subheader("🧠 결론 및 인사이트")
    if st.button("AI 인사이트 생성"):
        with st.spinner("AI가 데이터를 분석하고 인사이트를 생성하고 있습니다..."):
            insights = get_ai_insights(df)
        for i, insight in enumerate(insights):
            st.markdown(f" {insight}")

    # 데이터 출처 및 주의사항
    st.info("데이터 출처: 국토교통부 탄소공간지도시스템, 본 데이터는 2022년 기준으로 최신 상황과 다를 수 있습니다")
  

if __name__ == "__main__":
    show()
