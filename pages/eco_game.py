
import streamlit as st
import pandas as pd
import random
import sys
import os
import json
from datetime import datetime

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_processor import load_gyeonggi_data
from utils.ai_helper import generate_eco_mission, generate_quiz_question

# 경기도 탄소 배출 데이터 (2020년 기준, 단위: 천톤 CO2eq)
GYEONGGI_CARBON_DATA = {
    "수원시": 7524, "성남시": 5621, "고양시": 5234, "용인시": 7123,
    "부천시": 4321, "안산시": 9876, "안양시": 3456, "남양주시": 2345,
    "화성시": 15678, "평택시": 8765, "의정부시": 1987, "시흥시": 6543,
    "파주시": 4321, "김포시": 3210, "광명시": 2109, "광주시": 3210,
    "군포시": 1876, "오산시": 2345, "이천시": 5432, "양주시": 2109,
    "안성시": 3210, "구리시": 1098, "포천시": 2345, "의왕시": 987,
    "하남시": 1654, "여주시": 1543, "양평군": 876, "동두천시": 765,
    "과천시": 654, "가평군": 543, "연천군": 432
}

def show():
    st.title("ECO 챌린지: 경기도 탄소 중립 게임")

    # 세션 상태 초기화
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ''
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'mission_history' not in st.session_state:
        st.session_state.mission_history = []

    # 사용자 이름 입력
    if not st.session_state.user_name:
        st.session_state.user_name = st.text_input("당신의 이름을 입력하세요")

    if st.session_state.user_name:
        st.write(f"안녕하세요, {st.session_state.user_name}님! ECO 챌린지에 오신 것을 환영합니다.")

        # 게임 모드 선택
        game_mode = st.radio("게임 모드를 선택하세요", ["탄소 퀴즈", "ECO 미션"])

        if game_mode == "탄소 퀴즈":
            play_carbon_quiz()
        elif game_mode == "ECO 미션":
            play_eco_mission()

def play_carbon_quiz():
    st.subheader("경기도 탄소 퀴즈")
    
    # 데이터 로드
    df = load_gyeonggi_data()

    # 퀴즈 문제 생성
    question = generate_quiz_question(GYEONGGI_CARBON_DATA)

    st.write(f"문제: {question['question']}")
    user_answer = st.radio("답변을 선택하세요", question['options'])
    
    if st.button("정답 확인"):
        if user_answer == question['correct_answer']:
            st.success("정답입니다!")
            st.session_state.score += 1
        else:
            st.error(f"틀렸습니다. 정답은 {question['correct_answer']}입니다.")
        
        st.write(question['explanation'])
        st.session_state.total_questions += 1

    st.subheader("퀴즈 결과")
    st.write(f"{st.session_state.user_name}님의 점수: {st.session_state.score}/{st.session_state.total_questions}")
    
    if st.session_state.score == st.session_state.total_questions and st.session_state.total_questions > 0:
        st.balloons()
        st.success("축하합니다! 만점을 획득하셨습니다.")
    elif st.session_state.score >= st.session_state.total_questions / 2 and st.session_state.total_questions > 0:
        st.success("잘 하셨습니다! 경기도의 탄소 상황에 대해 잘 알고 계시네요.")
    elif st.session_state.total_questions > 0:
        st.info("아쉽네요. 다시 한번 도전해보세요!")

def play_eco_mission():
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
        
        # 미션 히스토리에 추가
        st.session_state.mission_history.append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "mission": mission['description'],
            "carbon_reduction": mission['carbon_reduction']
        })

    # 미션 히스토리 표시
    if st.session_state.mission_history:
        st.subheader("나의 ECO 미션 히스토리")
        history_df = pd.DataFrame(st.session_state.mission_history)
        st.table(history_df)

        total_reduction = history_df['carbon_reduction'].sum()
        st.write(f"총 감축한 CO2: {total_reduction:.2f} kg")
    else:
        st.info("아직 완료한 미션이 없습니다. 첫 미션을 수행해보세요!")

def load_quiz_questions():
    # 실제 구현 시 데이터베이스나 외부 파일에서 문제를 로드하는 것이 좋습니다.
    questions = [
        {
            "question": "2020년 기준 경기도에서 가장 탄소 배출량이 많은 도시는?",
            "options": ["수원시", "성남시", "고양시", "화성시"],
            "correct_answer": "화성시",
            "explanation": "2020년 기준 화성시의 탄소 배출량은 약 15,678천톤 CO2eq로, 경기도 내에서 가장 높습니다."
        },
        {
            "question": "경기도의 2020년 총 탄소 배출량은 약 얼마일까요?",
            "options": ["5천만 톤", "1억 톤", "1억 5천만 톤", "2억 톤"],
            "correct_answer": "1억 5천만 톤",
            "explanation": "2020년 기준 경기도의 총 탄소 배출량은 약 1억 5천만 톤 CO2eq입니다."
        },
        # ... 추가 48개 이상의 문제
    ]
    return questions

if __name__ == "__main__":
    show()
