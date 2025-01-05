from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.page import Page
from app.schemas.page import PageCreate, PageUpdate
from .base import CRUDBase

class CRUDPage(CRUDBase[Page, PageCreate, PageUpdate]):
    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Page]:
        return (
            db.query(self.model)
            .filter(Page.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

page = CRUDPage(Page)