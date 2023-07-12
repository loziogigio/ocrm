from sqlalchemy import Column, String, Integer, Boolean, CHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Port(Base):
    __tablename__ = 'ports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    locode = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    valid = Column(Boolean, default=True)
    enable = Column(Boolean, default=True)
    country_id = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    # location = Column(Point, nullable=True) # for simplicity we will comment this out
    featured = Column(Boolean, default=False)
    order = Column(Integer, nullable=True)
    UUID = Column(CHAR(36), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'locode': self.locode,
            'name': self.name,
            'valid': self.valid,
            'enable': self.enable,
            'country_id': self.country_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            # 'location': self.location, # for simplicity we will comment this out
            'featured': self.featured,
            'order': self.order,
            'UUID': self.UUID,
        }
