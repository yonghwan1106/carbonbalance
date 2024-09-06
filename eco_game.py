import streamlit as st
import pandas as pd
import random
from utils.data_processor import load_gyeonggi_data
from utils.ai_helper import generate_eco_mission

def show():
    st.title("ECO 챌린지: 경기도 탄소 중립 게임")

    # 사용자 이름 입력
    user_name = st.text_input("당신의 이름을 입력하세요")

    if user_name:
        st.write(f"안녕하세요, {user_name}님! ECO 챌린지에 오신 것을 환영합니다.")

        # 게임 모드 선택
        game_mode = st.radio("게임 모드를 선택하세요", ["탄소 퀴즈", "ECO 미션"])

        if game_mode == "탄소 퀴즈":
            play_carbon_quiz(user_name)
        elif game_mode == "ECO 미션":
            play_eco_mission(user_name)

def play_carbon_quiz(user_name):
    st.subheader("경기도 탄소 퀴즈")
    
    # 데이터 로드
    df = load_gyeonggi_data()

    # 퀴즈 문제 생성
    questions = generate_quiz_questions(df)

    score = 0
    for i, question in enumerate(questions, 1):
        st.write(f"문제 {i}: {question['question']}")
        user_answer = st.radio(f"답변을 선택하세요 (문제 {i})", question['options'])
        
        if st.button(f"정답 확인 (문제 {i})"):
            if user_answer == question['correct_answer']:
                st.success("정답입니다!")
                score += 1
            else:
                st.error(f"틀렸습니다. 정답은 {question['correct_answer']}입니다.")
            
            st.write(question['explanation'])

    st.subheader("퀴즈 결과")
    st.write(f"{user_name}님의 점수: {score}/{len(questions)}")
    
    if score == len(questions):
        st.balloons()
        st.success("축하합니다! 만점을 획득하셨습니다.")
    elif score >= len(questions) / 2:
        st.success("잘 하셨습니다! 경기도의 탄소 상황에 대해 잘 알고 계시네요.")
    else:
        st.info("아쉽네요. 다시 한번 도전해보세요!")

def play_eco_mission(user_name):
    st.subheader("일일 ECO 미션")

    # AI를 사용하여 미션 생성
    mission = generate_eco_mission()

    st.write(f"오늘의 미션: {mission['description']}")
    st.write(f"예상 탄소 감축량: {mission['carbon_reduction']} kg CO2")

    # 미션 수행 여부 체크
    mission_completed = st.checkbox("미션을 완료했어요!")

    if mission_completed:
        st.success(f"축하합니다! {mission['carbon_reduction']} kg의 CO2 배출을 감소시켰어요.")
        st.balloons()

    # 미션 히스토리 (실제 구현 시 데이터베이스 연동 필요)
    st.subheader("나의 ECO 미션 히스토리")
    mission_history = [
        {"date": "2024-03-01", "mission": "일회용품 사용 안 하기", "carbon_reduction": 0.5},
        {"date": "2024-03-02", "mission": "대중교통 이용하기", "carbon_reduction": 2.3},
        # ... 더 많은 미션 히스토리
    ]

    history_df = pd.DataFrame(mission_history)
    st.table(history_df)

    total_reduction = history_df['carbon_reduction'].sum()
    st.write(f"총 감축한 CO2: {total_reduction:.2f} kg")

def generate_quiz_questions(df):
    # 실제 구현 시 더 다양하고 동적인 문제 생성 로직 필요
    questions = [
        {
            "question": "경기도에서 가장 탄소 배출량이 많은 도시는?",
            "options": ["수원시", "성남시", "고양시", "용인시"],
            "correct_answer": "수원시",  # 실제 데이터에 따라 변경 필요
            "explanation": "수원시는 경기도 내에서 가장 큰 도시 중 하나로, 산업과 인구가 밀집되어 있어 탄소 배출량이 높습니다."
        },
        {
            "question": "경기도의 연간 총 탄소 배출량은 약 얼마일까요?",
            "options": ["5천만 톤", "1억 톤", "1억 5천만 톤", "2억 톤"],
            "correct_answer": "1억 5천만 톤",  # 실제 데이터에 따라 변경 필요
            "explanation": "경기도는 대한민국에서 가장 인구가 많은 지역으로, 높은 경제 활동으로 인해 상당한 양의 탄소를 배출합니다."
        },
        # ... 더 많은 문제 추가
    ]
    return questions

if __name__ == "__main__":
    show()