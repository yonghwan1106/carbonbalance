import uuid
from datetime import datetime, timedelta

class CarbonCredit:
    def __init__(self, amount, owner, expiration_date=None):
        self.id = str(uuid.uuid4())
        self.amount = amount
        self.owner = owner
        self.creation_date = datetime.now()
        self.expiration_date = expiration_date or self.creation_date + timedelta(days=365)
        self.is_active = True

class CreditManager:
    def __init__(self):
        self.credits = {}
        self.transactions = []

    def issue_credit(self, amount, owner):
        """탄소 크레딧 발행"""
        credit = CarbonCredit(amount, owner)
        self.credits[credit.id] = credit
        self.transactions.append({
            "type": "issue",
            "credit_id": credit.id,
            "amount": amount,
            "owner": owner,
            "date": datetime.now()
        })
        return credit.id

    def transfer_credit(self, credit_id, from_owner, to_owner, amount):
        """탄소 크레딧 거래"""
        if credit_id not in self.credits:
            raise ValueError("존재하지 않는 크레딧입니다.")
        
        credit = self.credits[credit_id]
        if credit.owner != from_owner:
            raise ValueError("크레딧 소유자가 아닙니다.")
        
        if credit.amount < amount:
            raise ValueError("크레딧 잔액이 부족합니다.")
        
        credit.amount -= amount
        new_credit_id = self.issue_credit(amount, to_owner)
        
        self.transactions.append({
            "type": "transfer",
            "from_credit_id": credit_id,
            "to_credit_id": new_credit_id,
            "amount": amount,
            "from_owner": from_owner,
            "to_owner": to_owner,
            "date": datetime.now()
        })
        
        return new_credit_id

    def retire_credit(self, credit_id, amount):
        """탄소 크레딧 소멸 (사용)"""
        if credit_id not in self.credits:
            raise ValueError("존재하지 않는 크레딧입니다.")
        
        credit = self.credits[credit_id]
        if credit.amount < amount:
            raise ValueError("크레딧 잔액이 부족합니다.")
        
        credit.amount -= amount
        
        self.transactions.append({
            "type": "retire",
            "credit_id": credit_id,
            "amount": amount,
            "owner": credit.owner,
            "date": datetime.now()
        })

    def get_credit_balance(self, owner):
        """특정 소유자의 총 크레딧 잔액 조회"""
        total_balance = sum(credit.amount for credit in self.credits.values() if credit.owner == owner and credit.is_active)
        return total_balance

    def expire_credits(self):
        """만료된 크레딧 처리"""
        now = datetime.now()
        for credit in self.credits.values():
            if credit.is_active and credit.expiration_date <= now:
                credit.is_active = False
                self.transactions.append({
                    "type": "expire",
                    "credit_id": credit.id,
                    "amount": credit.amount,
                    "owner": credit.owner,
                    "date": now
                })

    def get_transaction_history(self, owner=None):
        """거래 내역 조회"""
        if owner:
            return [t for t in self.transactions if t.get("owner") == owner or t.get("from_owner") == owner or t.get("to_owner") == owner]
        return self.transactions
        
    @staticmethod
    def expire_credits():
        session = get_db_session()
        now = datetime.utcnow()
        expired_credits = session.query(Credit).filter(Credit.expiration_date <= now, Credit.is_active == True).all()
        for credit in expired_credits:
            credit.is_active = False
        session.commit()
        session.close()
        
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
        print(transaction)
