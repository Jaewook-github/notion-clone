# backend/app/models/database.py
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

# 데이터베이스와 뷰 설정을 위한 테이블
class Database(Base):
    __tablename__ = "databases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    description = Column(String(500), nullable=True)
    schema = Column(JSON)  # 데이터베이스 스키마 정의
    views = Column(JSON)   # 뷰 설정 저장
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    parent_id = Column(Integer, ForeignKey('pages.id'), nullable=True)

    # 관계 설정
    records = relationship("DatabaseRecord", back_populates="database", cascade="all, delete-orphan")
    page = relationship("Page", back_populates="databases")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "schema": self.schema,
            "views": self.views,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "parent_id": self.parent_id
        }

# 데이터베이스 레코드를 저장하는 테이블
class DatabaseRecord(Base):
    __tablename__ = "database_records"

    id = Column(Integer, primary_key=True, index=True)
    database_id = Column(Integer, ForeignKey('databases.id'))
    data = Column(JSON)    # 실제 레코드 데이터
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 설정
    database = relationship("Database", back_populates="records")

    def to_dict(self):
        return {
            "id": self.id,
            "database_id": self.database_id,
            "data": self.data,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

# 관계형 필드를 위한 연결 테이블
DatabaseRelation = Table(
    'database_relations',
    Base.metadata,
    Column('source_record_id', Integer, ForeignKey('database_records.id')),
    Column('target_record_id', Integer, ForeignKey('database_records.id')),
    Column('relation_type', String(50))
)