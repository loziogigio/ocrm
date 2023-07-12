from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, CHAR, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Area(Base):
    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, nullable=True)
    lft = Column(Integer, nullable=True)
    rgt = Column(Integer, nullable=True)
    depth = Column(Integer, nullable=True)
    name = Column(String(255), nullable=False)
    featured = Column(Boolean, default=False)
    UUID = Column(CHAR(36), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'lft': self.lft,
            'rgt': self.rgt,
            'depth': self.depth,
            'name': self.name,
            'featured': self.featured,
            'UUID': self.UUID,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
