import streamlit as st
import pandas as pd
import os
import sys
import urllib.request
import urllib.parse
import json
import re
from dotenv import load_dotenv
from utils.data_processor import get_latest_national_data
from utils.ai_helper import get_daily_eco_tip

# 환경 변수 로드
load_dotenv()

def remove_html_tags(text):
    """HTML 태그를 제거하는 함수"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

@st.cache_data(ttl=3600)  # 1시간 동안 캐시
def get_naver_news(query):
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError("Naver API 키가 설정되지 않았습니다.")

    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/news.json?query={encText}&display=5&start=1&sort=date"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    
    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            return json.loads(response_body.decode('utf-8'))
        else:
            raise Exception(f"Error Code: {rescode}")
    except Exception as e:
        raise Exception(f"API 호출 실패: {str(e)}")

@st.cache_data(ttl=86400)  # 24시간 동안 캐시
def get_cached_national_data():
    try:
        return get_latest_national_data()
    except Exception as e:
        st.error(f"국가 데이터를 가져오는 중 오류 발생: {str(e)}")
        return None

@st.cache_data(ttl=86400)  # 24시간 동안 캐시
def get_cached_daily_tip():
    try:
        return get_daily_eco_tip()
    except Exception as e:
        st.error(f"일일 에코 팁을 가져오는 중 오류 발생: {str(e)}")
        return "오늘의 에코 팁을 불러올 수 없습니다. 대신 작은 실천으로 시작해보세요: 사용하지 않는 전자기기의 플러그를 뽑아두세요."

def show():
    st.title("🍃 Carbon Footprint Korea")
    
    # 환영 메시지
    st.write("""
    환영합니다! Carbon Footprint Korea는 당신의 탄소 발자국을 이해하고 줄이는 데 도움을 주는 플랫폼입니다.
    함께 더 나은 미래를 만들어 갑시다.
    """)
    
    # 주요 기능 소개
    st.header("주요 기능")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🧮 탄소 발자국 계산")
        st.write("개인의 일상 활동에 따른 탄소 발자국을 계산해보세요.")
        if st.button("계산하기"):
            st.switch_page("pages/carbon_calculator.py")
    
    with col2:
        st.subheader("🗺️ 전국 탄소 지도")
        st.write("대한민국 전체의 탄소 배출 현황을 한눈에 확인하세요.")
        if st.button("지도 보기"):
            st.switch_page("pages/carbon_map.py")
    
    with col3:
        st.subheader("💰 탄소 크레딧 거래")
        st.write("여러분의 노력을 크레딧으로 보상받고 거래해보세요.")
        if st.button("마켓플레이스"):
            st.switch_page("pages/marketplace.py")

    
    # 최신 뉴스 또는 업데이트
    st.header("📰 최신 탄소 중립 소식")
    try:
        news_data = get_naver_news("탄소 중립")
        
        for item in news_data['items']:
            clean_title = remove_html_tags(item['title'])
            clean_description = remove_html_tags(item['description'])
            st.markdown(f"<h5 style='font-size: 13px;'>{clean_title}</h5>", unsafe_allow_html=True)
            st.write(clean_description)
            st.write(f"[기사 보기]({item['link']})")
            st.write("---")
    except Exception as e:
        st.error(f"뉴스를 가져오는 중 오류가 발생했습니다: {str(e)}")
        st.write("대체 뉴스:")
        news_items = [
            "정부, 2050 탄소중립 로드맵 발표",
            "서울시, 도시 전체 태양광 패널 설치 계획 추진",
            "기업들의 ESG 경영 확대로 탄소 배출 감소 추세"
        ]
        for item in news_items:
            st.write(f"• {item}")

          
    # 일일 에코 팁
    st.header("🌱 오늘의 에코 팁")
    daily_tip = get_cached_daily_tip()
    st.info(daily_tip)
     
    # 사용자 참여 유도
    st.header("함께 만들어가는 녹색 미래")
    st.write("여러분의 작은 실천이 큰 변화를 만듭니다. 지금 시작해보세요!")
    if st.button("도전 과제 참여하기"):
        st.switch_page("pages/challenges.py")

    # 최신 국가 데이터
    st.header("🇰🇷 대한민국 최신 탄소 배출 현황")
    national_data = get_cached_national_data()
    if national_data:
        try:
            total_emissions = national_data.get('total_emissions', 'N/A')
            emissions_change = national_data.get('emissions_change', 'N/A')
            
            if isinstance(total_emissions, (int, float)):
                total_emissions_str = f"{total_emissions:,} 톤 CO2e"
            else:
                total_emissions_str = "데이터 없음"
            
            if isinstance(emissions_change, (int, float)):
                delta_str = f"{emissions_change:+.1f}% 전년 대비"
            else:
                delta_str = "변화율 데이터 없음"
            
            st.metric(label="총 탄소 배출량", value=total_emissions_str, delta=delta_str)
        except Exception as e:
            st.error(f"데이터 처리 중 오류 발생: {str(e)}")
    else:
        st.error("현재 국가 데이터를 표시할 수 없습니다.")
        
if __name__ == "__main__":
    show()