from typing import Optional, Dict, List
from datetime import datetime
from pydantic import BaseModel

class PageBase(BaseModel):
    title: str
    content: Dict
    parent_id: Optional[int] = None

class PageCreate(PageBase):
    pass

class PageUpdate(PageBase):
    title: Optional[str] = None
    content: Optional[Dict] = None

class Page(PageBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int

    class Config:
        orm_mode = True