from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, db, models


def create_pg(pg_data: schemas.PGCreate, db:Session = Depends(db.get_db)):
    new_pg = models.PG(
        name = pg_data.name,
        address = pg_data.address,
        rooms = pg_data.rooms,
        rent = pg_data.rent,
        amenities = pg_data.amenities
    )
    db.add(new_pg)
    db.commit()
    db.refresh(new_pg)
    return {"message" : "PG Details added Successfully !"}

def show_all(db: Session = Depends(db.get_db)):
    pgs = db.query(models.PG).all()
    return pgs

def show(id, db: Session = Depends(db.get_db)):
    pg = db.query(models.PG).filter(models.PG.id==id).first()
    if not pg:
        raise HTTPException(status_code=404, detail = f"PG with the id {id} is not available")
    return pg

def update(id, request: schemas.PGUpdate, db: Session = Depends(db.get_db)):
    pg = db.query(models.PG).filter(models.PG.id==id).first()
    if not pg:
        raise HTTPException(status_code=404, detail = f"PG with the id {id} is not available")
    
    for field, value in request.dict(exclude_unset=True).items():
        setattr(pg, field, value)

    db.commit()
    db.refresh(pg)
    return pg 

def delete(id, db: Session = Depends(db.get_db)):
    pg = db.query(models.PG).filter(models.PG.id == id).delete(synchronize_session=False)
    if not pg:
        raise HTTPException(status_code=404, detail = f"PG with the id {id} is not available")
    db.commit()
    return {"message" : "Deleted the PG details !"}
