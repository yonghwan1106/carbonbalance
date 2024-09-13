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
def load_national_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "carbon_emissions_by_region(2022).csv")
    df = pd.read_csv(file_path)
    df['순배출량'] = df['탄소배출량'] - df['탄소흡수량']
    return df

@st.cache_data
def load_korea_shapefile():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "ctprvn.shp")
    if not os.path.exists(file_path):
        st.error(f"Shapefile이 존재하지 않습니다: {file_path}")
        return None
    gdf = gpd.read_file(file_path)
    return gdf.to_crs(epsg=4326)

@st.cache_data
def load_gyeonggi_data():
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
    
    if '연도' not in df.columns:
        df['연도'] = 2022
    
    return df

@st.cache_data
def load_gyeonggi_geojson():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "LARD_ADM_SECT_SGG_41_202405.shp")
    gdf = gpd.read_file(file_path)
    return gdf.to_crs(epsg=4326)

def clean_region_name(name):
    return name.replace('특별시', '').replace('광역시', '').replace('특별자치시', '').replace('도', '').strip()

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

def show_national_map():
    st.title("대한민국 광역단위별 탄소 배출 현황 (2022년)")

    df = load_national_data()
    gdf = load_korea_shapefile()

    if gdf is not None and not gdf.empty:
        df['시도별'] = df['시도별'].apply(clean_region_name)
        gdf['CTP_KOR_NM'] = gdf['CTP_KOR_NM'].apply(clean_region_name)

        merged_data = gdf.merge(df, left_on="CTP_KOR_NM", right_on="시도별", how='left')

        fig = px.choropleth_mapbox(merged_data,
                                   geojson=merged_data.geometry,
                                   locations=merged_data.index,
                                   color="순배출량",
                                   color_continuous_scale="RdYlGn_r",
                                   mapbox_style="carto-positron",
                                   zoom=5.5,
                                   center={"lat": 35.9, "lon": 127.8},
                                   opacity=0.7,
                                   labels={"순배출량": "순 탄소 배출량 (톤CO2eq)"},
                                   hover_name="시도별",
                                   hover_data=["탄소배출량", "탄소흡수량", "순배출량"])

        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=600)
        st.plotly_chart(fig, use_container_width=True)

        df_sorted = df.sort_values(by="순배출량", ascending=False)
        fig_bar = px.bar(df_sorted, 
                         x="시도별", 
                         y=["탄소배출량", "탄소흡수량", "순배출량"],
                         title="광역단위별 탄소 배출, 흡수 및 순배출량",
                         labels={"value": "톤CO2eq", "variable": "구분"},
                         height=500,
                         color_discrete_map={"탄소배출량": "red", "탄소흡수량": "green", "순배출량": "blue"})
        fig_bar.update_layout(legend_title_text="구분")
        st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("광역단위별 탄소 배출 데이터")
        st.dataframe(df.style.format({"탄소배출량": "{:,.0f}", "탄소흡수량": "{:,.0f}", "순배출량": "{:,.0f}"}))
    else:
        st.error("지도 데이터를 불러오는데 실패했습니다.")

def show_gyeonggi_map():
    st.title("경기도 지자체별 카본 지도 및 정책 제안 (2022년)")

    df = load_gyeonggi_data()
    gdf = load_gyeonggi_geojson()

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

def main():
    st.sidebar.title("탄소 배출 현황 대시보드")
    tab_selection = st.sidebar.radio("보기 선택", ["전국", "지자체 상세"])

    if tab_selection == "전국":
        show_national_map()
    else:
        show_gyeonggi_map()

if __name__ == "__main__":
    main()
