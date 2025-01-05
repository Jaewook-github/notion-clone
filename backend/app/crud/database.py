from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.database import Database, DatabaseRecord
from app.schemas.database import DatabaseCreate, DatabaseUpdate
from .base import CRUDBase

class CRUDDatabase(CRUDBase[Database, DatabaseCreate, DatabaseUpdate]):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Database]:
        return (
            db.query(self.model)
            .filter(Database.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

database = CRUDDatabase(Database)