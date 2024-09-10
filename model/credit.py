from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Credit(Base):
    __tablename__ = 'credits'

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    creation_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    owner = relationship("User", back_populates="credits")
