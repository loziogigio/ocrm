from sqlalchemy import create_engine, Column, String, Integer, DateTime, Text, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CruiseGroup(Base):
    __tablename__ = 'cruise_groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(255), nullable=False)
    coords = Column(LONGTEXT, nullable=True)
    static = Column(String(255), nullable=True)
    static_small = Column(String(255), nullable=False)
    area_id = Column(Integer, index=True, nullable=True)
    custom_area_id = Column(Integer, index=True, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'coords': self.coords,
            'static': self.static,
            'static_small': self.static_small,
            'area_id': self.area_id,
            'custom_area_id': self.custom_area_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
