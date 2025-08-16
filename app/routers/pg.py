from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, db
from ..repository import pg
from typing import List

router = APIRouter(
    prefix = '/pg',
    tags = ['PG']
)

@router.post('/create', response_model=schemas.MessageResponse)
def create_pg(pg_data: schemas.PGCreate, db:Session = Depends(db.get_db)):
    return pg.create_pg(pg_data, db)

@router.get('/', response_model=list[schemas.PGResponse])
def show_all(db: Session = Depends(db.get_db)):
    return pg.show_all(db)

@router.get('/{id}', response_model=schemas.PGResponse)
def show(id:int, db: Session = Depends(db.get_db)):
    return pg.show(id, db)

@router.put('/{id}', response_model=schemas.PGUpdateResponse)
def update(id, request: schemas.PGUpdate, db: Session = Depends(db.get_db)):
    updated_pg = pg.update(id, request, db)
    return {
        "message": "Details updated successfully!",
        "updated_pg": updated_pg  # FastAPI converts SQLAlchemy object using PGResponse
    }