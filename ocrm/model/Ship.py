# ocrm/model/Ship.py

from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean, CHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Ship(Base):
    __tablename__ = 'ships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    code = Column(String(255), nullable=False)
    featured = Column(Boolean, default=False)
    order = Column(Integer, nullable=True)
    active = Column(Boolean, nullable=False)
    UUID = Column(CHAR(36), nullable=False)
    company_id = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'featured': self.featured,
            'order': self.order,
            'active': self.active,
            'UUID': self.UUID,
            'company_id': self.company_id,
        }
