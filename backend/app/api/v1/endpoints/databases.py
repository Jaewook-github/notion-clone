# backend/app/api/v1/endpoints/databases.py
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Database])
def read_databases(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Retrieve databases"""
    databases = crud.database.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return databases

@router.post("/", response_model=schemas.Database)
def create_database(
    *,
    db: Session = Depends(deps.get_db),
    database_in: schemas.DatabaseCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Create new database"""
    database = crud.database.create(
        db=db, obj_in=database_in, owner_id=current_user.id
    )
    return database

@router.put("/{id}", response_model=schemas.Database)
def update_database(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    database_in: schemas.DatabaseUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Update a database"""
    database = crud.database.get(db=db, id=id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    if not crud.user.is_superuser(current_user) and (database.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    database = crud.database.update(
        db=db, db_obj=database, obj_in=database_in
    )
    return database

@router.get("/{id}", response_model=schemas.Database)
def read_database(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Get database by ID"""
    database = crud.database.get(db=db, id=id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    if not crud.user.is_superuser(current_user) and (database.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return database

@router.delete("/{id}", response_model=schemas.Database)
def delete_database(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Delete database"""
    database = crud.database.get(db=db, id=id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    if not crud.user.is_superuser(current_user) and (database.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    database = crud.database.remove(db=db, id=id)
    return database

# Database Records API
@router.post("/{database_id}/records/", response_model=schemas.DatabaseRecord)
def create_database_record(
    *,
    db: Session = Depends(deps.get_db),
    database_id: int,
    record_in: schemas.DatabaseRecordCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Create new database record"""
    database = crud.database.get(db=db, id=database_id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    if not crud.user.is_superuser(current_user) and (database.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    record = crud.database_record.create(
        db=db,
        obj_in=record_in
    )
    return record

@router.get("/{database_id}/records/", response_model=List[schemas.DatabaseRecord])
def read_database_records(
    *,
    db: Session = Depends(deps.get_db),
    database_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """Retrieve database records"""
    database = crud.database.get(db=db, id=database_id)
    if not database:
        raise HTTPException(status_code=404, detail="Database not found")
    if not crud.user.is_superuser(current_user) and (database.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    records = crud.database_record.get_multi_by_database(
        db=db, database_id=database_id, skip=skip, limit=limit
    )
    return records