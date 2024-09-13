import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from utils.db_manager import get_supabase_client

def get_user_data(user_id):
    supabase = get_supabase_client()
    
    # 사용자 정보 가져오기
    user_response = supabase.table('users').select('*').eq('id', user_id).execute()
    if len(user_response.data) == 0:
        st.error("사용자를 찾을 수 없습니다.")
        return None
    
    user = user_response.data[0]
    
    # 탄소 크레딧 정보 가져오기
    credits_response = supabase.table('carbon_credits').select('*').eq('user_id', user_id).execute()
    current_carbon = sum(credit['amount'] for credit in credits_response.data)
    
    # 트랜잭션 정보 가져오기
    transactions_response = supabase.table('transactions').select('*').eq('user_id', user_id).execute()
    
    # 배지와 업적 계산 (예시)
    badges = ["초보 환경 지킴이"]
    if current_carbon > 1000:
        badges.append("탄소 저감 마스터")
    
    achievements = [
        {"name": "첫 탄소 크레딧 획득", "date": user['created_at'][:10]}
    ]
    if len(transactions_response.data) > 10:
        achievements.append({"name": "10회 이상 거래", "date": datetime.now().strftime("%Y-%m-%d")})
    
    return {
        "name": user['username'],
        "email": user['email'],
        "join_date": user['created_at'][:10],
        "carbon_goal": 5000.0,  # 목표는 임의 설정, 실제로는 사용자 설정 값을 사용해야 함
        "current_carbon": current_carbon,
        "badges": badges,
        "achievements": achievements,
    }

def show():
    st.title("🙋 내 프로필")

    # 실제 애플리케이션에서는 로그인한 사용자의 ID를 사용해야 합니다.
    # 여기서는 예시로 user_id를 1로 설정합니다.
    user_id = 1
    
    user_data = get_user_data(user_id)
    if user_data is None:
        return

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
        progress = max(0, min(1, progress))
        progress_percentage = progress * 100
        
        st.progress(progress)
        st.write(f"연간 목표: {user_data['carbon_goal']} kg CO2e")
        st.write(f"현재 발자국: {user_data['current_carbon']} kg CO2e")
        st.write(f"달성률: {progress_percentage:.1f}%")
    else:
        st.write("탄소 감축 목표가 설정되지 않았습니다.")

    # 월별 탄소 발자국 차트 (실제 데이터를 사용하려면 추가 쿼리 필요)
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
    col1.metric("총 감축량", f"{user_data['current_carbon']} kg CO2e", "15%")
    col2.metric("연속 미션 달성", "25일", "2일")  # 이 데이터는 실제로 계산해야 함
    col3.metric("참여한 챌린지", "5개", "1개")  # 이 데이터는 실제로 계산해야 함

if __name__ == "__main__":
    show()
