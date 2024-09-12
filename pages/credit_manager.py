# 📊 credit_manager.py
# 🏷️ 탄소 크레딧 관리 시스템

from supabase import create_client, Client
import uuid
from datetime import datetime, timedelta
import logging


class CreditManager:
    def __init__(self, url: str, key: str):
        self.supabase: Client = create_client(url, key)

    def check_tables(self):
        try:
            self.supabase.table("carbon_credits").select("id").limit(1).execute()
            self.supabase.table("transactions").select("id").limit(1).execute()
            return True
        except Exception as e:
            return f"테이블 확인 중 오류 발생: {str(e)}"

    def issue_credit(self, amount: float, owner_id: int):
        try:
            user = self.supabase.table("users").select("id").eq("id", owner_id).execute()
            if not user.data:
                raise ValueError(f"사용자 ID {owner_id}가 존재하지 않습니다.")

            credit_data = {
                "amount": amount,
                "owner": owner_id,
                "expiration_date": (datetime.now() + timedelta(days=365)).isoformat()
            }
            result = self.supabase.table("carbon_credits").insert(credit_data).execute()
            credit_id = result.data[0]['id']
            self.add_transaction("issue", credit_id, amount, to_owner=owner_id)
            return credit_id
        except Exception as e:
            raise Exception(f"크레딧 발행 중 오류 발생: {str(e)}")

    def transfer_credit(self, credit_id: str, from_owner_id: int, to_owner_id: int, amount: float):
        try:
            credit = self.supabase.table("carbon_credits").select("*").eq("id", credit_id).single().execute().data
            if not credit or credit["owner"] != from_owner_id or credit["amount"] < amount:
                raise ValueError("거래할 수 없는 크레딧입니다.")
            
            self.supabase.table("carbon_credits").update({"amount": credit["amount"] - amount}).eq("id", credit_id).execute()
            new_credit_id = self.issue_credit(amount, to_owner_id)
            self.add_transaction("transfer", credit_id, amount, from_owner_id, to_owner_id)
            return new_credit_id
        except Exception as e:
            raise Exception(f"크레딧 거래 중 오류 발생: {str(e)}")

    def retire_credit(self, credit_id: str, amount: float):
        try:
            credit = self.supabase.table("carbon_credits").select("*").eq("id", credit_id).single().execute().data
            if not credit or credit["amount"] < amount:
                raise ValueError("소멸할 수 없는 크레딧입니다.")
            
            self.supabase.table("carbon_credits").update({"amount": credit["amount"] - amount}).eq("id", credit_id).execute()
            self.add_transaction("retire", credit_id, amount, from_owner=credit["owner"])
        except Exception as e:
            raise Exception(f"크레딧 소멸 중 오류 발생: {str(e)}")

    def get_credit_balance(self, owner_id: int):
        try:
            result = self.supabase.table("carbon_credits").select("amount").eq("owner", owner_id).eq("is_active", True).execute()
            return sum(credit["amount"] for credit in result.data)
        except Exception as e:
            raise Exception(f"크레딧 잔액 조회 중 오류 발생: {str(e)}")

    def expire_credits(self):
        try:
            now = datetime.now().isoformat()
            expired_credits = self.supabase.table("carbon_credits").select("*").lt("expiration_date", now).eq("is_active", True).execute().data
            for credit in expired_credits:
                self.supabase.table("carbon_credits").update({"is_active": False}).eq("id", credit["id"]).execute()
                self.add_transaction("expire", credit["id"], credit["amount"], from_owner=credit["owner"])
            logging.info(f"{len(expired_credits)} 크레딧이 만료 처리되었습니다.")
        except Exception as e:
            logging.error(f"크레딧 만료 처리 중 오류 발생: {str(e)}")

    def get_transaction_history(self, owner_id: int = None):
        try:
            query = self.supabase.table("transactions").select("*")
            if owner_id:
                query = query.or_(f"from_owner.eq.{owner_id},to_owner.eq.{owner_id}")
            return query.execute().data
        except Exception as e:
            raise Exception(f"거래 내역 조회 중 오류 발생: {str(e)}")

    def add_transaction(self, type: str, credit_id: str, amount: float, from_owner: int = None, to_owner: int = None):
        try:
            transaction_data = {
                "type": type,
                "credit_id": credit_id,
                "amount": amount,
                "from_owner": from_owner,
                "to_owner": to_owner
            }
            self.supabase.table("transactions").insert(transaction_data).execute()
        except Exception as e:
            raise Exception(f"거래 내역 추가 중 오류 발생: {str(e)}")

    def execute_transaction(self, user_id: int, transaction_type: str, amount: float):
        try:
            if transaction_type == "buy":
                return self.issue_credit(amount, user_id)
            elif transaction_type == "sell":
                user_credits = self.supabase.table("carbon_credits").select("*").eq("owner", user_id).eq("is_active", True).execute().data
                if user_credits:
                    credit_to_sell = user_credits[0]
                    self.retire_credit(credit_to_sell["id"], amount)
                    return True
                else:
                    raise ValueError("판매할 크레딧이 없습니다.")
            else:
                raise ValueError("잘못된 거래 유형입니다.")
        except Exception as e:
            raise Exception(f"거래 실행 중 오류 발생: {str(e)}")

    def get_user_profile(self, user_id: int):
        try:
            user = self.supabase.table("users").select("*").eq("id", user_id).single().execute().data
            if not user:
                raise ValueError(f"사용자 ID {user_id}가 존재하지 않습니다.")
            return user
        except Exception as e:
            raise Exception(f"사용자 프로필 조회 중 오류 발생: {str(e)}")

    def update_user_profile(self, user_id: int, update_data: dict):
        try:
            self.supabase.table("users").update(update_data).eq("id", user_id).execute()
        except Exception as e:
            raise Exception(f"사용자 프로필 업데이트 중 오류 발생: {str(e)}")

# 사용 예시
if __name__ == "__main__":
    import streamlit as st

    # Supabase 클라이언트 설정
    url: str = st.secrets["supabase_url"]
    key: str = st.secrets["supabase_key"]

    try:
        manager = CreditManager(url, key)
        
        # 실제 존재하는 사용자 ID를 사용 (예: 5번 사용자 sano3383)
        test_user_id = 5
        
        # 크레딧 발행 테스트
        credit_id1 = manager.issue_credit(100, test_user_id)
        if credit_id1:
            st.success(f"크레딧 발행 성공: {credit_id1}")
        else:
            st.error("크레딧 발행 실패")
        
        # 잔액 조회 테스트
        balance = manager.get_credit_balance(test_user_id)
        st.write(f"사용자 {test_user_id}번 (sano3383) 잔액: {balance}")
        
        # 다른 사용자에게 크레딧 전송 테스트
        if credit_id1:
            transfer_amount = 30
            to_user_id = 6  # sanoramyun8
            new_credit_id = manager.transfer_credit(credit_id1, test_user_id, to_user_id, transfer_amount)
            if new_credit_id:
                st.success(f"크레딧 전송 성공: {transfer_amount} 크레딧을 사용자 {to_user_id}번에게 전송")
            else:
                st.error("크레딧 전송 실패")
            
            # 전송 후 잔액 확인
            balance_after = manager.get_credit_balance(test_user_id)
            st.write(f"전송 후 사용자 {test_user_id}번 잔액: {balance_after}")
            
            receiver_balance = manager.get_credit_balance(to_user_id)
            st.write(f"수신자 (사용자 {to_user_id}번) 잔액: {receiver_balance}")
        
    except Exception as e:
        st.error(f"전체 실행 중 오류 발생: {str(e)}")