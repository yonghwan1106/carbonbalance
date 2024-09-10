import streamlit as st
import pandas as pd
from utils.credit_manager import CreditManager

# CreditManager 인스턴스 생성
manager = CreditManager()

def get_user_credits(user_id):
    return manager.get_credit_balance(user_id)

def get_transaction_history(user_id):
    transactions = manager.get_transaction_history(user_id)
    df = pd.DataFrame(transactions)
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
    return df

def execute_transaction(user_id, transaction_type, amount):
    try:
        if transaction_type == "buy":
            credit_id = manager.issue_credit(amount, user_id)
            st.success(f"{amount} 크레딧이 성공적으로 구매되었습니다. 크레딧 ID: {credit_id}")
        elif transaction_type == "sell":
            # 사용자의 크레딧 중 첫 번째 것을 사용 (실제로는 더 복잡한 로직이 필요할 수 있습니다)
            user_credits = [credit for credit in manager.credits.values() if credit.owner == user_id and credit.is_active]
            if user_credits:
                credit_to_sell = user_credits[0]
                manager.retire_credit(credit_to_sell.id, amount)
                st.success(f"{amount} 크레딧이 성공적으로 판매되었습니다.")
            else:
                st.error("판매할 크레딧이 없습니다.")
        return True
    except ValueError as e:
        st.error(f"거래 실패: {str(e)}")
        return False

st.title("💰 탄소 크레딧 거래")
st.write("여러분의 노력을 크레딧으로 보상받고 거래해보세요.")

# 사용자 선택
user_id = st.text_input("사용자 ID를 입력하세요:", value="user123")

# 사용자 크레딧 현황
user_credits = get_user_credits(user_id)
st.subheader("보유 탄소 크레딧")
st.write(f"현재 보유 크레딧: {user_credits} 크레딧")

# 거래 섹션
st.subheader("크레딧 거래")
transaction_type = st.selectbox("거래 유형 선택", ["buy", "sell"])

# max_value를 조건부로 설정
if transaction_type == "sell":
    max_value = min(int(user_credits), 1000)  # user_credits와 1000 중 작은 값
else:
    max_value = 1000

amount = st.number_input("거래할 크레딧 양", min_value=1, max_value=max_value, value=1)

if st.button("거래 실행"):
    if execute_transaction(user_id, transaction_type, amount):
        # 거래 후 업데이트된 크레딧 현황
        user_credits = get_user_credits(user_id)
        st.write(f"현재 보유 크레딧: {user_credits} 크레딧")

# 거래 내역 확인
st.subheader("거래 내역")
transaction_history = get_transaction_history(user_id)
if not transaction_history.empty:
    st.write(transaction_history)
else:
    st.write("거래 내역이 없습니다.")

# 만료된 크레딧 처리
manager.expire_credits()
