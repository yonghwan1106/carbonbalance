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
        self.create_tables_if_not_exist()

    def create_tables_if_not_exist(self):
        # carbon_credits 테이블 생성
        supabase.table("carbon_credits").insert({
            "id": "dummy",
            "amount": 0,
            "owner": "dummy",
            "creation_date": datetime.now().isoformat(),
            "expiration_date": datetime.now().isoformat(),
            "is_active": False
        }).execute()

        # transactions 테이블 생성
        supabase.table("transactions").insert({
            "type": "dummy",
            "credit_id": "dummy",
            "amount": 0,
            "from_owner": "dummy",
            "to_owner": "dummy",
            "date": datetime.now().isoformat()
        }).execute()

        # 더미 데이터 삭제
        supabase.table("carbon_credits").delete().eq("id", "dummy").execute()
        supabase.table("transactions").delete().eq("credit_id", "dummy").execute()

    def issue_credit(self, amount: float, owner: str):
        """탄소 크레딧 발행"""
        credit_id = str(uuid.uuid4())
        credit_data = {
            "id": credit_id,
            "amount": amount,
            "owner": owner,
            "creation_date": datetime.now().isoformat(),
            "expiration_date": (datetime.now() + timedelta(days=365)).isoformat(),
            "is_active": True
        }
        supabase.table("carbon_credits").insert(credit_data).execute()
        self.add_transaction("issue", credit_id, amount, owner=owner)
        return credit_id

    def transfer_credit(self, credit_id: str, from_owner: str, to_owner: str, amount: float):
        """탄소 크레딧 거래"""
        credit = supabase.table("carbon_credits").select("*").eq("id", credit_id).execute().data[0]
        if not credit or credit["owner"] != from_owner or credit["amount"] < amount:
            raise ValueError("거래할 수 없는 크레딧입니다.")
        
        supabase.table("carbon_credits").update({"amount": credit["amount"] - amount}).eq("id", credit_id).execute()
        new_credit_id = self.issue_credit(amount, to_owner)
        self.add_transaction("transfer", credit_id, amount, from_owner, to_owner)
        return new_credit_id

    def retire_credit(self, credit_id: str, amount: float):
        """탄소 크레딧 소멸 (사용)"""
        credit = supabase.table("carbon_credits").select("*").eq("id", credit_id).execute().data[0]
        if not credit or credit["amount"] < amount:
            raise ValueError("소멸할 수 없는 크레딧입니다.")
        
        supabase.table("carbon_credits").update({"amount": credit["amount"] - amount}).eq("id", credit_id).execute()
        self.add_transaction("retire", credit_id, amount, owner=credit["owner"])

    def get_credit_balance(self, owner: str):
        """특정 소유자의 총 크레딧 잔액 조회"""
        credits = supabase.table("carbon_credits").select("amount").eq("owner", owner).eq("is_active", True).execute().data
        return sum(credit["amount"] for credit in credits)

    def expire_credits(self):
        """만료된 크레딧 처리"""
        now = datetime.now().isoformat()
        expired_credits = supabase.table("carbon_credits").select("*").lt("expiration_date", now).eq("is_active", True).execute().data
        for credit in expired_credits:
            supabase.table("carbon_credits").update({"is_active": False}).eq("id", credit["id"]).execute()
            self.add_transaction("expire", credit["id"], credit["amount"], owner=credit["owner"])

    def get_transaction_history(self, owner: str = None):
        """거래 내역 조회"""
        query = supabase.table("transactions").select("*")
        if owner:
            query = query.or_(f"from_owner.eq.{owner},to_owner.eq.{owner}")
        return query.execute().data

    def add_transaction(self, type: str, credit_id: str, amount: float, from_owner: str = None, to_owner: str = None):
        """거래 내역 추가"""
        transaction_data = {
            "type": type,
            "credit_id": credit_id,
            "amount": amount,
            "from_owner": from_owner,
            "to_owner": to_owner,
            "date": datetime.now().isoformat()
        }
        supabase.table("transactions").insert(transaction_data).execute()

# 사용 예시
if __name__ == "__main__":
    manager = CreditManager()
    
    # 크레딧 발행
    credit_id1 = manager.issue_credit(100, "User1")
    credit_id2 = manager.issue_credit(50, "User2")
    
    # 크레딧 거래
    manager.transfer_credit(credit_id1, "User1", "User2", 30)
    
    # 크레딧 소멸
    manager.retire_credit(credit_id2, 20)
    
    # 잔액 조회
    print(f"User1 balance: {manager.get_credit_balance('User1')}")
    print(f"User2 balance: {manager.get_credit_balance('User2')}")
    
    # 거래 내역 조회
    print("Transaction history:")
    for transaction in manager.get_transaction_history():
        print(f"{transaction['type']}: {transaction['amount']} (From: {transaction['from_owner']}, To: {transaction['to_owner']})")
