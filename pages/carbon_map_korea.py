import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import os

def clean_region_name(name):
    # 필요에 따라 지역 이름을 정제하는 로직 추가
    return name.replace('특별시', '').replace('광역시', '').replace('특별자치시', '').replace('도', '').strip()

@st.cache_data
def load_national_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "carbon_emissions_by_region(2022).csv")
    df = pd.read_csv(file_path)
    df['시도별'] = df['시도별'].apply(clean_region_name)
    df['총계'] = df['탄소배출량'] - df['탄소흡수량']
    return df

@st.cache_data
def load_korea_shapefile():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "ctprvn.shp")
    st.write(f"Shapefile 경로: {file_path}")
    if not os.path.exists(file_path):
        st.error(f"Shapefile이 존재하지 않습니다: {file_path}")
        return None
    gdf = gpd.read_file(file_path)
    gdf = gdf.to_crs(epsg=4326)
    gdf['CTP_KOR_NM'] = gdf['CTP_KOR_NM'].apply(clean_region_name)
    st.write("Shapefile 열 이름:", gdf.columns.tolist())
    return gdf

def show_national_map():
    st.title("대한민국 광역단위별 탄소 배출 현황 (2022년)")

    df = load_national_data()
    gdf = load_korea_shapefile()

    if gdf is not None and not gdf.empty:
        # 데이터 결합 (열 이름을 실제 Shapefile의 열 이름으로 변경)
        merged_data = gdf.merge(df, left_on="CTP_KOR_NM", right_on="시도별", how='left')

        # 지도맵 생성
        fig = px.choropleth_mapbox(merged_data,
                                   geojson=merged_data.geometry,
                                   locations=merged_data.index,
                                   color="총계",
                                   color_continuous_scale="RdYlGn_r",
                                   mapbox_style="carto-positron",
                                   zoom=5.5,
                                   center={"lat": 35.9, "lon": 127.8},
                                   opacity=0.7,
                                   labels={"총계": "순 탄소 배출량"},
                                   hover_name="시도별",
                                   hover_data=["탄소배출량", "탄소흡수량", "총계"])

        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          height=600)

        st.plotly_chart(fig, use_container_width=True)

        # 막대 그래프 생성
        df_sorted = df.sort_values(by="총계", ascending=False)
        fig_bar = px.bar(df_sorted, 
                         x="시도별", 
                         y=["탄소배출량", "탄소흡수량", "총계"],
                         title="광역단위별 탄소 배출 및 흡수량",
                         labels={"value": "톤CO2eq", "variable": "구분"},
                         height=500,
                         color_discrete_map={"탄소배출량": "red", "탄소흡수량": "green", "총계": "blue"})
        st.plotly_chart(fig_bar, use_container_width=True)

        # 데이터 테이블 표시
        st.subheader("광역단위별 탄소 배출 데이터")
        st.dataframe(df)
    else:
        st.error("지도 데이터를 불러오는데 실패했습니다.")

def main():
    st.sidebar.title("탄소 배출 현황 대시보드")
    tab_selection = st.sidebar.radio("보기 선택", ["전국", "상세"])

    if tab_selection == "전국":
        show_national_map()
    else:
        # 여기에 상세 보기 함수 호출
        st.write("상세 보기는 아직 구현되지 않았습니다.")

if __name__ == "__main__":
    main()
