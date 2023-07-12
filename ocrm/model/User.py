from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean, CHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    default_shipping_address_id = Column(Integer, index=True, nullable=True)
    default_billing_address_id = Column(Integer, index=True, nullable=True)
    last_login = Column(DateTime, nullable=True)
    remember_token = Column(String(100), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    tax_code = Column(String(255), nullable=True)
    nationality = Column(String(255), nullable=True)
    birth = Column(DateTime, nullable=True)
    UUID = Column(CHAR(36), nullable=False)
    phone = Column(String(255), nullable=True)
    newsletter = Column(Boolean, nullable=False)
    card = Column(String(255), nullable=False)
    sms = Column(Boolean, nullable=False)
    note = Column(Text, nullable=True)
    is_auth_api = Column(Boolean, nullable=False)
    old_backup = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'default_shipping_address_id': self.default_shipping_address_id,
            'default_billing_address_id': self.default_billing_address_id,
            'last_login': self.last_login,
            'remember_token': self.remember_token,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'tax_code': self.tax_code,
            'nationality': self.nationality,
            'birth': self.birth,
            'UUID': self.UUID,
            'phone': self.phone,
            'newsletter': self.newsletter,
            'card': self.card,
            'sms': self.sms,
            'note': self.note,
            'is_auth_api': self.is_auth_api,
            'old_backup': self.old_backup
        }
