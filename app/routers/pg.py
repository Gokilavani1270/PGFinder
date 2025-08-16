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
def show(db: Session = Depends(db.get_db)):
    return pg.show(db)