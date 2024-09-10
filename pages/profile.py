import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def get_user_data():
    return {
        "name": "홍길동",
        "email": "hong@example.com",
        "join_date": "2023-01-01",
        "carbon_goal": 5000.0,  # float으로 명시
        "current_carbon": 4500.0,  # float으로 명시
        "badges": ["초보 환경 지킴이", "대중교통 마스터", "재활용 챔피언"],
        "achievements": [
            {"name": "첫 탄소 저감", "date": "2023-01-15"},
            {"name": "100일 연속 미션 수행", "date": "2023-04-10"},
            {"name": "1톤 CO2 감축", "date": "2023-06-30"},
        ]
    }

def show():
    st.title("🙋 내 프로필")

    user_data = get_user_data()
    st.write("Debug: User Data", user_data)  # 디버그용 출력
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("개인 정보")
        st.write(f"이름: {user_data['name']}")
        st.write(f"이메일: {user_data['email']}")
        st.write(f"가입일: {user_data['join_date']}")

        if st.button("개인 정보 수정"):
            st.write("개인 정보 수정 기능은 아직 구현되지 않았습니다.")

    with col2:
        st.image("https://via.placeholder.com/150", caption="프로필 사진")

    st.subheader("🎯 탄소 감축 목표 및 성과")
    
    if user_data['carbon_goal'] > 0:
        progress = (user_data['carbon_goal'] - user_data['current_carbon']) / user_data['carbon_goal']
        progress = max(0, min(1, progress))  # 진행률을 0에서 1 사이로 제한
        progress_percentage = progress * 100  # 백분율로 변환
        
        st.progress(progress)  # progress()에는 0에서 1 사이의 값을 전달
        st.write(f"연간 목표: {user_data['carbon_goal']} kg CO2e")
        st.write(f"현재 발자국: {user_data['current_carbon']} kg CO2e")
        st.write(f"달성률: {progress_percentage:.1f}%")
    else:
        st.write("탄소 감축 목표가 설정되지 않았습니다.")

    # 월별 탄소 발자국 차트 (예시 데이터)
    months = pd.date_range(start="2023-01-01", end="2023-12-31", freq='M')
    carbon_data = pd.DataFrame({
        'month': months,
        'carbon': [500, 480, 460, 440, 420, 400, 380, 360, 340, 320, 300, 280]
    })

    fig = px.line(carbon_data, x='month', y='carbon', title='월별 탄소 발자국')
    st.plotly_chart(fig)

    st.subheader("🏅 획득한 배지")
    for badge in user_data['badges']:
        st.markdown(f"- {badge}")

    st.subheader("🏆 업적")
    for achievement in user_data['achievements']:
        st.markdown(f"- {achievement['name']} ({achievement['date']})")

    st.subheader("📊 통계")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 감축량", "1.5 톤 CO2e", "15%")
    col2.metric("연속 미션 달성", "25일", "2일")
    col3.metric("참여한 챌린지", "5개", "1개")

if __name__ == "__main__":
    show()
