from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Page(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(JSON)
    parent_id = Column(Integer, ForeignKey('page.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey('user.id'))
    
    children = relationship("Page", backref="parent", remote_side=[id])
    owner = relationship("User", back_populates="pages")