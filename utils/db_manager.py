from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models.user import User
from models.credit import Credit

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_db_session():
    return Session()

def init_db():
    Base.metadata.create_all(engine)
