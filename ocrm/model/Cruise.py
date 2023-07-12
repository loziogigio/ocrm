# ocrm/model/Cruise.py

from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean, CHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cruise(Base):
    __tablename__ = 'cruises'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    name = Column('name', String(255), nullable=False)
    display_name = Column('display_name', String(255), nullable=False)
    adv = Column('adv', String(255))
    code = Column('code', String(255), nullable=False)
    original_code = Column('original_code', String(255), nullable=False)
    area_code = Column('area_code', String(255), nullable=False)
    duration = Column('duration', Integer, nullable=False)
    date_start = Column('date_start', DateTime, nullable=False)
    date_end = Column('date_end', DateTime, nullable=False)
    featured = Column('featured', Boolean, default=False)
    active = Column('active', Boolean, default=True)
    immediate_confirm = Column('immediate_confirm', Boolean, default=False)
    company_id = Column('company_id', Integer, nullable=False)
    ship_id = Column('ship_id', Integer, nullable=False)
    cruise_group_id = Column('cruise_group_id', Integer, nullable=True)
    UUID = Column('UUID', CHAR(36), nullable=False)
    flights = Column('flights', Text)
    flight_type = Column('flight_type', Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'display_name': self.display_name,
            'adv': self.adv,
            'code': self.code,
            'original_code': self.original_code,
            'area_code': self.area_code,
            'duration': self.duration,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'featured': self.featured,
            'active': self.active,
            'immediate_confirm': self.immediate_confirm,
            'company_id': self.company_id,
            'ship_id': self.ship_id,
            'cruise_group_id': self.cruise_group_id,
            'UUID': self.UUID,
            'flights': self.flights,
            'flight_type': self.flight_type,
        }
