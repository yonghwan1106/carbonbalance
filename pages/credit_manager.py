import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy 설정
Base = declarative_base()
engine = create_engine('sqlite:///carbon_credits.db', echo=True)
Session = sessionmaker(bind=engine)

class CarbonCredit(Base):
    __tablename__ = 'carbon_credits'

    id = Column(String, primary_key=True)
    amount = Column(Float)
    owner = Column(String)
    creation_date = Column(DateTime)
    expiration_date = Column(DateTime)
    is_active = Column(Boolean)

    def __init__(self, amount, owner, expiration_date=None):
        self.id = str(uuid.uuid4())
        self.amount = amount
        self.owner = owner
        self.creation_date = datetime.now()
        self.expiration_date = expiration_date or self.creation_date + timedelta(days=365)
        self.is_active = True

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    credit_id = Column(String)
    amount = Column(Float)
    from_owner = Column(String)
    to_owner = Column(String)
    date = Column(DateTime)

class CreditManager:
    def __init__(self):
        self.session = Session()

    def issue_credit(self, amount, owner):
        """탄소 크레딧 발행"""
        credit = CarbonCredit(amount, owner)
        self.session.add(credit)
        self.add_transaction("issue", credit.id, amount, owner=owner)
        self.session.commit()
        return credit.id

    def transfer_credit(self, credit_id, from_owner, to_owner, amount):
        """탄소 크레딧 거래"""
        credit = self.session.query(CarbonCredit).get(credit_id)
        if not credit or credit.owner != from_owner or credit.amount < amount:
            raise ValueError("거래할 수 없는 크레딧입니다.")
        
        credit.amount -= amount
        new_credit = CarbonCredit(amount, to_owner)
        self.session.add(new_credit)
        self.add_transaction("transfer", credit_id, amount, from_owner, to_owner)
        self.session.commit()
        return new_credit.id

    def retire_credit(self, credit_id, amount):
        """탄소 크레딧 소멸 (사용)"""
        credit = self.session.query(CarbonCredit).get(credit_id)
        if not credit or credit.amount < amount:
            raise ValueError("소멸할 수 없는 크레딧입니다.")
        
        credit.amount -= amount
        self.add_transaction("retire", credit_id, amount, owner=credit.owner)
        self.session.commit()

    def get_credit_balance(self, owner):
        """특정 소유자의 총 크레딧 잔액 조회"""
        total_balance = self.session.query(CarbonCredit).filter_by(owner=owner, is_active=True).with_entities(CarbonCredit.amount).all()
        return sum(balance[0] for balance in total_balance)

    def expire_credits(self):
        """만료된 크레딧 처리"""
        now = datetime.now()
        expired_credits = self.session.query(CarbonCredit).filter(CarbonCredit.expiration_date <= now, CarbonCredit.is_active == True).all()
        for credit in expired_credits:
            credit.is_active = False
            self.add_transaction("expire", credit.id, credit.amount, owner=credit.owner)
        self.session.commit()

    def get_transaction_history(self, owner=None):
        """거래 내역 조회"""
        query = self.session.query(Transaction)
        if owner:
            query = query.filter((Transaction.from_owner == owner) | (Transaction.to_owner == owner))
        return query.all()

    def add_transaction(self, type, credit_id, amount, from_owner=None, to_owner=None):
        """거래 내역 추가"""
        transaction = Transaction(type=type, credit_id=credit_id, amount=amount, 
                                  from_owner=from_owner, to_owner=to_owner, date=datetime.now())
        self.session.add(transaction)

    def close(self):
        """세션 종료"""
        self.session.close()

# 데이터베이스 테이블 생성
Base.metadata.create_all(engine)

# 사용 예시
if __name__ == "__main__":
    manager = CreditManager()
    
    try:
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
            print(f"{transaction.type}: {transaction.amount} (From: {transaction.from_owner}, To: {transaction.to_owner})")
    
    finally:
        manager.close()
