
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Page])
def read_pages(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Retrieve pages"""
    pages = crud.page.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return pages

@router.post("/", response_model=schemas.Page)
def create_page(
    *,
    db: Session = Depends(deps.get_db),
    page_in: schemas.PageCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Create new page"""
    page = crud.page.create(db=db, obj_in=page_in, owner_id=current_user.id)
    return page

@router.put("/{id}", response_model=schemas.Page)
def update_page(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    page_in: schemas.PageUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Update a page"""
    page = crud.page.get(db=db, id=id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    if not crud.user.is_superuser(current_user) and (page.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    page = crud.page.update(db=db, db_obj=page, obj_in=page_in)
    return page

@router.get("/{id}", response_model=schemas.Page)
def read_page(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get page by ID"""
    page = crud.page.get(db=db, id=id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    if not crud.user.is_superuser(current_user) and (page.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return page

@router.delete("/{id}", response_model=schemas.Page)
def delete_page(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Delete page"""
    page = crud.page.get(db=db, id=id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    if not crud.user.is_superuser(current_user) and (page.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    page = crud.page.remove(db=db, id=id)
    return page