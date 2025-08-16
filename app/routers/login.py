from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, db
from ..repository import login

router = APIRouter()

get_db = db.get_db

@router.post('/register', response_model=schemas.MessageResponse)
def registerUser(user_data: schemas.CreateUser, db:Session = Depends(db.get_db)):
    return login.registerUser(user_data, db)

@router.post('/login', response_model=schemas.MessageResponse)
def loginUser(user_data: schemas.LoginUser, db:Session = Depends(db.get_db)):
    return login.loginUser(user_data, db)