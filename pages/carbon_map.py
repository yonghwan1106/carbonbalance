import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import os

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
    
    return df

@st.cache_data
def load_geojson():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "LARD_ADM_SECT_SGG_41_202405.shp")
    gdf = gpd.read_file(file_path)
    gdf = gdf.to_crs(epsg=4326)  # 좌표계 변환
    return gdf

def preprocess_name(name):
    return name.replace('경기도 ', '').replace(' ', '')

def show_carbon_map():
    st.title("경기도 지자체별 카본 지도 (2022년)")

    df = load_data()
    gdf = load_geojson()

    # ShapeFile의 열 이름 확인
    #st.subheader("ShapeFile 구조")
    #st.write("ShapeFile의 열:", gdf.columns.tolist())
    #st.write("ShapeFile의 지자체명:", gdf['SGG_NM'].tolist())
    #st.write("CSV 파일의 지자체명:", df['지자체명'].tolist())

    # 지자체명 전처리
    gdf['처리된_지자체명'] = gdf['SGG_NM'].apply(preprocess_name)
    df['처리된_지자체명'] = df['지자체명'].apply(preprocess_name)

    # 매핑된 데이터만 사용
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

    # 지자체 선택 및 상세 정보 표시
    selected_municipality = st.selectbox("지자체를 선택하세요", df['지자체명'])
    if selected_municipality:
        st.subheader(f"{selected_municipality} 상세 정보")
        municipality_data = df[df['지자체명'] == selected_municipality].iloc[0]
        st.write(f"총 배출량: {municipality_data['총배출량']:,.0f} tCO2eq")
        st.write(f"탄소 흡수량: {municipality_data['탄소흡수_산림']:,.0f} tCO2eq")
        st.write(f"순 배출량: {municipality_data['순배출량']:,.0f} tCO2eq")

    # 배출원별 비교 차트
    st.subheader("배출원별 비교")
    emission_sources = ['배출_건물_전기', '배출_건물_지역난방', '배출_건물_가스', '탄소배출_수송']
    fig_sources = px.bar(df, x='지자체명', y=emission_sources, title="지자체별 배출원 비교")
    fig_sources.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_sources)

if __name__ == "__main__":
    show_carbon_map()
