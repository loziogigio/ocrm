from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):  
    __tablename__ = 'orders' 

    id = Column(Integer, primary_key=True, autoincrement=True)
    pratica = Column(String(45))
    participants = Column(LONGTEXT, nullable=False)
    prices = Column(LONGTEXT, nullable=False)
    category = Column(LONGTEXT, nullable=False)
    flight = Column(String(45))
    flight_detail = Column(LONGTEXT)
    offline = Column(Integer)
    is_cc = Column(Integer)
    closing_details = Column(LONGTEXT)
    cabin = Column(Integer, nullable=False)
    option = Column(LONGTEXT, nullable=False)
    history = Column(LONGTEXT, nullable=False)
    flat = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Assuming the foreign key 'users.id'
    admin_id = Column(Integer, ForeignKey('admins.id'))  # Assuming the foreign key 'admins.id'
    cruise_id = Column(Integer, ForeignKey('cruises.id'))  # Assuming the foreign key 'cruises.id'
    cabin_type_id = Column(Integer, ForeignKey('cabin_types.id'))  # Assuming the foreign key 'cabin_types.id'
    price_type_id = Column(Integer, ForeignKey('price_types.id'))  # Assuming the foreign key 'price_types.id'
    payment_rule_id = Column(Integer, ForeignKey('payment_rules.id'))  # Assuming the foreign key 'payment_rules.id'
    membership_id = Column(Integer, ForeignKey('memberships.id'))  # Assuming the foreign key 'memberships.id'
    pax_type_id = Column(Integer, ForeignKey('pax_types.id'))  # Assuming the foreign key 'pax_types.id'
    quote_id = Column(Integer, ForeignKey('quotes.id'))  # Assuming the foreign key 'quotes.id'
    last_price_update = Column(DateTime, nullable=False)
    UUID = Column(String(36), nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())  # Default current timestamp
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  # Default current timestamp and updates when a row is updated

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
