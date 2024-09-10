from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models.user import User
from models.credit import Credit
from models.credit import Base as CreditBase

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_db_session():
    return Session()

def init_db():
    UserBase.metadata.create_all(engine)
    CreditBase.metadata.create_all(engine)

# 애플리케이션 시작 시 이 함수를 호출하세요
init_db()
