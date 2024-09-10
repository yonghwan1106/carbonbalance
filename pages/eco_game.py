import streamlit as st
import pandas as pd
import random

# 게임 상태 저장 및 업데이트를 위한 클래스
class EcoGame:
    def __init__(self):
        self.city_status = {
            '탄소배출량': 1000,  # 초기 탄소 배출량
            '점수': 0,
            '탄소크레딧': 0,
            '레벨': 1
        }
        self.missions = [
            {'이름': '재활용 캠페인', '점수': 10, '탄소감소': 50},
            {'이름': '전기 절약', '점수': 15, '탄소감소': 70},
            {'이름': '친환경 교통수단 이용', '점수': 20, '탄소감소': 100},
            {'이름': '에너지 효율 개선', '점수': 25, '탄소감소': 150}
        ]

    def show_status(self):
        return self.city_status
    
    def perform_mission(self, mission_index):
        mission = self.missions[mission_index]
        self.city_status['탄소배출량'] -= mission['탄소감소']
        self.city_status['점수'] += mission['점수']
        self.city_status['탄소크레딧'] += mission['점수'] * 0.5  # 0.5는 예시, 실제 비율에 따라 조정 가능

        if self.city_status['탄소배출량'] < 0:
            self.city_status['탄소배출량'] = 0
        
        # 레벨업
        if self.city_status['점수'] >= self.city_status['레벨'] * 50:
            self.city_status['레벨'] += 1

        return mission

# Streamlit 애플리케이션
st.title("💚 탄소 중립 도전!")

# 게임 객체 생성
if 'game' not in st.session_state:
    st.session_state.game = EcoGame()

game = st.session_state.game

# 현재 도시 상태 표시
status = game.show_status()
st.subheader("현재 도시 상태")
st.write(f"탄소 배출량: {status['탄소배출량']} 톤 CO2e")
st.write(f"점수: {status['점수']}")
st.write(f"탄소 크레딧: {status['탄소크레딧']}")
st.write(f"레벨: {status['레벨']}")

# 미션 수행
st.subheader("미션 수행")
mission_options = [mission['이름'] for mission in game.missions]
selected_mission_index = st.selectbox("미션을 선택하세요", range(len(mission_options)), format_func=lambda x: mission_options[x])

if st.button("미션 수행"):
    mission = game.perform_mission(selected_mission_index)
    st.success(f"미션 '{mission['이름']}' 수행 완료! 점수 +{mission['점수']}, 탄소 배출량 -{mission['탄소감소']}")

# 거래 내역을 위한 데이터 생성 (예시 데이터)
transaction_history = pd.DataFrame({
    '날짜': pd.date_range(start='2024-01-01', periods=5, freq='D'),
    '거래유형': ['구매', '판매', '구매', '판매', '구매'],
    '양': [50, 20, 30, 10, 40]
})

# 거래 내역 표시
st.subheader("거래 내역")
st.write(transaction_history)
