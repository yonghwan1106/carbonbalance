# 📊 credit_manager.py
# 🏷️ 탄소 크레딧 관리 시스템

import streamlit as st
from supabase import create_client, Client
import uuid
from datetime import datetime, timedelta

# Supabase 클라이언트 설정
url: str = st.secrets["supabase_url"]
key: str = st.secrets["supabase_key"]
supabase: Client = create_client(url, key)

class CreditManager:
    def __init__(self):
        self.check_tables()

    def check_tables(self):
        try:
            # carbon_credits 테이블 확인
            supabase.table("carbon_credits").select("id").limit(1).execute()
            # transactions 테이블 확인
            supabase.table("transactions").select("id").limit(1).execute()
            st.success("데이터베이스 테이블이 정상적으로 확인되었습니다.")
        except Exception as e:
            st.error(f"테이블 확인 중 오류 발생: {str(e)}")
            st.error("Supabase 대시보드에서 필요한 테이블을 생성해주세요.")

    def issue_credit(self, amount: float, owner_id: int):
        """탄소 크레딧 발행"""
        try:
            credit_data = {
                "amount": amount,
                "owner": owner_id,
                "expiration_date": (datetime.now() + timedelta(days=365)).isoformat()
            }
            result = supabase.table("carbon_credits").insert(credit_data).execute()
            credit_id = result.data[0]['id']
            self.add_transaction("issue", credit_id, amount, to_owner=owner_id)
            return credit_id
        except Exception as e:
            st.error(f"크레딧 발행 중 오류 발생: {str(e)}")
            return None

    def transfer_credit(self, credit_id: str, from_owner_id: int, to_owner_id: int, amount: float):
        """탄소 크레딧 거래"""
        try:
            credit = supabase.table("carbon_credits").select("*").eq("id", credit_id).single().execute().data
            if not credit or credit["owner"] != from_owner_id or credit["amount"] < amount:
                raise ValueError("거래할 수 없는 크레딧입니다.")
            
            supabase.table("carbon_credits").update({"amount": credit["amount"] - amount}).eq("id", credit_id).execute()
            new_credit_id = self.issue_credit(amount, to_owner_id)
            self.add_transaction("transfer", credit_id, amount, from_owner_id, to_owner_id)
            return new_credit_id
        except Exception as e:
            st.error(f"크레딧 거래 중 오류 발생: {str(e)}")
            return None

    def retire_credit(self, credit_id: str, amount: float):
        """탄소 크레딧 소멸 (사용)"""
        try:
            credit = supabase.table("carbon_credits").select("*").eq("id", credit_id).single().execute().data
            if not credit or credit["amount"] < amount:
                raise ValueError("소멸할 수 없는 크레딧입니다.")
            
            supabase.table("carbon_credits").update({"amount": credit["amount"] - amount}).eq("id", credit_id).execute()
            self.add_transaction("retire", credit_id, amount, from_owner=credit["owner"])
        except Exception as e:
            st.error(f"크레딧 소멸 중 오류 발생: {str(e)}")

    def get_credit_balance(self, owner_id: int):
        """특정 소유자의 총 크레딧 잔액 조회"""
        try:
            result = supabase.table("carbon_credits").select("amount").eq("owner", owner_id).eq("is_active", True).execute()
            return sum(credit["amount"] for credit in result.data)
        except Exception as e:
            st.error(f"크레딧 잔액 조회 중 오류 발생: {str(e)}")
            return 0

    def expire_credits(self):
        """만료된 크레딧 처리"""
        try:
            now = datetime.now().isoformat()
            expired_credits = supabase.table("carbon_credits").select("*").lt("expiration_date", now).eq("is_active", True).execute().data
            for credit in expired_credits:
                supabase.table("carbon_credits").update({"is_active": False}).eq("id", credit["id"]).execute()
                self.add_transaction("expire", credit["id"], credit["amount"], from_owner=credit["owner"])
        except Exception as e:
            st.error(f"크레딧 만료 처리 중 오류 발생: {str(e)}")

    def get_transaction_history(self, owner_id: int = None):
        """거래 내역 조회"""
        try:
            query = supabase.table("transactions").select("*")
            if owner_id:
                query = query.or_(f"from_owner.eq.{owner_id},to_owner.eq.{owner_id}")
            return query.execute().data
        except Exception as e:
            st.error(f"거래 내역 조회 중 오류 발생: {str(e)}")
            return []

    def add_transaction(self, type: str, credit_id: str, amount: float, from_owner: int = None, to_owner: int = None):
        """거래 내역 추가"""
        try:
            transaction_data = {
                "type": type,
                "credit_id": credit_id,
                "amount": amount,
                "from_owner": from_owner,
                "to_owner": to_owner
            }
            supabase.table("transactions").insert(transaction_data).execute()
        except Exception as e:
            st.error(f"거래 내역 추가 중 오류 발생: {str(e)}")

# 사용 예시
if __name__ == "__main__":
    try:
        manager = CreditManager()
        
        # 크레딧 발행 테스트 (사용자 ID 1번에게 100 크레딧 발행)
        credit_id1 = manager.issue_credit(100, 1)
        if credit_id1:
            st.success(f"크레딧 발행 성공: {credit_id1}")
        
        # 잔액 조회 테스트
        balance = manager.get_credit_balance(1)
        st.write(f"사용자 1번 잔액: {balance}")
        
    except Exception as e:
        st.error(f"전체 실행 중 오류 발생: {str(e)}")
