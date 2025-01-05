
from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.api import deps
from app.schemas.database import ViewConfig

router = APIRouter()

@router.post("/{database_id}/views/{view_id}/clone")
async def clone_view(
    *,
    db: Session = Depends(deps.get_db),
    database_id: int,
    view_id: str,
    new_name: str = None
) -> Any:
    """뷰 복제"""
    try:
        cloned_view = await crud.database_view.clone_view(
            db=db,
            database_id=database_id,
            view_id=view_id,
            new_name=new_name
        )
        return cloned_view
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))