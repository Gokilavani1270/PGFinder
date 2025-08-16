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
