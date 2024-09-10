import streamlit as st
import random
import time
import os   

# 초기 설정
st.title("Eco Game: 탄소중립을 위한 도전")

# 사이드바 게임 정보
st.sidebar.header("게임 정보")
st.sidebar.markdown("탄소중립 목표를 달성하기 위해 올바른 결정을 내려보세요!")

# 초기 변수
carbon_footprint = 100  # 초기 탄소 발자국
score = 0  # 초기 점수
level = 1  # 시작 레벨

def update_graph():
    st.bar_chart({"탄소 발자국": [carbon_footprint]})

def level_description(level):
    descriptions = {
        1: "레벨 1: 가정에서 에너지 절약하기",
        2: "레벨 2: 교통수단 선택하기",
        3: "레벨 3: 음식 선택하기",
        4: "레벨 4: 여행 계획하기"
    }
    return descriptions.get(level, "더 이상의 레벨은 없습니다.")

def make_choice(options, results):
    choice = st.selectbox("당신의 선택:", options)
    show_image(choice)  # 선택한 후 이미지 표시
    result = results.get(choice, ("기본 결과입니다.", 0, 0))
    st.write(result[0])
    return result[1], result[2]

def show_image(choice):
    images = {
        "LED 조명으로 교체하기": "images/led.png",
        "에어컨 온도 낮추기": "images/aircon.png",
        "전기 난방 사용하기": "images/heating.png",
        "자전거": "images/bike.png",
        "대중교통": "images/bus.png",
        "자동차": "images/car.png",
        "비행기": "images/plane.png",
        "채식 식단": "images/vegetarian.png",
        "현지 음식": "images/local_food.png",
        "육류 중심 식단": "images/meat.png"
    }
    
    image_path = images.get(choice)
    if image_path and os.path.exists(image_path):
        st.image(image_path, width=300)
    else:
        st.write("이미지를 찾을 수 없습니다.")

while carbon_footprint > 0 and carbon_footprint < 200:
    st.subheader(level_description(level))
    
    if level == 1:
        options = ["LED 조명으로 교체하기", "에어컨 온도 낮추기", "전기 난방 사용하기"]
        results = {
            "LED 조명으로 교체하기": ("탄소 배출량을 줄였습니다!", -10, 15),
            "에어컨 온도 낮추기": ("에어컨 사용으로 탄소 배출이 증가했습니다.", 5, -5),
            "전기 난방 사용하기": ("난방 사용으로 탄소 배출이 증가했습니다.", 10, -10)
        }

    elif level == 2:
        options = ["자전거", "대중교통", "자동차", "비행기"]
        results = {
            "자전거": ("좋은 선택입니다! 탄소 배출량을 줄였습니다.", -5, 10),
            "대중교통": ("괜찮은 선택입니다! 탄소 배출량이 약간 줄었습니다.", -3, 5),
            "자동차": ("자동차를 선택했습니다. 탄소 배출량이 증가합니다.", 10, -5),
            "비행기": ("비행기를 선택했습니다. 탄소 배출량이 크게 증가합니다!", 20, -15)
        }
    elif level == 3:
        options = ["채식 식단", "현지 음식", "육류 중심 식단"]
        results = {
            "채식 식단": ("훌륭한 선택입니다! 탄소 배출량을 줄였습니다.", -15, 20),
            "현지 음식": ("현지 음식을 선택해 탄소 배출량이 줄었습니다.", -5, 10),
            "육류 중심 식단": ("육류 섭취로 인해 탄소 배출량이 증가했습니다.", 10, -10)
        }
    elif level == 4:
        options = ["기차 여행", "친환경 호텔 선택", "자동차 여행"]
        results = {
            "기차 여행": ("탄소 배출량을 최소화한 여행 선택입니다!", -10, 15),
            "친환경 호텔 선택": ("친환경 호텔을 선택해 탄소 배출량을 줄였습니다.", -5, 10),
            "자동차 여행": ("자동차 여행은 탄소 배출량을 증가시킵니다.", 15, -5)
        }
    else:
        st.write("축하합니다! 모든 레벨을 완료했습니다!")
        break
    
    delta_carbon, delta_score = make_choice(options, results)
    carbon_footprint += delta_carbon
    score += delta_score
    
    st.write(f"현재 탄소 발자국: {carbon_footprint}")
    st.write(f"현재 점수: {score}")
    
    update_graph()
    
    if carbon_footprint <= 0:
        st.success("축하합니다! 탄소중립 목표를 달성했습니다!")
        break
    elif carbon_footprint >= 200:
        st.error("탄소 배출량이 너무 많습니다! 게임 오버!")
        break
    
    level += 1
    time.sleep(1)  # 사용자가 다음 레벨로 넘어갈 때 기다리는 시간

