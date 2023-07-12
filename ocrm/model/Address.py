from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Address(Base):
    __tablename__ = 'user_addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    province = Column(String(255), nullable=False)
    cap = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
