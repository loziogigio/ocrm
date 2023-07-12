from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean, CHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    short_name = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)
    UUID = Column(CHAR(36), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'short_name': self.short_name,
            'order': self.order,
            'UUID': self.UUID,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
