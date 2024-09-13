import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import os
import requests
import json
from utils.data_processor import analyze_emissions_trend

# Groq API 설정
MODEL = "llama-3.1-70b-versatile"
URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "gyeonggi_carbon_data_2022.csv")
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='cp949')
    
    numeric_columns = ['배출_건물_전기', '배출_건물_지역난방', '배출_건물_가스', '탄소배출_수송', '탄소흡수_산림']
    
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col].replace(',', '', regex=True), errors='coerce')
    
    df['총배출량'] = df[numeric_columns[:4]].sum(axis=1)
    df['순배출량'] = df['총배출량'] - df['탄소흡수_산림']
    
    # '연도' 열이 없다면 추가 (예: 모든 행에 2022 할당)
    if '연도' not in df.columns:
        df['연도'] = 2022
    
    return df

@st.cache_data
def load_geojson():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "LARD_ADM_SECT_SGG_41_202405.shp")
    gdf = gpd.read_file(file_path)
    gdf = gdf.to_crs(epsg=4326)  # 좌표계 변환
    return gdf

def preprocess_name(name):
    return name.replace('경기도 ', '').replace(' ', '')

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

    위 정보를 바탕으로 {region}의 탄소 배출량을 줄이기 위한 구체적인 정책을 5개 제안해주세요. 
    각 정책은 지역 특성을 고려하고, 실행 가능해야 합니다. 
    천천히 답변해도 좋으니 모든 답변 내용을 리뷰해서 100퍼센트 한글로만 답변해 주세요. 특히 한자와 일본어는 반드시 한글로 번역해서 답변해줘.
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

def show_carbon_map():
    st.title("경기도 지자체별 카본 지도 및 정책 제안 (2022년)")

    df = load_data()
    gdf = load_geojson()

    gdf['처리된_지자체명'] = gdf['SGG_NM'].apply(preprocess_name)
    df['처리된_지자체명'] = df['지자체명'].apply(preprocess_name)

    merged_data = gdf.merge(df, on='처리된_지자체명', how='inner')

    st.subheader("경기도 지자체별 순 탄소 배출량 지도")
    
    fig = px.choropleth_mapbox(merged_data, 
                               geojson=merged_data.geometry,
                               locations=merged_data.index,
                               color='순배출량',
                               color_continuous_scale="Viridis",
                               mapbox_style="carto-positron",
                               zoom=8, 
                               center = {"lat": 37.41, "lon": 127.52},
                               opacity=0.5,
                               labels={'순배출량':'순 탄소 배출량'},
                               hover_name='SGG_NM'
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

    selected_municipality = st.selectbox("지자체를 선택하세요", df['지자체명'])
    if selected_municipality:
        st.subheader(f"{selected_municipality} 상세 정보")
        municipality_data = df[df['지자체명'] == selected_municipality].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("총 배출량", f"{municipality_data['총배출량']:,.0f} tCO2eq")
        with col2:
            st.metric("탄소 흡수량", f"{municipality_data['탄소흡수_산림']:,.0f} tCO2eq")
        with col3:
            st.metric("순 배출량", f"{municipality_data['순배출량']:,.0f} tCO2eq")

        st.subheader("배출원별 비교")
        emission_sources = ['배출_건물_전기', '배출_건물_지역난방', '배출_건물_가스', '탄소배출_수송']
        fig_sources = px.pie(values=municipality_data[emission_sources], names=emission_sources, title="배출원별 비중")
        st.plotly_chart(fig_sources)

        st.subheader("📈 배출 트렌드 분석")
        trend_analysis = analyze_emissions_trend(df[df['지자체명'] == selected_municipality])
        st.write(trend_analysis)

        if st.button("🤖 AI 정책 제안 생성"):
            with st.spinner("AI가 정책을 생성 중입니다..."):
                emissions_data = {
                    'total_emissions': municipality_data['총배출량'],
                    'trend': trend_analysis,
                    'sector_breakdown': municipality_data[emission_sources].to_dict()
                }
                policy_suggestions = get_ai_policy_suggestions(selected_municipality, emissions_data)
            
            st.subheader("💡 AI 기반 정책 제안")
            st.write(policy_suggestions)

        st.subheader("🔬 정책 효과 시뮬레이션")
        reduction_percentage = st.slider("예상 감축률 (%)", 0, 100, 10)
        current_emissions = municipality_data['총배출량']
        simulated_emissions = current_emissions * (1 - reduction_percentage / 100)

        fig_simulation = px.bar(x=['현재 배출량', '정책 적용 후 예상 배출량'], 
                                y=[current_emissions, simulated_emissions],
                                title="정책 적용 효과 시뮬레이션")
        st.plotly_chart(fig_simulation)

        st.write(f"현재 배출량 {current_emissions:,.0f} tCO2eq에서 {simulated_emissions:,.0f} tCO2eq로")
        st.write(f"{reduction_percentage}% 감소할 것으로 예상됩니다.")

if __name__ == "__main__":
    show_carbon_map()
