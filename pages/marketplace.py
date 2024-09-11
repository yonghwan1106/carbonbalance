import streamlit as st
import pandas as pd
from utils.credit_manager import CreditManager

def show():
    st.title("💰 탄소 크레딧 거래")

    # 로그인 상태 확인
    if 'user_data' not in st.session_state or not st.session_state.user_data:
        st.warning("이 페이지를 이용하려면 로그인이 필요합니다.")
        return

    user_id = st.session_state.user_data.get('user_id')
    if not user_id:
        st.error("사용자 정보를 찾을 수 없습니다. 다시 로그인해주세요.")
        return

    show_marketplace(user_id)

def show_marketplace(user_id):
    # 탄소 크레딧 설명 추가
    with st.expander("탄소 크레딧이란?"):
        st.write("""
        탄소 크레딧은 온실가스 배출량을 줄이거나 제거하는 노력을 수치화한 것입니다. 
        1 탄소 크레딧은 일반적으로 1톤의 이산화탄소 또는 이에 상응하는 다른 온실가스의 감축을 나타냅니다.

        **탄소 크레딧의 개념:**
        - 기업이나 개인이 온실가스 배출을 줄이면 크레딧을 얻습니다.
        - 배출 목표를 초과 달성한 경우, 초과분을 크레딧으로 받아 다른 기업에 판매할 수 있습니다.
        - 반대로, 배출 목표를 달성하지 못한 기업은 크레딧을 구매하여 부족분을 보완할 수 있습니다.

        **거래 방식:**
        1. 자발적 시장: 기업이나 개인이 자발적으로 참여하는 시장입니다.
        2. 규제 시장: 정부 규제에 따라 의무적으로 참여해야 하는 시장입니다.

        탄소 크레딧 거래는 온실가스 감축을 경제적으로 유도하고, 
        전 세계적으로 효율적인 탄소 감축을 달성하는 데 도움을 줍니다.
        """)

    st.write("여러분의 노력을 크레딧으로 보상받고 거래해보세요.")

    # 사용자 크레딧 현황
    user_credits = CreditManager.get_credit_balance(user_id)
    st.subheader("보유 탄소 크레딧")
    st.write(f"현재 보유 크레딧: {user_credits} 크레딧")

    # 거래 섹션
    st.subheader("크레딧 거래")
    transaction_type = st.selectbox("거래 유형 선택", ["구매", "판매"])

    if transaction_type == "판매":
        if user_credits > 0:
            max_value = min(int(user_credits), 1000)
            amount = st.number_input("거래할 크레딧 양", min_value=1, max_value=max_value, value=1)
        else:
            st.warning("판매할 크레딧이 없습니다.")
            amount = 0
    else:
        max_value = 1000
        amount = st.number_input("거래할 크레딧 양", min_value=1, max_value=max_value, value=1)

    if st.button("거래 실행"):
        if amount > 0:
            try:
                if transaction_type == "구매":
                    credit_id = CreditManager.issue_credit(amount, user_id)
                    st.success(f"{amount} 크레딧이 성공적으로 구매되었습니다. 크레딧 ID: {credit_id}")
                else:  # 판매
                    CreditManager.retire_credit(user_id, amount)
                    st.success(f"{amount} 크레딧이 성공적으로 판매되었습니다.")
                
                # 거래 후 업데이트된 크레딧 현황
                user_credits = CreditManager.get_credit_balance(user_id)
                st.write(f"현재 보유 크레딧: {user_credits} 크레딧")
            except ValueError as e:
                st.error(f"거래 실패: {str(e)}")
        else:
            st.error("거래할 크레딧 양을 입력해주세요.")

    # 거래 내역 확인
    st.subheader("거래 내역")
    transaction_history = CreditManager.get_transaction_history(user_id)
    if transaction_history:
        df = pd.DataFrame(transaction_history)
        st.write(df)
    else:
        st.write("거래 내역이 없습니다.")

    # 만료된 크레딧 처리
    CreditManager.expire_credits()

    # 추가 정보
    st.sidebar.header("💡 알고 계셨나요?")
    st.sidebar.info("""
    - 전 세계적으로 탄소 크레딧 시장의 규모는 계속 성장하고 있습니다.
    - 많은 기업들이 탄소 중립을 목표로 하고 있으며, 이를 위해 탄소 크레딧을 활용합니다.
    - 개인도 일상생활에서의 탄소 감축 노력을 통해 크레딧을 얻을 수 있습니다.
    - 탄소 크레딧 거래는 환경 보호와 경제적 이익을 동시에 추구할 수 있는 방법입니다.
    """)

if __name__ == "__main__":
    show()
