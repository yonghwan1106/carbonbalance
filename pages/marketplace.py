import streamlit as st
import pandas as pd
import random

# 예제 데이터
def get_user_credits(user_id):
    # 실제로는 데이터베이스에서 조회하거나 API를 호출해야 합니다.
    # 여기서는 임시로 데이터를 생성합니다.
    return {
        'user_id': user_id,
        'credits': random.randint(100, 1000)
    }

def get_transaction_history(user_id):
    # 실제로는 데이터베이스에서 조회하거나 API를 호출해야 합니다.
    # 여기서는 임시로 데이터를 생성합니다.
    return pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=5, freq='D'),
        'transaction_type': ['buy', 'sell', 'buy', 'sell', 'buy'],
        'amount': [50, 20, 30, 10, 40]
    })

def execute_transaction(user_id, transaction_type, amount):
    # 실제로는 데이터베이스에서 거래를 수행하고 결과를 반환해야 합니다.
    # 여기서는 성공적으로 거래가 완료되었다고 가정합니다.
    return True

st.title("💰 탄소 크레딧 거래")
st.write("여러분의 노력을 크레딧으로 보상받고 거래해보세요.")

# 사용자 선택
user_id = st.text_input("사용자 ID를 입력하세요:", value="user123")

# 사용자 크레딧 현황
user_credits = get_user_credits(user_id)
st.subheader("보유 탄소 크레딧")
st.write(f"현재 보유 크레딧: {user_credits['credits']} 크레딧")

# 거래 섹션
st.subheader("크레딧 거래")

transaction_type = st.selectbox("거래 유형 선택", ["buy", "sell"])
amount = st.number_input("거래할 크레딧 양", min_value=1, max_value=user_credits['credits'] if transaction_type == "sell" else 1000, value=1)

if st.button("거래 실행"):
    if execute_transaction(user_id, transaction_type, amount):
        st.success(f"{transaction_type.capitalize()} 거래가 성공적으로 완료되었습니다.")
        # 거래 후 업데이트된 크레딧 현황
        user_credits = get_user_credits(user_id)
        st.write(f"현재 보유 크레딧: {user_credits['credits']} 크레딧")
    else:
        st.error("거래에 실패했습니다. 다시 시도해 주세요.")

# 거래 내역 확인
st.subheader("거래 내역")
transaction_history = get_transaction_history(user_id)
st.write(transaction_history)

